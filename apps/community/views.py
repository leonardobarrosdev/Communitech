from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from knox.auth import TokenAuthentication
from apps.community.models import (
    Community, Space
)
from apps.community.serializers import (
    CommunitySerializer,
    CommunityUpdateSerializer,
    SpaceSerializer
)


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CommunityUpdateView(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunityUpdateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class SpaceViewSet(viewsets.ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Space.objects.filter(
            Q(visibility='public') |
            Q(membership__user=user) |
            Q(moderators=user)
        ).distinct()
