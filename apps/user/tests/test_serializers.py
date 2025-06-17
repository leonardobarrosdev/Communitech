import pytest
from django.contrib.auth import get_user_model
from apps.user.serializers import UserSerializer, RegisterSerializer


User = get_user_model()

class TestUserSerializer:
    def test_user_serializer_fields(self):
        user = User(
            id=1,
            first_name='Test',
            last_name='User',
            email='test@example.com'
        )
        serializer = UserSerializer(user)
        assert serializer.data == {
            'id': 1,
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com'
        }


@pytest.mark.django_db
class TestRegisterSerializer:
    def test_valid_registration(self):
        data = {
            'email': 'test@example.com',
            'password': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.email == 'test@example.com'
        assert user.first_name == 'Test'
        assert user.check_password('StrongPass123!')

    def test_passwords_not_matching(self):
        data = {
            'email': 'test@example.com',
            'password': 'StrongPass123!',
            'password2': 'DifferentPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        serializer = RegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Invalid password.' in str(serializer.errors)

    def test_email_already_exists(self):
        User.objects.create_user(
            email='existing@example.com',
            password='StrongPass123!',
            first_name='Existing',
            last_name='User'
        )
        data = {
            'email': 'existing@example.com',
            'password': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        serializer = RegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert 'unique' in str(serializer.errors)
