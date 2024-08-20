from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from ..models import Message, JobAd
from ..forms import MessageForm

class EditCommentViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.other_user = User.objects.create_user(username='otheruser', password='12345')

        self.ad = JobAd.objects.create(
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

        self.content_type = ContentType.objects.get_for_model(self.ad)
        self.comment = Message.objects.create(
            user=self.user,
            ad=self.ad,
            content_type=self.content_type,
            object_id=self.ad.id,
            message='Original comment'
        )

        self.url = reverse('ad:edit_comment', kwargs={'adtype': 'job', 'pk': self.comment.pk})

    def test_edit_comment_access(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comment/edit_comment.html')
        self.client.login(username='otheruser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_edit_comment_form_submission(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.url, {
            'message': 'Updated comment'
        })
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.message, 'Updated comment')
        self.assertRedirects(response, reverse('ad:ad_detail', kwargs={'adtype': 'job', 'pk': self.ad.pk}))

    def test_non_owner_cannot_edit_comment(self):
        self.client.login(username='otheruser', password='12345')
        response = self.client.post(self.url, {
            'message': 'Updated comment by non-owner'
        })
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.message, 'Original comment')
        self.assertEqual(response.status_code, 403) 
    
    def test_owner_can_edit_comment(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.url, {
            'message': 'Updated comment by non-owner'
        })
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.message, 'Updated comment by non-owner')
        self.assertEqual(response.status_code, 302) 

class DeleteCommentViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.other_user = User.objects.create_user(username='otheruser', password='12345')

        self.ad = JobAd.objects.create(
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

        self.content_type = ContentType.objects.get_for_model(self.ad)
        self.comment = Message.objects.create(
            user=self.user,
            ad=self.ad,
            content_type=self.content_type,
            object_id=self.ad.id,
            message='Comment to be deleted'
        )

        self.url = reverse('ad:delete_comment', kwargs={'adtype': 'job', 'adpk':self.ad.pk, 'pk': self.comment.pk})

    def test_delete_comment_access(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comment/delete_comment.html')
        self.client.login(username='otheruser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_successful_comment_deletion(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.url)
        with self.assertRaises(Message.DoesNotExist):
            Message.objects.get(pk=self.comment.pk)
        self.assertRedirects(response, reverse('ad:ad_detail', kwargs={'adtype': 'job', 'pk': self.ad.pk}))

    def test_non_owner_cannot_delete_comment(self):
        self.client.login(username='otheruser', password='12345')
        response = self.client.post(self.url)
        self.assertTrue(Message.objects.filter(pk=self.comment.pk).exists())
        self.assertEqual(response.status_code, 403)
