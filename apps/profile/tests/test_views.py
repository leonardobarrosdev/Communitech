import pytest
from knox.models import AuthToken
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.profile.models import Profile


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestRegisterAPIView:
    def test_profile_register_success(self, api_client):
        url = reverse("profile:register")
        data = {
            "first_name": "Test",
            "last_name": "Profile",
            "email": "test@example.com",
            "password": "testpass123",
            "password2": "testpass123",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert "user" in response.data
        assert "token" in response.data
        assert Profile.objects.filter(email="test@example.com").exists()

    def test_profile_register_invalid_data(self, api_client):
        url = reverse("profile:register")
        data = {
            "email": "invalid_email",
            "password": "short",
            "password2": "not_matching",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_profile_register_duplicate_email(self, api_client):
        Profile.objects.create_user(
            email="existing@example.com", password="testpass123"
        )
        url = reverse("profile:register")
        data = {
            "email": "existing@example.com",
            "password": "testpass123",
            "password2": "testpass123",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUpdateProfileAPIView:
    def setup_method(self):
        self.profile = Profile.objects.create_user(
            first_name="Test",
            email="test@company.com",
            password="StringPass123"
        )
        self.api_client = APIClient()
        _, token = AuthToken.objects.create(self.profile)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        self.url = reverse("profile:update", kwargs={"id": self.profile.id})
        self.data = {"first_name": "Johny", "last_name": "Test"}

    def test_update_profile_success(self):
        response = self.api_client.patch(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_200_OK
        self.profile.refresh_from_db()
        assert self.profile.first_name == "Johny"
        assert self.profile.last_name == "Test"

    def test_update_profile_unauthenticated(self):
        self.api_client.logout()
        self.data["last_name"] = "Doe"
        response = self.api_client.patch(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUpdateAuthAPIView:
    def setup_method(self):
        self.profile = Profile.objects.create_user(
            first_name="Test",
            email="test@company.com",
            password="StringPass123"
        )
        self.api_client = APIClient()
        _, token = AuthToken.objects.create(self.profile)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        self.url = reverse("profile:update-auth", kwargs={"id": self.profile.id})
        self.data = {"email": "contact@company.com"}

    def test_update_auth_success(self):
        response = self.api_client.patch(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_200_OK
        self.profile.refresh_from_db()
        assert self.profile.email == "contact@company.com"
    
    def test_update_auth_unauthenticated(self):
        self.api_client.logout()
        response = self.api_client.patch(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED