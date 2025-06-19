import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.course.models import Course, Section, Lesson, LessonProgress
from apps.course.serializers import SectionSerializer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    User = get_user_model()
    return User.objects.create_user(email="test@example.com", password="testpass")


@pytest.fixture
def test_course(test_user):
    return Course.objects.create(
        title="Test Course", description="Test Description", author=test_user
    )


@pytest.fixture
def test_section(test_course):
    return Section.objects.create(title="Test Section", position=1, course=test_course)


@pytest.fixture
def test_lesson(test_section):
    return Lesson.objects.create(
        title="Test Lesson", content="Test Content", position=1, section=test_section
    )


@pytest.mark.django_db
class TestCourseViewSet:
    def test_list_courses(self, api_client, test_user, test_course):
        api_client.force_authenticate(user=test_user)
        url = reverse("course-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_course(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        url = reverse("course-list")
        data = {
            "title": "New Course",
            "description": "New Description",
            "type": "free",
            "status": "draft",
            "visibility": "public",
            "author": str(test_user.id),
            "author_name": test_user.get_full_name(),
            "sections": [],
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "New Course"


@pytest.mark.django_db
class TestLessonViewSet:
    def test_mark_lesson_complete(self, api_client, test_user, test_lesson):
        api_client.force_authenticate(user=test_user)
        url = reverse("lesson-mark-complete", kwargs={"pk": test_lesson.pk})
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK

        progress = LessonProgress.objects.get(user=test_user, lesson=test_lesson)
        assert progress.completed is True
        assert progress.completed_at is not None

    def test_mark_lesson_complete_twice(self, api_client, test_user, test_lesson):
        api_client.force_authenticate(user=test_user)
        url = reverse("lesson-mark-complete", kwargs={"pk": test_lesson.pk})

        # First attempt
        response1 = api_client.post(url)
        assert response1.status_code == status.HTTP_200_OK

        # Second attempt
        response2 = api_client.post(url)
        assert response2.status_code == status.HTTP_200_OK

        progress_count = LessonProgress.objects.filter(
            user=test_user, lesson=test_lesson
        ).count()
        assert progress_count == 1


@pytest.mark.django_db
class TestLessonProgressViewSet:
    def test_list_progress(self, api_client, test_user, test_lesson):
        api_client.force_authenticate(user=test_user)
        LessonProgress.objects.create(
            user=test_user,
            lesson=test_lesson,
            completed=True,
            completed_at=timezone.now(),
        )

        url = reverse("lesson-progress-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
