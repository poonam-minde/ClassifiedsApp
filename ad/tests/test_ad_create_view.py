from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import JobAd, AdImage
from ..views import AdImagesMixin

User = get_user_model()

class AdImagesMixinTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.ad_url = reverse('ad:create_ad', kwargs={'adtype': 'job'})  # Adjust to your URL name
        self.factory = RequestFactory()
        self.mixin=AdImagesMixin()
        self.mixin.request = self.factory.get('/')

    def test_get_formset(self):
        formset = self.mixin.get_formset(AdImage.objects.none())
        self.assertTrue(hasattr(formset, 'forms')) 

        self.assertEqual(formset.model, AdImage)

        self.assertEqual(formset.total_form_count(), 4)
        self.assertEqual(formset.can_delete, True) 

    def test_get_context_data(self):
        response = self.client.get(self.ad_url)
        self.assertIn('formset', response.context)

    def test_form_valid_with_valid_data(self):
        form_data = {'title':'Test Job Ad',
            'category':'FT',
            'description':'Job description',
            'tags':'job',
            'email':'test@example.com',
            'phone':'1234567890',
            'location':'Test Location',
            'postal_code':'12345',
            'salary':50000,
            'owner':self.user,
        }
        image_data = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('static/img/job/image.jpg', 'rb').read(),
            content_type='image/*'
        )
        form_files = {
            'form-0-image': image_data,
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '4',
        }

        response = self.client.post(self.ad_url, data=form_data, files=form_files)

        self.assertFalse(AdImage.objects.exists())
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, '/ad/')
        self.assertTrue(JobAd.objects.filter(title='Test Job Ad').exists())
