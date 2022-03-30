from audioop import reverse
import email
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')

def create_user (**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payLoad = {
            'email':'user@test.com',
            'password' :'Someuserpassword55',
            'name':'Test user full name'
        }
        res = self.client.post(CREATE_USER_URL, payLoad)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payLoad['password']))
        self.assertNotIn('password', res.data)
    
    def test_user_exist(self):
        payLoad = {'email':'user@test.com','password' :'Someuserpassword55'}
        create_user(**payLoad)
        res = self.client.post(CREATE_USER_URL, payLoad)

    def test_password_too_short(self):
        payLoad = {'email':'user@test.com','password' :'55'}
        res = self.client.post(CREATE_USER_URL, payLoad)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email = payLoad['email']
        ).exists()
        self.assertFalse(user_exist)


