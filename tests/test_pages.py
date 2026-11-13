from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PublicPageTests(TestCase):
    def test_home_page_is_accessible_to_visitors(self):
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get(reverse('account:user_login'))
        self.assertEqual(response.status_code, 200)

    def test_registration_page(self):
        response = self.client.get(reverse('account:user_register'))
        self.assertEqual(response.status_code, 200)

    def test_chat_requires_login(self):
        response = self.client.get(reverse('chat:first'))
        self.assertEqual(response.status_code, 302)


class AuthenticatedPageTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', email='testuser@example.invalid', password='test-password-only'
        )
        self.client.force_login(self.user)

    def test_home_page(self):
        self.assertEqual(self.client.get(reverse('home:home')).status_code, 200)

    def test_chat_index(self):
        self.assertEqual(self.client.get(reverse('chat:first')).status_code, 200)

    def test_chat_room(self):
        self.assertEqual(self.client.get(reverse('chat:room', args=['demo_room'])).status_code, 200)
