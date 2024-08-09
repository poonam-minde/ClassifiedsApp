from django.test import TestCase
from django.urls import reverse
from ..models import JobAd, SaleAd, RentalAd, ServiceAd, EventAd, ClassAd
from django.contrib.auth.models import User
import datetime

class JobAdDetailViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')

        cls.job_ad = JobAd.objects.create(
            title='Test Job Ad',
            category='FT',
            description='Job description',
            tags='job',
            email='test@example.com',
            phone='1234567890',
            location='Test Location',
            postal_code='12345',
            salary=50000,
            owner=cls.user,
        )

    def setUp(self):
        self.client.login(username='testuser', password='password')

    def test_job_ad_detail_view(self):
        response = self.client.get(reverse('ad:ad_detail', kwargs={'adtype': 'job', 'pk': self.job_ad.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ad/ad_detail.html')
        self.assertContains(response, self.job_ad.title)
        self.assertContains(response, self.job_ad.description)
    
    def test_sale_ad_detail_view_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('ad:ad_detail', kwargs={'adtype': 'job', 'pk': self.job_ad.pk}))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('ad:ad_detail', kwargs={'adtype': 'job', 'pk': self.sale_ad.pk})}")

    def test_sale_ad_detail_view_404_error(self):
        non_existent_pk = self.job_ad.pk + 1
        response = self.client.get(reverse('ad:ad_detail', kwargs={'adtype': 'job', 'pk': non_existent_pk}))
        self.assertEqual(response.status_code, 404)

class SaleAdDetailViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')

        cls.sale_ad = SaleAd.objects.create(
            title='Test Sale Ad',
            category='FU',
            description='Sale description',
            tags='sale',
            price=50000,
            owner=cls.user,
        )

    def setUp(self):
        self.client.login(username='testuser', password='password')

    def test_sale_ad_detail_view(self):
        response = self.client.get(reverse('ad:ad_detail', kwargs={'adtype': 'sale', 'pk': self.sale_ad.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ad/ad_detail.html')
        self.assertContains(response, self.sale_ad.title)
        self.assertContains(response, self.sale_ad.description)
    
    def test_sale_ad_detail_view_404_error(self):
        non_existent_pk = self.sale_ad.pk + 1
        response = self.client.get(reverse('ad:ad_detail', kwargs={'adtype': 'sale', 'pk': non_existent_pk}))
        self.assertEqual(response.status_code, 404)

class RentalAdDetailViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')

        cls.rental_ad = RentalAd.objects.create(
            title='Test Rental Ad',
            category='FT',
            description='Rental description',
            tags='rental',
            email='test@example.com',
            phone='1234567890',
            charge=50000,
            period='MO',
            owner=cls.user,
        )

    def setUp(self):
        self.client.login(username='testuser', password='password')

    def test_rental_ad_detail_view(self):
        response = self.client.get(reverse('ad:ad_detail', kwargs={'adtype': 'rental', 'pk': self.rental_ad.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ad/ad_detail.html')
        self.assertContains(response, self.rental_ad.title)
        self.assertContains(response, self.rental_ad.description)

    def test_sale_ad_detail_view_404_error(self):
        non_existent_pk = self.rental_ad.pk + 1
        response = self.client.get(reverse('ad:ad_detail', kwargs={'adtype': 'rental', 'pk': non_existent_pk}))
        self.assertEqual(response.status_code, 404)

class ServiceAdDetailViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')

        cls.service_ad = ServiceAd.objects.create(
            pk=1,
            title='Test Service Ad',
            category='LE',
            description='Job description',
            tags='job',
            email='test@example.com',
            phone='1234567890',
            price=50000,
            owner=cls.user,
        )

    def setUp(self):
        self.client.login(username='testuser', password='password')

    def test_job_ad_detail_view(self):
        response = self.client.get(reverse('ad:ad_detail', kwargs={'adtype': 'service', 'pk': self.service_ad.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ad/ad_detail.html')
        self.assertContains(response, self.service_ad.title)
        self.assertContains(response, self.service_ad.description)

    def test_sale_ad_detail_view_404_error(self):
        non_existent_pk = self.service_ad.pk + 1
        response = self.client.get(reverse('ad:ad_detail', kwargs={'adtype': 'service', 'pk': non_existent_pk}))
        self.assertEqual(response.status_code, 404)

class EventAdDetailViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')

        cls.event_ad = EventAd.objects.create(
            pk=4,
            title='Test Event Ad',
            category='SE',
            description='Event description',
            tags='event',
            email='test@example.com',
            phone='1234567890',
            location='Test Location',
            postal_code='12345',
            price=50000,
            owner=cls.user,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now(),
        )

    def setUp(self):
        self.client.login(username='testuser', password='password')

    def test_job_ad_detail_view(self):
        response = self.client.get(reverse('ad:ad_detail', kwargs={'adtype': 'event', 'pk': self.event_ad.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ad/ad_detail.html')
        self.assertContains(response, self.event_ad.title)
        self.assertContains(response, self.event_ad.description)
    
    def test_sale_ad_detail_view_404_error(self):
        non_existent_pk = self.event_ad.pk + 1
        response = self.client.get(reverse('ad:ad_detail', kwargs={'adtype': 'event', 'pk': non_existent_pk}))
        self.assertEqual(response.status_code, 404)

class ClassAdDetailViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')

        cls.class_ad = ClassAd.objects.create(
            pk=1,
            title='Test Class Ad',
            category='WO',
            description='Class description',
            tags='class',
            email='test@example.com',
            phone='1234567890',
            location='Test Location',
            postal_code='12345',
            fees=50000,
            owner=cls.user,
        )

    def setUp(self):
        self.client.login(username='testuser', password='password')

    def test_job_ad_detail_view(self):
        response = self.client.get(reverse('ad:ad_detail', kwargs={'adtype': 'class', 'pk': self.class_ad.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ad/ad_detail.html')
        self.assertContains(response, self.class_ad.title)
        self.assertContains(response, self.class_ad.description)

    def test_sale_ad_detail_view_404_error(self):
        non_existent_pk = self.class_ad.pk + 1
        response = self.client.get(reverse('ad:ad_detail', kwargs={'adtype': 'class', 'pk': non_existent_pk}))
        self.assertEqual(response.status_code, 404)