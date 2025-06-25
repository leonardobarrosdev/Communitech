import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from apps.notification.models import NotificationType, UserNotificationPreference
from django.utils.translation import gettext_lazy as _
from community.models import Space

@pytest.mark.django_db
def test_notification_type_str():
    space = Space.objects.create(name="Test Space", slug="test-space")
    notif_type = NotificationType.objects.create(
        name="Like",
        slug="like",
        category="activity",
        space=space,
        is_default=True
    )
    assert str(notif_type) == "Like"

@pytest.mark.django_db
def test_notification_type_unique_slug():
    space = Space.objects.create(name="Test Space", slug="test-space")
    NotificationType.objects.create(
        name="Comment",
        slug="comment",
        category="activity",
        space=space
    )
    with pytest.raises(IntegrityError):
        NotificationType.objects.create(
            name="Comment 2",
            slug="comment",
            category="activity",
            space=space
        )

@pytest.mark.django_db
def test_user_notification_preference_unique_together():
    User = get_user_model()
    user = User.objects.create_user(username="user1", password="pass")
    space = Space.objects.create(name="Test Space", slug="test-space")
    notif_type = NotificationType.objects.create(
        name="DM",
        slug="dm",
        category="activity",
        space=space
    )
    UserNotificationPreference.objects.create(
        user=user,
        notification_type=notif_type,
        via_email=True,
        via_platform=True
    )
    with pytest.raises(IntegrityError):
        UserNotificationPreference.objects.create(
            user=user,
            notification_type=notif_type,
            via_email=False,
            via_platform=False
        )

@pytest.mark.django_db
def test_user_notification_preference_defaults():
    User = get_user_model()
    user = User.objects.create_user(username="user2", password="pass")
    space = Space.objects.create(name="Test Space", slug="test-space")
    notif_type = NotificationType.objects.create(
        name="Space Post",
        slug="space-post",
        category="space_post",
        space=space
    )
    pref = UserNotificationPreference.objects.create(
        user=user,
        notification_type=notif_type
    )
    assert pref.via_email is True
    assert pref.via_platform is True
