from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import JobAd, RentalAd, SaleAd, ServiceAd, EventAd, ClassAd
import datetime

class AdListViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        
        self.other_user = User.objects.create_user(username='otheruser', password='54321')
        
        self.job_ad = JobAd.objects.create(
            title='Test Job Ad',
            category='FT',
            description='Job description',
            tags='job',
            email='test@example.com',
            phone='1234567890',
            location='Test Location',
            postal_code='12345',
            salary=50000,
            owner=self.user,
        )
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
        self.sale_ad = SaleAd.objects.create(
            title='Test Sale Ad',
            category='FU',
            description='Sale description',
            tags='sale',
            price=50000,
            owner=self.user,
        )
        self.service_ad = ServiceAd.objects.create(
            pk=1,
            title='Test Service Ad',
            category='LE',
            description='Job description',
            tags='job',
            email='test@example.com',
            phone='1234567890',
            price=50000,
            owner=self.user,
        )
        self.event_ad = EventAd.objects.create(
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
            owner=self.user,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now(),
        )
        self.class_ad = ClassAd.objects.create(
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
            owner=self.user,
        )
        self.other_job_ad = JobAd.objects.create(
            title='Test Job Ad 2',
            category='FT',
            description='Job description 2',
            tags='job1',
            email='test@example.com',
            phone='1234567890',
            location='Test Location',
            postal_code='12345',
            salary=50000,
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

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('ad:ad_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template_used(self):
        response = self.client.get(reverse('ad:ad_list'))
        self.assertTemplateUsed(response, 'ad/ad_list.html')
    
    def test_ads_context_data(self):
        response = self.client.get(reverse('ad:ad_list'))
        
        self.assertIn(self.job_ad, response.context['jobs'])
        self.assertIn(self.other_job_ad, response.context['jobs'])
        
        self.assertIn(self.rental_ad, response.context['rentals'])
        self.assertIn(self.other_rental_ad, response.context['rentals'])
        
        self.assertIn(self.sale_ad, response.context['sales'])
        self.assertIn(self.service_ad, response.context['services'])
        self.assertIn(self.event_ad, response.context['events'])
        self.assertIn(self.class_ad, response.context['classes'])

    def test_redirection_for_anonymous_user(self):
        self.client.logout()
        response = self.client.get(reverse('ad:ad_list'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("ad:ad_list")}')
