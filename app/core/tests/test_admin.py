from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.super_user= get_user_model().objects.create_superuser(
            email = 'naouss@gmail.com',
            password= 'test1029'
        )
        self.client.force_login(self.super_user)

        self.user= get_user_model().objects.create_user(
            email= 'naoussmichel20005@gmail.com',
            password= 'Mn102938',
            name= "Michel"
        )
    def test_users_listed(self):
        url= reverse('admin:core_user')
        res= self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)