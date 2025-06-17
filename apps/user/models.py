import uuid
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError


# For testing model validation
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 10  # 10mb


def file_validation(file):
    """
    For regular upload, we get UploadedFile instance, so we can validate it.
    When using direct upload from the browser, here we get an instance of the CloudinaryResource
    and file is already uploaded to Cloudinary.
    Still can perform all kinds on validations and maybe delete file, approve moderation, perform analysis, etc.
    """
    if not file:
        raise ValidationError("No file selected.")
    if isinstance(file, UploadedFile):
        if file.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
            raise ValidationError("File shouldn't be larger than 10MB.")


def upload_thumbnail(instance, filename):
    path = f"thumbnails/{instance.username}"
    extension = filename.split(".")[-1]
    if extension:
        path = path + "." + extension
    return path


def username_generator(instance):
    if not instance.first_name:
        instance.first_name = instance.email.split("@")[0]
    username = f"{instance.first_name}{str(uuid.uuid4().int)[:4]}"
    if len(username) > 30:
        username = username[:26] + str(uuid.uuid4().int)[:4]
    return username


class ProfileManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


# Create your models here.
class Profile(AbstractUser):
    """
    Custom User model that extends the default Django User model.
    """

    email = models.EmailField(_("email address"), unique=True)
    thumbnail = CloudinaryField(
        default="thumbnails/profile.png", validators=[file_validation]
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    objects = ProfileManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = username_generator(self)
        super().save(*args, **kwargs)
