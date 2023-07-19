from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from core.views import WelcomeView
from core.models import Profile
import os

test_user_email = os.environ.get('TEST_EMAIL')
test_user_password = os.environ.get('TEST_PASSWORD')

class WelcomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.url = reverse('welcome')
        self.user = get_user_model().objects.create_user(
            email=test_user_email,
            password=test_user_password,
        )

    def test_view_url_exists_at_intended_location(self):
        self.client.login(email=test_user_email, password=test_user_password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_correct_template(self):
        self.client.login(email=test_user_email, password=test_user_password)    
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'welcome.html')
    
    def test_view_requires_login_for_anon(self):
        request = self.factory.get('welcome')
        request.user = AnonymousUser()
        response = WelcomeView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_view_for_authd_user(self):
        request = self.factory.get('welcome')
        request.user = self.user
        response = WelcomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class ProfileUpdateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            email=test_user_email,
            password=test_user_password,
        )
        profile = Profile.objects.get(user=self.user)
        profile.location = 'Test Location'
        profile.title = 'Test Title'
        self.profile = profile
        self.url = reverse('profile_update', kwargs={'pk': self.profile.id})

    def test_view_requires_login_for_anon(self):
        self.client.user = AnonymousUser()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_view_for_authd_user(self):
        request = self.factory.get(self.url)
        request.user = self.user
        response = WelcomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_intended_location(self):
        self.client.login(email=test_user_email, password=test_user_password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email=test_user_email, password=test_user_password)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'profile_update.html')

    def test_view_updates_user_profile(self):
        self.client.login(email=test_user_email, password=test_user_password)
        data = {
            'location': 'New Location',
            'title': 'New Title'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/profile')
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.location, 'New Location')
        self.assertEqual(self.profile.title, 'New Title')

class CustomUserUpdateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            email=test_user_email,
            password=test_user_password,
        )
        self.url = reverse('user_update', kwargs={'pk': self.user.id})

    def test_view_requires_login_for_anon(self):
        self.client.user = AnonymousUser()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_intended_location(self):
        self.client.login(email=test_user_email, password=test_user_password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email=test_user_email, password=test_user_password)
        respose = self.client.get(self.url)
        self.assertTemplateUsed(respose, 'user_update.html')