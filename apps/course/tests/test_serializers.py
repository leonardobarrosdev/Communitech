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
    LessonProgressListSerializer,
    LessonProgressDetailSerializer
)

User = get_user_model()


@pytest.fixture
def get_user():
    return User.objects.create_user(email="testuser@example.com", password="testpass")

@pytest.fixture
def get_course(get_user):
    return Course.objects.create(
        title="Test Course",
        description="Test Description",
        author=get_user,
        type="free",
        status="draft",
        visibility="private",
    )

@pytest.fixture
def get_section(get_course):
    return Section.objects.create(title="Test Section", course=get_course, position=1)

@pytest.fixture
def get_lesson(get_section):
    return Lesson.objects.create(
        title="Test Lesson",
        section=get_section,
        content_type="text",
        content="Test Content",
        position=1
    )

@pytest.fixture
def get_progress(get_user, get_lesson):
    return LessonProgress.objects.create(user=get_user, lesson=get_lesson)


@pytest.mark.django_db
class TestCourseSerializer:
    def test_contains_expected_fields(self, get_course):
        serializer = CourseSerializer(instance=get_course)
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
    def test_contains_expected_fields(self, get_section):
        serializer = SectionSerializer(instance=get_section)
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
    def test_contains_expected_fields(self, get_lesson):
        serializer = LessonSerializer(instance=get_lesson)
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
class TestLessonProgressListSerializer:
    serializer = LessonProgressListSerializer

    def setup_method(self, get_progress):
        self.serializer = self.serializer(instance=get_progress)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        assert set(data.keys()) == {"id", "user", "lesson", "completed", "completed_at"}
    
    def test_completed_lower_bound(self):
        self.serializer.data["completed"] = True
        serializer = LessonProgressListSerializer(data=self.serializer.data)
        assert serializer.is_valid() == False
        assert set(serializer.errors) == set(["completed"])


@pytest.mark.django_db
class TestLessonProgressDetailSerializer:
    serializer = LessonProgressDetailSerializer

    @pytest.fixture(autouse=True)
    def setUp(self, get_progress):
        self.serializer = self.serializer(instance=get_progress)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        assert set(data.keys()) == {"id", "user", "lesson", "completed", "completed_at"}
    
    def test_update_lesson_progress(self):
        data = {"completed": True}
        serializer = LessonProgressDetailSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.data["completed"] == data["completed"]
