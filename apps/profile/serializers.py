from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from apps.profile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "first_name", "last_name", "email"]
        read_only_fields = ["id"]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=Profile.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "email", "password", "password2"]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        email = attrs.get("email", "").strip().lower()
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if not email or "@" not in email:
            raise serializers.ValidationError(_("Email is required."))
        if password != password2:
            raise serializers.ValidationError(_("Invalid password."))
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        profile = Profile.objects.create_user(**validated_data)
        profile.set_password(validated_data["password"])
        profile.save()
        return profile


class UpdateProfileSerializer(serializers.ModelSerializer):
    """Serializer for updating profile information."""

    class Meta:
        model = Profile
        fields = [
            "thumbnail",
            "first_name",
            "last_name",
            "language",
            "headline",
            "bio",
            "location",
            "website",
            "linkedin",
            "member_send_messages",
            "show_profile",
        ]


class UpdateAuthSerializer(serializers.ModelSerializer):
    """Serializer for updating authentication profile information."""

    old_password = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False,
        validators=[validate_password],
        help_text=_("Current password for verification."),
    )
    new_password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        help_text=_("New password. Must meet password complexity requirements."),
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        help_text=_("Confirm new password by repeating it."),
    )

    class Meta:
        model = Profile
        fields = [
            "email",
            "old_password",
            "new_password",
            "confirm_password",
            "is_active",
        ]

    def validate(self, attrs):
        email = attrs.get("email", "").strip().lower()
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")
        if not email:
            raise serializers.ValidationError(_("Email is required."))
        if old_password and new_password and new_password != confirm_password:
            raise serializers.ValidationError(_("New passwords do not match."))
        return attrs

    def update(self, instance, validated_data):
        new_password = validated_data.pop("new_password", None)
        if new_password:
            instance.set_password(new_password)
        instance.email = validated_data.get("email", instance.email)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance
