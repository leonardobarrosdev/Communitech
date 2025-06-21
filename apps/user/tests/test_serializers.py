import pytest
from django.contrib.auth import get_user_model
from apps.user.serializers import UserSerializer, RegisterSerializer


User = get_user_model()

@pytest.fixture
def get_user():
    return User.objects.create_user(
        email="existing@example.com",
        password="StrongPass123!",
        first_name="Test",
        last_name="User",
    )

class TestUserSerializer:
    def test_user_serializer_fields(self):
        user = User(id=1, first_name="Test", last_name="User", email="test@example.com")
        serializer = UserSerializer(user)
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
        user = serializer.save()
        assert user.email == "test@example.com"
        assert user.first_name == "Test"
        assert user.check_password("StrongPass123!")

    def test_passwords_not_matching(self):
        data = self.data.copy()
        data["password2"] = "DifferentPass123!"
        serializer = RegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "Invalid password." in str(serializer.errors)

    def test_email_already_exists(self):
        User.objects.create_user(**self.data)
        serializer = RegisterSerializer(data=self.data)
        assert not serializer.is_valid()
        assert "unique" in str(serializer.errors)
