from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import TimeAvailable, Booking
from training.models import Activity
from datetime import datetime, timedelta

User = get_user_model()
"""
Defines a variable `User` to hold the user model
retrieved using `get_user_model()`
"""


class BookingTestCase(TestCase):
    def setUp(self):
        """
        Set up necessary data for each test case.
        Create a test activity
        Create a test time slot available for booking
        Create a test user
        Login the test user
        """
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.activity = Activity.objects.create(
            name='Test Activity', max_capacity=10, duration=timedelta(hours=1))
        self.time_available = TimeAvailable.objects.create(
            activity=self.activity, day=datetime.now().date(),
            time=datetime.now().time())
        self.booking = Booking.objects.create(
            user=self.user, time_available=self.time_available)

    def test_booking_list_view(self):
        """
        Test case for retrieving the list of available time slots for booking.
        Make a GET request to retrieve the list of available time slots
        Assert that the response status code is 200 (success)
        """
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('booking'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking.html')

    def test_booking_post(self):
        """
        Test case for posting a booking.
        Make a POST request to book a class with valid form data
        Assert that the response status code is 200 (success)
        """
        client = Client()
        client.force_login(self.user)
        response = client.post(reverse('booking'), {
            'selected_class_id': self.time_available.pk}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('booking'))

    def test_book_class(self):
        """
        Test case for booking a class.
        Make a POST request to book a class
        Assert that the response status code is 200 (success)
        """
        client = Client()
        client.force_login(self.user)
        response = client.post(reverse('book_class'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('booking'))

    def test_cancel_booking(self):
        """
        Test case for canceling a booking.
        Create a booking for the test user
        Make a POST request to cancel the booking
        Assert that the response status code is 200 (success)
        Assert that the booking is deleted from the database
        """
        client = Client()
        client.force_login(self.user)
        response = client.post(reverse(
            'cancel_booking', args=[self.booking.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('booking'))
        self.assertFalse(Booking.objects.filter(pk=self.booking.pk).exists())

    def test_cancel_booking_unauthorized(self):
        """
        Test case for attempting to cancel a booking by an unauthorized user.
        Make a POST request to cancel the booking
        Assert that the response status code is 200 (success)
        Assert that the booking is not deleted from the database
        """
        unauthorized_user = User.objects.create_user(
            username='unauthorized', password='testpassword')
        client = Client()
        client.force_login(unauthorized_user)
        response = client.post(
            reverse('cancel_booking', args=[self.booking.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Booking.objects.filter(pk=self.booking.pk).exists())
