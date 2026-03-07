"""Tests for Event Management application."""

# pylint: disable=no-member

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from events.models import Event, Participant


class EventModelTest(TestCase):
    """Test cases for Event model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        self.event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            date=timezone.now(),
            location="Test Location",
            user=self.user,
            max_participants=10
        )

    def test_event_creation(self):
        """Test event creation."""
        self.assertEqual(self.event.title, "Test Event")
        self.assertEqual(self.event.location, "Test Location")

    def test_event_string(self):
        """Test event string representation."""
        self.assertEqual(str(self.event), "Test Event")


class ParticipantModelTest(TestCase):
    """Test cases for Participant model."""

    def test_participant_creation(self):
        """Test participant creation."""
        participant = Participant.objects.create(
            name="John Doe",
            email="john@example.com"
        )

        self.assertEqual(participant.name, "John Doe")
        self.assertEqual(str(participant), "John Doe")


class EventViewTest(TestCase):
    """Test cases for event views."""

    def setUp(self):
        """Set up client and test data."""
        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        self.event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            date=timezone.now(),
            location="Test Location",
            user=self.user,
            max_participants=10
        )

    def test_events_page(self):
        """Test events list page."""
        response = self.client.get(reverse("events"))
        self.assertEqual(response.status_code, 200)

    def test_event_detail_page(self):
        """Test viewing a single event."""
        response = self.client.get(reverse("view_events", args=[self.event.id]))
        self.assertEqual(response.status_code, 200)


class AuthenticationTest(TestCase):
    """Test authentication views."""

    def setUp(self):
        """Create test client and user."""
        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

    def test_register_view(self):
        """Test user registration."""
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
            },
        )

        self.assertEqual(response.status_code, 302)

    def test_login_view(self):
        """Test login functionality."""
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "password123",
            },
        )

        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        """Test logout functionality."""
        self.client.login(username="testuser", password="password123")

        response = self.client.get(reverse("logout"))

        self.assertEqual(response.status_code, 302)
        