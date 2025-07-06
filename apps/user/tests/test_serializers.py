import pytest, uuid
from django.contrib.auth import get_user_model
from apps.user.serializers import (
    ProfileSerializer,
    RegisterSerializer,
    UpdateProfileSerializer,
    UpdateAuthSerializer,
)

Profile = get_user_model()


@pytest.fixture
def get_profile():
    generate_name = f"test{uuid.uuid4().hex[:8]}"
    return Profile.objects.create_user(
        email=f"{generate_name}@example.com",
        password="StrongPass123!",
        first_name="Test",
        last_name="User",
    )


class TestUserSerializer:
    def test_profile_serializer_fields(self):
        profile = Profile(
            id=1, first_name="Test", last_name="User", email="test@example.com"
        )
        serializer = ProfileSerializer(profile)
        assert serializer.data == {
            "id": 1,
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
        }


@pytest.mark.django_db
class TestRegisterSerializer:
    data = {
        "email": "test@example.com",
        "password": "StrongPass123!",
        "password2": "StrongPass123!",
        "first_name": "Test",
        "last_name": "User",
    }

    def test_valid_registration(self):
        serializer = RegisterSerializer(data=self.data)
        assert serializer.is_valid()
        profile = serializer.save()
        assert profile.email == "test@example.com"
        assert profile.first_name == "Test"
        assert profile.check_password("StrongPass123!")

    def test_passwords_not_matching(self):
        data = self.data.copy()
        data["password2"] = "DifferentPass123!"
        serializer = RegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "Invalid password." in str(serializer.errors)

    def test_email_already_exists(self):
        data = self.data.copy()
        data.pop("password2")
        Profile.objects.create_user(**data)
        serializer = RegisterSerializer(data=self.data)
        assert not serializer.is_valid()
        assert "unique" in str(serializer.errors)


@pytest.mark.django_db
class TestUpdateUserSerializer:
    data = {
        "thumbnail": "profile.png",
        "first_name": "Test",
        "last_name": "User",
        "language": "en",
        "headline": None,
        "bio": None,
        "location": None,
        "website": None,
        "linkedin": None,
        "member_send_messages": False,
        "show_profile": False,
    }

    def test_update_profile_serializer(self, get_profile):
        profile = get_profile
        data = self.data.copy()
        serializer = UpdateProfileSerializer(profile, data=data, partial=True)
        assert serializer.is_valid()
        updated_profile = serializer.save()
        assert updated_profile.first_name == data["first_name"]

    def test_update_profile_serializer_invalid_data(self, get_profile):
        profile = get_profile
        data = self.data.copy()
        data["language"] = "invalid_language"
        serializer = UpdateProfileSerializer(profile, data=data, partial=True)
        assert not serializer.is_valid()
        assert "language" in str(serializer.errors)


@pytest.mark.django_db
class TestUpdateAuthSerializer:
    data = {
        "old_password": "StrongPass123!",
        "new_password": "mypassword123",
        "confirm_password": "mypassword123",
        "is_active": True,
    }

    def test_update_auth_serializer(self, get_profile):
        profile = get_profile
        self.data["email"] = profile.email
        serializer = UpdateAuthSerializer(
            instance=profile, data=self.data, partial=True
        )
        assert serializer.is_valid()
        updated_auth = serializer.save()
        assert updated_auth.email == self.data["email"]
        assert updated_auth.check_password(self.data["new_password"])

    def test_update_auth_serializer_invalid_data(self, get_profile):
        profile = get_profile
        self.data["email"] = profile.email
        self.data["new_password"] = "short"
        serializer = UpdateAuthSerializer(
            instance=profile, data=self.data, partial=True
        )
        assert not serializer.is_valid()
