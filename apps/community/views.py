from rest_framework import viewsets
from django.db.models import Q
from apps.community.models import Community, Group, Space
from apps.community.serializers import (
    CommunitySerializer,
    CommunityUpdateSerializer,
    GroupSerializer,
    GroupDetailSerializer,
    SpaceSerializer,
)


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer


class CommunityUpdateView(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunityUpdateSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None


class GroupDetailViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupDetailSerializer


class SpaceViewSet(viewsets.ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return Space.objects.filter(
            Q(visibility="public") | Q(membership__user=user) | Q(moderators=user)
        ).distinct()
