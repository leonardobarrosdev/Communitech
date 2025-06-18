import pytest, uuid
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.course.models import (
    Course,
    Section,
    Lesson,
    LessonProgress,
)

User = get_user_model()


@pytest.fixture
def test_user():
    return User.objects.create(
        username="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def test_course(test_user):
    return Course.objects.create(
        title="Test Course",
        description="Test Description",
        type="self-paced",
        status="published",
        visibility="public",
        author=test_user,
    )


@pytest.fixture
def test_section(test_course):
    return Section.objects.create(title="Test Section", position=1, course=test_course)


@pytest.fixture
def test_lesson(test_section):
    return Lesson.objects.create(
        title="Test Lesson",
        content_type="video",
        content="https://example.com/video",
        position=1,
        section=test_section,
    )


@pytest.mark.django_db
class TestCourseModel:
    def test_create_course(self, test_course):
        assert isinstance(test_course.id, uuid.UUID)
        assert test_course.title == "Test Course"
        assert test_course.created_at
        assert test_course.updated_at

    def test_course_author_relationship(self, test_course, test_user):
        assert test_course.author == test_user
        assert test_course in test_user.courses.all()


@pytest.mark.django_db
class TestSectionModel:
    def test_create_section(self, test_section, test_course):
        assert isinstance(test_section.id, uuid.UUID)
        assert test_section.title == "Test Section"
        assert test_section.position == 1
        assert test_section.course == test_course

    def test_section_course_relationship(self, test_section, test_course):
        assert test_section in test_course.sections.all()


@pytest.mark.django_db
class TestLessonModel:
    def test_create_lesson(self, test_lesson, test_section):
        assert isinstance(test_lesson.id, uuid.UUID)
        assert test_lesson.title == "Test Lesson"
        assert test_lesson.content_type == "video"
        assert test_lesson.position == 1
        assert test_lesson.section == test_section

    def test_lesson_section_relationship(self, test_lesson, test_section):
        assert test_lesson in test_section.lessons.all()


@pytest.mark.django_db
class TestLessonProgressModel:
    def test_create_lesson_progress(self, test_user, test_lesson):
        progress = LessonProgress.objects.create(
            user=test_user,
            lesson=test_lesson,
            completed=True,
            completed_at=timezone.now(),
        )
        assert isinstance(progress.id, uuid.UUID)
        assert progress.user == test_user
        assert progress.lesson == test_lesson
        assert progress.completed is True
