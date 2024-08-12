from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from ..models import JobAd

class AdDeleteViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.ad1 = JobAd.objects.create(
            category='Category1',
            title='Ad1',
            image='image.jpg',
            tags='tag1,tag2',
            location='Location1',
            postal_code='12345',
            description='Description1',
            salary='50000',
            email='user@example.com',
            show_email=True,
            phone='1234567890',
            show_phone=True,
            owner=self.user
        )

    def test_successful_deletion(self):
        response = self.client.post(reverse('ad:ad_delete', kwargs={'adtype': 'job', 'pk': self.ad1.pk}))
        self.assertFalse(JobAd.objects.filter(pk=self.ad1.pk).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('ad:ad_list'))

    def test_deletion_without_login(self):
        self.client.logout()
        response = self.client.post(reverse('ad:ad_delete', kwargs={'adtype': 'job', 'pk': self.ad1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("ad:ad_delete", kwargs={"adtype": "job", "pk": self.ad1.pk})}')
        self.assertTrue(JobAd.objects.filter(pk=self.ad1.pk).exists())
    
    def test_delete_non_existent_ad(self):
        response = self.client.post(reverse('ad:ad_delete', kwargs={'adtype': 'job', 'pk': 9999}))
        self.assertEqual(response.status_code, 404)
