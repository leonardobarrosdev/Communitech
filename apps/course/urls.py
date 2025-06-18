from django.urls import path
from apps.course.views import (
    CourseViewSet,
    SectionViewSet,
    LessonViewSet,
    LessonProgressViewSet,
)

urlpatterns = [
    path(
        "courses/",
        CourseViewSet.as_view({"get": "list", "post": "create"}),
        name="course-list",
    ),
    path(
        "courses/<uuid:pk>/",
        CourseViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="course-detail",
    ),
    path(
        "sections/",
        SectionViewSet.as_view({"get": "list", "post": "create"}),
        name="section-list",
    ),
    path(
        "sections/<uuid:pk>/",
        SectionViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="section-detail",
    ),
    path(
        "lessons/",
        LessonViewSet.as_view({"get": "list", "post": "create"}),
        name="lesson-list",
    ),
    path(
        "lessons/<uuid:pk>/",
        LessonViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="lesson-detail",
    ),
    path(
        "lessons/<uuid:pk>/mark_complete/",
        LessonViewSet.as_view({"post": "mark_complete"}),
        name="lesson-mark-complete",
    ),
    path(
        "progress/",
        LessonProgressViewSet.as_view({"get": "list", "post": "create"}),
        name="lesson-progress-list",
    ),
    path(
        "progress/<uuid:pk>/",
        LessonProgressViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="lesson-progress-detail",
    ),
]
