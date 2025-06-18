from rest_framework import serializers
from apps.course.models import (
    Course,
    Section,
    Lesson,
    LessonProgress,
)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "content_type",
            "content",
            "position",
            "created_at",
            "updated_at",
        ]


class SectionSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ["id", "title", "position", "lessons", "created_at", "updated_at"]


class CourseSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Course
        fields = [
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
        ]


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ["id", "user", "lesson", "completed", "completed_at"]
