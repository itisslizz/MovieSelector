from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

# Include an appropriate `Authorization:` header on all requests.

from movieselector.models import *

# Create your tests here.


#Model tests

class SelectionTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="testuser", password="test")
        user = User.objects.get(username="testuser")
        Selection.objects.create(owner = user)

    def test_selection_is_created(self):
        """The Selection is created with the default values"""
        user = User.objects.get(username="testuser")
        selection = Selection.objects.get(owner = user)
        self.assertEqual(selection.owner, user)
        self.assertEqual(selection.in_round, 0)
        self.assertEqual(selection.max_movies_per_user, 3)
        self.assertEqual(selection.has_winner, False)


# Token tests

class RegisterTestCase(TestCase):
    def setUp(self):
        client = APIClient()
        client.post('/users/register/', {'username': 'testuser', 'password': 'test'}, format='json')


    def test_register_user(self):
        user = User.objects.get(username="testuser")


class RetrieveTokenTestCase(TestCase):
    def setUp(self):
        client = APIClient()
        client.post('/users/register/', {'username': 'testuser', 'password': 'test'}, format='json')

    def test_retrieve_token(self):
        client = APIClient()
        response = client.post('/api-token-auth/', {'username': 'testuser', 'password': 'test'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


# SelectionTestCase

class CreateSelectionTestCase(TestCase):
    def setUp(self):
        client = APIClient()
        client.post('/users/register/', {'username': 'testuser', 'password': 'test'}, format='json')

    def test_create_selection(self):
        token = Token.objects.get(user__username='testuser')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post('/selections/')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
