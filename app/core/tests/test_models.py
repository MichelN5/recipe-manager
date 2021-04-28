from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(email='naous@gmail.com', password='test1tttdj'):
    return get_user_model().objects.create_user(email,password)

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
    
    def test_str_tag(self):
        tag= models.Tag.objects.create(
            user= sample_user(),
            name="recipe"
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)