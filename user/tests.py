from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class UserTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.test_user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.create_url = reverse('user-list')

    def test_create_user(self):
        """
        Ensure we can create a new user.
        """
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword',
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username='newuser').email, 'new@example.com')

    def test_get_users(self):
        """
        Ensure we can retrieve users.
        """
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class UserMyViewTests(APITestCase):
    def test_retrieve_my_info(self):
        """
        Ensure we can retrieve the current user's info.
        """
        # Here, you'd need to authenticate the request
        self.client.force_authenticate(user=self.test_user)
        url = reverse('user-my')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], self.test_user.username)
