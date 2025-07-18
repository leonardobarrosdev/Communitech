from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from config.paginations import ResultsSetPagination
from apps.course.models import Course, Section, Lesson, LessonProgress

from .serializers import (
    CourseSerializer,
    SectionSerializer,
    LessonSerializer,
    LessonProgressSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related("author").prefetch_related("sections")
    serializer_class = CourseSerializer
    pagination_class = ResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.prefetch_related("lessons")
    serializer_class = SectionSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    @action(detail=True, methods=["post"])
    def mark_complete(self, request, pk=None):
        lesson = self.get_object()
        progress, created = LessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson,
            defaults={"completed": True, "completed_at": timezone.now()},
        )
        if not created:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()
        return Response(
            {"status": "lesson marked as complete"}, status=status.HTTP_200_OK
        )


class LessonProgressViewSet(viewsets.ModelViewSet):
    serializer_class = LessonProgressSerializer

    def get_queryset(self):
        return LessonProgress.objects.filter(user=self.request.user)
