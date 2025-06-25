from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from apps.community.models import Space
from apps.community.serializers import SpaceSerializer


class SpaceViewSet(viewsets.ModelViewSet):
    serializer_class = SpaceSerializer
    queryset = Space.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Space.objects.filter(
            Q(visibility='public') |
            Q(membership__user=user) |
            Q(moderators=user)
        ).distinct()
