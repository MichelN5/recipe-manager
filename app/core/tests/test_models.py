from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = 'naoussmichel20005@gmail.com'
        password= 'Mn102938'
        user= get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(email , user.email)
        self.assertTrue(user.check_password(password))

    def test_email_normalized(self):
        email= 'naoussmichel20005@GMAIL.COM'
        user= get_user_model().objects.create_user(
            email=email,
            password="Mn102938"
        )

        self.assertEqual(email.lower(), user.email)

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("","testjdksjdkj")

    def test_create_superuser(self):
        user= get_user_model().objects.create_superuser(
            'naoussmichel20005@gmail.com',
            'Mn102938'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        