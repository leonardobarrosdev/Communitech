from django.urls import path
from community.views import CommunityViewSet, CommunityUpdateView

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
]
