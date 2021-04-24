from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse     
from django.contrib.auth import get_user_model

CU_url = reverse('user:create')
def create_user(**params):
    get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client= APIClient
    def test_create_valid_user(self):
        payload= {
            'email': 'test@gmail.com',
            'password': 'test1212',
            'name': 'aboemak'
        }

        res= self.client.post(CU_url ,payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user= get_user_model().objects.get(**res.data)
        self.assertEqual(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        payload= {
            'email': 'naoussmichel20005@gmail.com',
            'password': 'test1212',
            'name': 'aboemak'
        }
        res= self.client.post(CU_url ,payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_pass(self):
        payload= {
            'email': 'naoussmichel20005@gmail.com',
            'password': 'te',
            'name': 'aboemak'
        }
        res= self.client.post(CU_url ,payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        exists= get_user_model().objects.filter(
            email= payload['email']
        ).exists()
        self.assertFalse(user_exists)
        



        
