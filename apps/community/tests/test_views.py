import pytest, random
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from knox.models import AuthToken
from apps.community.models import Community, Group

User = get_user_model()

@pytest.fixture
def get_user():
    generate_name = f"test{random.randint(1, 100)}"
    return User.objects.create_user(
        email=f"{generate_name}@example.com",
        password="StrongPass123!",
        first_name="Test",
        last_name="User",
    )

@pytest.fixture
def get_community(get_user):
    user = get_user
    return Community.objects.create(
        owner=user,
        name="New Community",
        description="Test community"
    )


@pytest.mark.django_db
class TestCreateCommunityAPIView:
    api_client = APIClient()

    @pytest.fixture(autouse=True)
    def setUp(self, get_user):
        self.user = get_user
        _, token = AuthToken.objects.create(self.user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        self.url = reverse("community-list")
        self.data = {
            "owner": self.user.id,
            "name": "New Community",
            "description": "Testing community",
        }

    def test_create_community_success(self):
        response = self.api_client.post(path=self.url, data=self.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == self.data["name"]

    def test_create_community_failed(self):
        data = self.data.copy()
        del data["owner"]
        response = self.api_client.post(path=self.url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "owner" in response.data

    def test_community_unauthorized(self):
        self.api_client.logout()
        response = self.api_client.post(path=self.url, data=self.data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestListCommunityAPIView:
    api_client = APIClient()

    @pytest.fixture(autouse=True)
    def setUp(self, get_user):
        self.user = get_user
        _, token = AuthToken.objects.create(self.user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        self.url = reverse("community-list")
        self.data = {
            "owner": self.user.id,
            "name": "New Community",
            "description": "Testing community",
        }

    def test_list_community_success(self):
        self.api_client.post(path=self.url, data=self.data, format="json")
        data = self.data.copy()
        data["name"] = "Second community"
        self.api_client.post(path=self.url, data=data, format="json")
        response = self.api_client.get(path=self.url, format="json")
        assert len(response.data) == 2

    def test_list_community_0(self):
        response = self.api_client.get(path=self.url, format="json")
        assert len(response.data) == 0


@pytest.mark.django_db
class TestRetrieveCommunityAPIView:
    api_client = APIClient()

    @pytest.fixture(autouse=True)
    def setUp(self, get_user):
        self.user = get_user
        _, token = AuthToken.objects.create(self.user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        self.url = reverse("community-list")
        self.data = {
            "owner": self.user.id,
            "name": "New Community",
            "description": "Testing community",
        }

    def test_retrieve_community_success(self):
        info = self.api_client.post(path=self.url, data=self.data, format="json")
        url = reverse("community-details", kwargs={"pk": info.data["id"]})
        response = self.api_client.get(path=url, format="json")
        assert response.data["id"] == info.data["id"]

    def test_retrieve_community_failed(self):
        url = reverse("community-details", kwargs={"pk": 2})
        response = self.api_client.get(path=url, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateCommunityAPIView:
    api_client = APIClient()

    @pytest.fixture(autouse=True)
    def setUp(self, get_user):
        self.user = get_user
        _, token = AuthToken.objects.create(self.user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        self.url = reverse("community-list")
        self.data = {
            "owner": self.user.id,
            "name": "New Community",
            "description": "Testing community",
        }

    def test_update_community_success(self):
        info = self.api_client.post(path=self.url, data=self.data, format="json")
        url = reverse("community-update", kwargs={"pk": info.data["id"]})
        data = {"name": "Your ".join(self.data["name"].split()[0:])}
        response = self.api_client.put(path=url, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == data["name"]

    def test_update_community_failed(self):
        info = self.api_client.post(path=self.url, data=self.data, format="json")
        url = reverse("community-update", kwargs={"pk": info.data["id"]})
        data = {}
        response = self.api_client.put(path=url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteCommunityAPIView:
    api_client = APIClient()

    @pytest.fixture(autouse=True)
    def setUp(self, get_user):
        self.user = get_user
        _, token = AuthToken.objects.create(self.user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        self.url = reverse("community-list")
        self.data = {
            "owner": self.user.id,
            "name": "New Community",
            "description": "Testing community",
        }

    def test_delete_community_success(self):
        info = self.api_client.post(path=self.url, data=self.data, format="json")
        url = reverse("community-details", kwargs={"pk": info.data["id"]})
        response = self.api_client.delete(path=url, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_community_failed(self):
        url = reverse("community-details", kwargs={"pk": 999999})
        response = self.api_client.delete(path=url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestListGroupView:
    api_client = APIClient()

    @pytest.fixture(autouse=True)
    def setUp(self, get_user):
        self.user = get_user
        _, token = AuthToken.objects.create(self.user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        self.url = reverse("group-list")
        self.community = Community.objects.create(
            owner=self.user,
            name="New Community",
            description="Testing community"
        )
        self.data = {"name": "Test group", "community": self.community.id}
    
    def test_create_group_success(self):
        response = self.api_client.post(path=self.url, data=self.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == self.data["name"]
    
    def test_create_group_failed(self):
        data = self.data.copy()
        del data["name"]
        response = self.api_client.post(path=self.url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_list_group_success(self):
        self.api_client.post(path=self.url, data=self.data, format="json")
        self.api_client.post(path=self.url, data=self.data, format="json")
        response = self.api_client.get(path=self.url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_list_group_unauthorized(self):
        self.api_client.logout()
        response = self.api_client.get(path=self.url, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestDetailGroupView:
    api_client = APIClient()

    @pytest.fixture(autouse=True)
    def setUp(self, get_community):
        community = get_community
        self.user = User.objects.get(id=community.owner.id)
        _, token = AuthToken.objects.create(self.user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        group = Group.objects.create(name="Test group", community=community)
        self.url = reverse("group-detail", kwargs={"pk": group.id})
    
    def test_retrieve_group_success(self):
        response = self.api_client.get(path=self.url, format="json")
        assert response.status_code == status.HTTP_200_OK
    
    def test_restrieve_group_not_found(self):
        url = reverse("group-detail", kwargs={"pk": 0})
        response = self.api_client.get(path=url, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_group_success(self):
        data = {"name": "Testing"}
        response = self.api_client.put(path=self.url, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == data["name"]
    
    def test_update_group_failed(self):
        data = {"community": 0}
        response = self.api_client.put(path=self.url, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_delete_group_success(self):
        response = self.api_client.delete(path=self.url, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        resp_verify = self.api_client.get(path=self.url, format="json")
        assert resp_verify.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_group_unauthorized(self):
        self.api_client.logout()
        response = self.api_client.delete(path=self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
