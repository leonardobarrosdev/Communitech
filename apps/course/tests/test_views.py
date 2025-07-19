import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.course.models import Course, Section, Lesson, LessonProgress


@pytest.mark.django_db
class TestCourseViewSet:
    api_client = APIClient()
    User = get_user_model()

    def setup_method(self):
        self.user = self.User.objects.create_user(
            email="test@example.com", password="testpass"
        )
        token = Token.objects.create(user=self.user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self.url = reverse("course-list")
        self.data = {
            "title": "New Course",
            "description": "New Description",
            "type": "free",
            "status": "draft",
            "visibility": "public",
            "author": self.user,
        }
    
    def test_list_course_success(self):
        Course.objects.create(**self.data)
        response = self.api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
    
    def test_list_course_unauthorized(self):
        self.api_client.logout()
        Course.objects.create(**self.data)
        response = self.api_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_course_success(self):
        data = self.data.copy()
        data["author"] = str(self.user.id)
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == self.data["title"]
    
    def test_create_course_failed(self):
        data = self.data.copy()
        del data["author"]
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLessonViewSet:
    api_client = APIClient()
    User = get_user_model()

    def setup_method(self):
        self.user = self.User.objects.create_user(
            email="test@example.com", password="testpass"
        )
        token = Token.objects.create(user=self.user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        self.course = Course.objects.create(
            title="Test Course", description="Test Description", author=self.user
        )
        self.section = Section.objects.create(title="Test Section", position=1, course=self.course)
        self.lesson = Lesson.objects.create(
            title="Test Lesson", content="Test Content", position=1, section=self.section
        )

    def test_mark_lesson_complete(self):
        url = reverse("lesson-mark-complete", kwargs={"pk": self.lesson.pk})
        response = self.api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        progress = LessonProgress.objects.get(user=self.user, lesson=self.lesson)
        assert progress.completed is True
        assert progress.completed_at is not None

    def test_mark_lesson_complete_twice(self):
        self.api_client.force_authenticate(user=self.user)
        url = reverse("lesson-mark-complete", kwargs={"pk": self.lesson.pk})
        # First attempt
        response1 = self.api_client.post(url)
        assert response1.status_code == status.HTTP_200_OK
        # Second attempt
        response2 = self.api_client.post(url)
        assert response2.status_code == status.HTTP_200_OK
        progress_count = LessonProgress.objects.filter(
            user=self.user, lesson=self.lesson
        ).count()
        assert progress_count == 1


@pytest.mark.django_db
class TestLessonProgressView:
    api_client = APIClient()
    User = get_user_model()

    def setup_method(self):
        self.user = self.User.objects.create_user(
            email="test@example.com", password="testpass"
        )
        token = Token.objects.create(user=self.user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        self.course = Course.objects.create(
            title="Test Course", description="Test Description", author=self.user
        )
        self.section = Section.objects.create(title="Test Section", position=1, course=self.course)
        self.lesson = Lesson.objects.create(
            title="Test Lesson", content="Test Content", position=1, section=self.section
        )
        self.lesson_progress = LessonProgress.objects.create(
            user=self.user,
            lesson=self.lesson,
            completed=False,
            completed_at=timezone.now(),
        )
        self.url = reverse("lesson-progress-list")
        self.url_id = reverse(
            "lesson-progress-detail", kwargs={"pk": self.lesson_progress.id}
        )

    def test_list_progress_success(self):
        response = self.api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_list_progress_unauthorized(self):
        self.api_client.logout()
        response = self.api_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_retrieve_lesson_progress_success(self):
        response = self.api_client.get(self.url_id)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(self.lesson_progress.id)
    
    def test_update_lesson_progress(self):
        data = {"completed": True}
        response = self.api_client.patch(path=self.url_id, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["completed"] == data["completed"]
    
    def test_destroy_lesson_progress(self):
        response = self.api_client.delete(self.url_id)
        assert response.status_code == status.HTTP_204_NO_CONTENT
