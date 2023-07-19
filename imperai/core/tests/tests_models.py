from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Profile
import os

test_user_email = os.environ.get('TEST_EMAIL')
test_user_password = os.environ.get('TEST_PASSWORD')

class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email=test_user_email, password=test_user_password)
        self.assertEqual(user.email, test_user_email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password=test_user_password)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(test_user_email, password=test_user_password)
        self.assertEqual(admin_user.email, test_user_email)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertIsNone(admin_user.username)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=test_user_email,
                password=test_user_password,
                is_superuser=False,
            )

    
    def test_create_superuser_without_email(self):
        with self.assertRaises(ValueError) as cm:
            User = get_user_model()
            User.objects.create_superuser(
                email="",
                password=test_user_password
            )
        self.assertEqual(str(cm.exception), "An email must be provided.")

    def test_create_superuser_without_staff_flag(self):
        with self.assertRaises(ValueError) as cm:
            User = get_user_model()
            User.objects.create_superuser(
                email=test_user_email,
                password=test_user_password,
                is_staff=False
            )
        self.assertEqual(str(cm.exception), "Superusers must have is_staff=True.")

    def test_attribute_error(self):
        try:
            raise AttributeError("AttributeError raised")
        except AttributeError:
            pass

class CustomUsersTests(TestCase):
    def test_custom_user_str(self):
        instance = get_user_model().objects.create_user(
            email=test_user_email,
            password=test_user_password,
        )
        self.assertEqual(str(instance), instance.email)


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email=test_user_email,
            password=test_user_password
        )
        profile = Profile.objects.get(user=self.user)
        profile.location = 'Test Location'
        profile.title = 'Test Title'
        self.profile = profile

    def test_profile_str_method(self):
        expected_str = str(self.user.email)
        self.assertEqual(expected_str, str(self.profile))

    def test_profile_location_field(self):
        expected_location = 'Test Location'
        self.assertEqual(expected_location, self.profile.location)

    def test_profile_title_field(self):
        expected_title = 'Test Title'
        self.assertEqual(expected_title, self.profile.title)

    def test_profile_user_field(self):
        user = get_user_model().objects.get(id=self.user.id)
        self.assertEqual(user, self.profile.user)

    def test_create_profile(self):
        user = self.user
        profile = self.profile
        self.assertEqual(user, profile.user)
        self.assertEqual(profile.location, 'Test Location')
        self.assertEqual(profile.title, 'Test Title')