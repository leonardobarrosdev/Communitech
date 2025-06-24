import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from apps.profile.models import Profile, username_generator, file_validation


@pytest.mark.django_db
class TestProfileModel:

    def test_create_profile(self):
        profile = Profile.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        assert profile.email == "test@example.com"
        assert profile.is_active
        assert not profile.is_staff
        assert not profile.is_superuser

    def test_create_superuser(self):
        admin = Profile.objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )
        assert admin.email == "admin@example.com"
        assert admin.is_active
        assert admin.is_staff
        assert admin.is_superuser

    def test_create_profile_without_email(self):
        with pytest.raises(ValueError, match="The Email must be set"):
            Profile.objects.create_user(email="")

    def test_create_superuser_not_staff(self):
        with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
            Profile.objects.create_superuser(
                email="admin@example.com", password="adminpass123", is_staff=False
            )

    def test_username_generator(self):
        profile = Profile(email="test@example.com", first_name="TestUser")
        username = username_generator(profile)
        assert len(username) <= 30
        assert username.startswith("TestUser")

    def test_username_generator_no_first_name(self):
        profile = Profile(email="test@example.com")
        username = username_generator(profile)
        assert len(username) <= 30
        assert username.startswith("test")

    def test_file_validation_no_file(self):
        with pytest.raises(ValidationError, match="No file selected."):
            file_validation(None)

    def test_file_validation_large_file(self):
        large_file = SimpleUploadedFile(
            "test.jpg", b"x" * (1024 * 1024 * 11)  # 11MB file
        )
        with pytest.raises(
            ValidationError, match="File shouldn't be larger than 10MB."
        ):
            file_validation(large_file)

    def test_unique_email(self):
        Profile.objects.create_user(email="test@example.com", password="test123")
        with pytest.raises(IntegrityError):
            Profile.objects.create_user(email="test@example.com", password="test123")

    def test_auto_username_generation(self):
        profile = Profile.objects.create_user(
            email="test@example.com", password="test123"
        )
        assert profile.username is not None
        assert len(profile.username) <= 30
