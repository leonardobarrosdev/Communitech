import pytest
from datetime import datetime
from django.contrib.auth import get_user_model
from apps.course.models import (
    Course,
    Section,
    Lesson,
    LessonProgress,
)

from apps.course.serializers import (
    CourseSerializer,
    SectionSerializer,
    LessonSerializer,
    LessonProgressSerializer,
)

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(email="testuser@example.com", password="testpass")


@pytest.fixture
def course(user):
    return Course.objects.create(
        title="Test Course",
        description="Test Description",
        author=user,
        type="free",
        status="draft",
        visibility="private",
    )


@pytest.fixture
def section(course):
    return Section.objects.create(title="Test Section", course=course, position=1)


@pytest.fixture
def lesson(section):
    return Lesson.objects.create(
        title="Test Lesson",
        section=section,
        content_type="text",
        content="Test Content",
        position=1,
    )


@pytest.mark.django_db
class TestCourseSerializer:
    def test_contains_expected_fields(self, course):
        serializer = CourseSerializer(instance=course)
        data = serializer.data

        assert set(data.keys()) == {
            "id",
            "title",
            "description",
            "type",
            "status",
            "visibility",
            "author",
            "author_name",
            "sections",
            "created_at",
            "updated_at",
        }


@pytest.mark.django_db
class TestSectionSerializer:
    def test_contains_expected_fields(self, section):
        serializer = SectionSerializer(instance=section)
        data = serializer.data

        assert set(data.keys()) == {
            "id",
            "title",
            "position",
            "lessons",
            "created_at",
            "updated_at",
        }


@pytest.mark.django_db
class TestLessonSerializer:
    def test_contains_expected_fields(self, lesson):
        serializer = LessonSerializer(instance=lesson)
        data = serializer.data

        assert set(data.keys()) == {
            "id",
            "title",
            "content_type",
            "content",
            "position",
            "created_at",
            "updated_at",
        }


@pytest.mark.django_db
class TestLessonProgressSerializer:
    def test_contains_expected_fields(self, user, lesson):
        progress = LessonProgress.objects.create(
            user=user, lesson=lesson, completed=True, completed_at=datetime.now()
        )
        serializer = LessonProgressSerializer(instance=progress)
        data = serializer.data

        assert set(data.keys()) == {"id", "user", "lesson", "completed", "completed_at"}
