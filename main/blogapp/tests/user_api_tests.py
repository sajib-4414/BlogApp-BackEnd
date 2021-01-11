from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
User = get_user_model()


def get_authenticated_client():
    client = APIClient()
    request_body = get_user_creation_body_params()
    response = client.post('/users/', request_body, format='json')
    response_user = response.data
    assert response_user["user_id"] == 2
    user = User.objects.get(username = "testusername")
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client


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

    def test_update_user_fail_unauthorized_case(self):
        request_body = get_user_creation_body_params()
        client = APIClient()
        response = client.post('/users/', request_body, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_created = response.data
        payload_test = {
            "username": "abc"
        }
        response2 = client.put('/users/'+str(user_created["user_id"])+"/",payload_test)
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_fail_readonly_params_case(self):

        client = get_authenticated_client()
        payload_test = {
            "username": "abc"
        }
        response2 = client.put('/users/2/',payload_test) # I tested the userid will be 2
        response_user = response2.data
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response_user["username"],"abc") # username is readonly and will not update


def get_user_creation_body_params():
    return {
            'username': 'testusername',
            'email': 'a@a.com',
            'password':'12345678',
            'first_name':'test first name',
            'last_name': 'test last name'
        }
