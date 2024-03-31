from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import timedelta
from .models import Activity, Comment


# Create your tests here
class ActivityViewsTestCase(TestCase):
    def setUp(self):
        """
        Create a superuser for testing
        Create activities for testing
        Create comments for testing
        """
        self.user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='admin')
        self.activity1 = Activity.objects.create(
            name='Activity 1', slug='activity-1', description='Description 1',
            duration=timedelta(minutes=60), status=1)
        self.activity2 = Activity.objects.create(
            name='Activity 2', slug='activity-2', description='Description 2',
            duration=timedelta(minutes=90), status=1)
        self.comment1 = Comment.objects.create(
            activity=self.activity1, body='Comment 1', user=self.user)
        self.comment2 = Comment.objects.create(
            activity=self.activity1, body='Comment 2', user=self.user)
        self.comment3 = Comment.objects.create(
            activity=self.activity2, body='Comment 3', user=self.user)

    def test_activity_comment_view(self):
        """
        Test GET request to activity_comment view
        Test POST request to activity_comment view
        """
        client = Client()
        response = client.get(reverse(
            'activity_detail', args=[self.activity1.slug]))
        self.assertEqual(response.status_code, 302)
        response = client.post(reverse(
            'activity_detail', args=[self.activity1.slug]),
            {'body': 'Test Comment'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_comment_edit_view(self):
        """
        Test GET request to comment_edit view
        Test POST request to comment_edit view
        """
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse(
            'comment_edit', args=[self.activity1.slug, self.comment1.pk]))
        self.assertEqual(response.status_code, 200)
        response = client.post(reverse(
            'comment_edit', args=[self.activity1.slug, self.comment1.pk]),
            {'body': 'Updated Comment'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Comment Updated!')

    def test_comment_delete_view(self):
        """
        Test GET request to comment_delete view
        Test POST request to comment_delete view
        """
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse(
            'comment_delete', args=[self.activity1.slug, self.comment1.pk]))
        self.assertEqual(response.status_code, 302)
        response = client.post(reverse(
            'comment_delete', args=[self.activity1.slug, self.comment2.pk]),
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Comment 2 deleted!')
