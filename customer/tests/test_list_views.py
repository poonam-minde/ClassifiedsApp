from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ad.models import JobAd, SaleAd, RentalAd, ServiceAd, EventAd, ClassAd
import datetime

class BaseListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('customer:sale_list') 

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'customer/list.html')

    def test_view_context_object_name(self):
        response = self.client.get(self.url)
        self.assertIn('ads', response.context)

class JobListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.url = reverse('customer:job_list')
        self.job_ad1 = JobAd.objects.create( 
            title='Test Job Ad 1',
            category='FT',
            description='Job description',
            tags='job',
            email='test@example.com',
            phone='1234567890',
            location='Test Location',
            postal_code='12345',
            salary=50000,
            owner=self.user,)
        self.job_ad2 = JobAd.objects.create( 
            title='Test Job Ad 2',
            category='PT',
            description='Job description',
            tags='job',
            email='test@example.com',
            phone='1234567890',
            location='Test Location',
            postal_code='12345',
            salary=50000,
            owner=self.user,)


    def test_context_contains_ad_type(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['ad_type'], 'job')

    def test_context_contains_job_ads(self):
        response = self.client.get(self.url)
        self.assertIn('ads', response.context)
        self.assertEqual(response.context['ads'].count(), 2)
        self.assertQuerysetEqual(
            response.context['ads'],
            [self.job_ad1, self.job_ad2],
            transform=lambda x: x,
            ordered=False
        )

    def test_response_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

class SaleListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.url = reverse('customer:sale_list')
        self.sale_ad = SaleAd.objects.create(
            title='Test Sale Ad',
            category='FU',
            description='Sale description',
            tags='sale',
            price=50000,
            owner=self.user,
        )

    def test_context_contains_ad_type(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['ad_type'], 'sale')

    def test_context_contains_job_ads(self):
        # Test if the context contains the correct queryset of job ads
        response = self.client.get(self.url)
        self.assertIn('ads', response.context)
        self.assertEqual(response.context['ads'].count(), 1)
        self.assertQuerysetEqual(
            response.context['ads'],
            [self.sale_ad],
            transform=lambda x: x,
            ordered=False
        )

    def test_response_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

class RentalListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.url = reverse('customer:rental_list')
        self.rental_ad = RentalAd.objects.create(
            title='Test Rental Ad',
            category='FT',
            description='Rental description',
            tags='rental',
            email='test@example.com',
            phone='1234567890',
            charge=50000,
            period='MO',
            owner=self.user,
        )
        self.other_rental_ad = RentalAd.objects.create(
            title='Test Rental Ad 2',
            category='FT',
            description='Rental description',
            tags='rental',
            email='test@example.com',
            phone='1234567890',
            charge=50000,
            period='MO',
            owner=self.user,
        )


    def test_context_contains_ad_type(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['ad_type'], 'rental')

    def test_context_contains_job_ads(self):
        # Test if the context contains the correct queryset of job ads
        response = self.client.get(self.url)
        self.assertIn('ads', response.context)
        self.assertEqual(response.context['ads'].count(), 2)
        self.assertQuerysetEqual(
            response.context['ads'],
            [self.rental_ad, self.other_rental_ad],
            transform=lambda x: x,
            ordered=False
        )

    def test_response_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

class ServiceListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.url = reverse('customer:service_list')
        self.service_ad = ServiceAd.objects.create(
            title='Test Service Ad',
            category='LE',
            description='Job description',
            tags='job',
            email='test@example.com',
            phone='1234567890',
            price=50000,
            owner=self.user,
        )

    def test_context_contains_ad_type(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['ad_type'], 'service')

    def test_context_contains_job_ads(self):
        response = self.client.get(self.url)
        self.assertIn('ads', response.context)
        self.assertEqual(response.context['ads'].count(), 1)
        self.assertQuerysetEqual(
            response.context['ads'],
            [self.service_ad],
            transform=lambda x: x,
            ordered=False
        )

    def test_response_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

class EventListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.url = reverse('customer:event_list')
        self.event_ad = EventAd.objects.create(
            title='Test Event Ad',
            category='SE',
            description='Event description',
            tags='event',
            email='test@example.com',
            phone='1234567890',
            location='Test Location',
            postal_code='12345',
            price=50000,
            owner=self.user,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now(),
        )

    def test_context_contains_ad_type(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['ad_type'], 'event')

    def test_context_contains_job_ads(self):
        response = self.client.get(self.url)
        self.assertIn('ads', response.context)
        self.assertEqual(response.context['ads'].count(), 1)
        self.assertQuerysetEqual(
            response.context['ads'],
            [self.event_ad],
            transform=lambda x: x,
            ordered=False
        )

    def test_response_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

class ClassListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.url = reverse('customer:class_list')
        self.class_ad = ClassAd.objects.create(
            title='Test Class Ad',
            category='WO',
            description='Class description',
            tags='class',
            email='test@example.com',
            phone='1234567890',
            location='Test Location',
            postal_code='12345',
            fees=50000,
            owner=self.user,
        )

    def test_context_contains_ad_type(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['ad_type'], 'class')

    def test_context_contains_job_ads(self):
        response = self.client.get(self.url)
        self.assertIn('ads', response.context)
        self.assertEqual(response.context['ads'].count(), 1)
        self.assertQuerysetEqual(
            response.context['ads'],
            [self.class_ad],
            transform=lambda x: x,
            ordered=False
        )

    def test_response_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)