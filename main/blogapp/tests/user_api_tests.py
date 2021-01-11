from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class UserCreationAPITests(TestCase):
    def test_create_user_without_required_params(self):
        request_body = {
            'username': 'testusername',
            'email': 'a@a.com'
        }
        client = APIClient()
        response = client.post('/users/', request_body, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_success_case(self):
        request_body = get_user_creation_body_params()
        client = APIClient()
        response = client.post('/users/', request_body, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_same_username(self):
        request_body = ()
        client = APIClient()
        response = client.post('/users/', request_body, format='json')
        response2 = client.post('/users/', request_body, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)


def get_user_creation_body_params():
    return {
            'username': 'testusername',
            'email': 'a@a.com',
            'password':'12345678',
            'first_name':'test first name',
            'last_name': 'test last name'
        }
