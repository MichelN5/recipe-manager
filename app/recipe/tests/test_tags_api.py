from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from core.models import Tag
from recipe.serializers import  TagSerializer
from rest_framework.test import APIClient

TAGS_URL= reverse('recipe:tag-list')

class PublicApiTagTests(TestCase):
    def setUp(self):
        self.client= APIClient()
    
    def test_login_required(self):
        res= self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
class PrvtApiTagTests(TestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(email= 'naous@gmail.com', password= 'Mn102938')
        self.client= APIClient()
        self.client.force_authenticate(self.user)

    def test_get_tags(self):
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')
        res= self.client.get(TAGS_URL)
        tags= Tag.objects.all().order_by('-name')
        serializer= TagSerializer(tags, many= True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    

    def test_tags_connected_to_user(self):
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        res  = self.client.post(TAGS_URL, {'name':'Test Name'})
        exists= Tag.objects.filter(
            user= self.user, 
            name="Test Name"
        ).exists()

        self.assertTrue(exists)
    
    def test_create_invalid(self):
        res  = self.client.post(TAGS_URL, {'name':''})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



