from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import JobAd, SaleAd
from ..forms import JobAdForm, SaleAdForm

class AdUpdateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.ad1 = JobAd.objects.create(title='Ad1', description='Desc1', tags='ad1', category='IN',email='test@gmail.com', phone='1234567890', location='location', postal_code='123456', owner=self.user, salary="1234")
        self.ad2 = SaleAd.objects.create(title='Ad2', description='Desc2', tags='ad2', category='GR', price='100',owner=self.user)
        self.client.login(username='testuser', password='12345')
    
    def test_get_model_valid(self):
        response = self.client.get(reverse('ad:ad_update', kwargs={'adtype': 'job', 'pk': self.ad1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ad'], self.ad1)

    def test_get_model_invalid(self):
        response = self.client.get(reverse('ad:ad_update', kwargs={'adtype': 'invalidtype', 'pk': 1}))
        self.assertEqual(response.status_code, 404)

    def test_get_form_class_valid(self):
        response = self.client.get(reverse('ad:ad_update', kwargs={'adtype': 'job', 'pk': self.ad1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], JobAdForm)

    def test_get_queryset(self):
        response = self.client.get(reverse('ad:ad_update', kwargs={'adtype': 'job', 'pk': self.ad1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ad'], self.ad1)
    
    def test_login_required(self):
        self.client.logout()
        response = self.client.get(reverse('ad:ad_update', kwargs={'adtype': 'job', 'pk': self.ad1.pk}))
        self.assertRedirects(response, f'/accounts/login/?next=/ad/update/adtype1/{self.ad1.pk}/')
