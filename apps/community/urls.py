from django.urls import path
from community.views import (
    CommunityViewSet,
    CommunityUpdateView,
    GroupViewSet,
    GroupDetailViewSet
)

urlpatterns = [
    path(
        "",
        CommunityViewSet.as_view({"get": "list", "post": "create"}),
        name="community-list",
    ),
    path(
        "<int:pk>/",
        CommunityViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
        name="community-details",
    ),
    path(
        "<int:pk>/update/",
        CommunityUpdateView.as_view({"put": "update"}),
        name="community-update",
    ),
    path(
        "groups/",
        GroupViewSet.as_view({"get": "list", "post": "create"}),
        name="group-list"
    ),
    path(
        "groups/<int:pk>/",
        GroupDetailViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="group-detail"
    )
]
