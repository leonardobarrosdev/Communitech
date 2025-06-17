import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient


User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestRegisterAPIView:
    def test_user_register_success(self, api_client):
        url = reverse('user:register')
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'user' in response.data
        assert 'token' in response.data
        assert User.objects.filter(email='test@example.com').exists()

    def test_user_register_invalid_data(self, api_client):
        url = reverse('user:register')
        data = {
            'email': 'invalid_email',
            'password': 'short',
            'password2': 'not_matching'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_user_register_duplicate_email(self, api_client):
        User.objects.create_user(email='existing@example.com', password='testpass123')
        url = reverse('user:register')
        data = {
            'email': 'existing@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
