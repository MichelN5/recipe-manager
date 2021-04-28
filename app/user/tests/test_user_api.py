from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse     
from django.contrib.auth import get_user_model

CU_url = reverse('user:create')
token_url= reverse('user:token')
ME_URL= reverse('user:me')
def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client= APIClient()
        
    def test_create_valid_user(self):
        payload= {
            'email': 'naoussmichel20005@gmail.com',
            'password': 'test1212',
            'name': 'Michel'
        }

        res= self.client.post(CU_url ,payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user= get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'hello1232',
            'name': 'Test',
        }
        create_user(**payload)
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
        self.assertFalse(exists)

    def test_create_token_user(self):
        payload = {'email': 'test@londonappdev.com','password': 'hello1232','name': 'Test'}
        create_user(**payload)
        res= self.client.post( token_url, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@londonappdev.com', password='testpass')
        payload = {'email': 'test@londonappdev.com', 'password': 'wrong'}
        res = self.client.post(token_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_token_no_user(self):
        payload = {'email': 'test@londonappdev.com','password': 'hello1232','name': 'Test'}
        res= self.client.post( token_url, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_missing_field(self):
        payload = {'email': 'test@londonappdev.com','password': '', 'name' :'mich' }
        res= self.client.post( token_url, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retreive_unauthorized(self):
        res= self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email='test@londonappdev.com',
            password='testpass',
            name='fname',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retreive_profile(self):
        res= self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_unallowed_me(self):
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_info(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'new name', 'password': 'newpass1212'}

        res = self.client.patch(ME_URL, payload)
        
        self.user.refresh_from_db()
        print(self.user.password)
        self.assertEqual(self.user.name, payload['name'])
        print(payload['password'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    







        
        



        
