from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import JobAd, SaleAd, RentalAd, ServiceAd, EventAd, ClassAd, AdImage
import datetime
from django.contrib.contenttypes.models import ContentType

class BaseListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('ad:sale_list') 

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'ad/adtype_list.html')

    def test_view_context_object_name(self):
        response = self.client.get(self.url)
        self.assertIn('ads', response.context)

class JobListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.url = reverse('ad:job_list')
        self.ad_content_type = ContentType.objects.get_for_model(JobAd)
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
        self.image1 = AdImage.objects.create(
            ad=self.job_ad1,
            image='images/image1.jpg',
            content_type=self.ad_content_type,
            object_id=self.job_ad1.id
        )
        self.image2 = AdImage.objects.create(
            ad=self.job_ad2,
            image='images/image2.jpg',
            content_type=self.ad_content_type,
            object_id=self.job_ad2.id
        )

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
        self.assertIn('images_dict', response.context)
        images_dict = response.context['images_dict']
        self.assertEqual(images_dict.get(self.job_ad1.id), self.image1)
        self.assertEqual(images_dict.get(self.job_ad2.id), self.image2)
        non_existent_ad_id = 999
        self.assertIsNone(images_dict.get(non_existent_ad_id))

    def test_response_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

class SaleListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.url = reverse('ad:sale_list')
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
        self.url = reverse('ad:rental_list')
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
        self.url = reverse('ad:service_list')
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
        self.url = reverse('ad:event_list')
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
        self.url = reverse('ad:class_list')
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