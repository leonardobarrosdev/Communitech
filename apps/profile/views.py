from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from knox.models import AuthToken

from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from apps.profile.serializers import ProfileSerializer, RegisterSerializer
from apps.profile.ultils import Util, CsrfExemptSessionAuthentication
from apps.profile.serializers import UpdateProfileSerializer, UpdateAuthSerializer
from apps.profile.models import Profile


class RegisterAPIView(CreateAPIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    queryset = Profile.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid fields."}, status=status.HTTP_400_BAD_REQUEST
            )
        profile = serializer.save()
        token_object, token = AuthToken.objects.create(profile)
        email_body = render_to_string("emails/welcome.txt", {"user": profile})
        data = {
            "email_subject": _(
                "Welcome to Comunitu - Your Ultimate Community Platform!"
            ),
            "email_body": _(email_body),
            "to_email": profile.email,
        }
        Util.send_email(data=data)
        return Response(
            {
                "user": ProfileSerializer(
                    profile, context=self.get_serializer_context()
                ).data,
                "token": token,
            },
            status=status.HTTP_201_CREATED,
        )


class UpdateProfileAPIView(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UpdateProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def patch(self, request, **kwargs):
        try:
            profile = self.queryset.get(id=kwargs["id"])
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(
                    {serializer.errors[:]}, status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateAuthAPIView(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UpdateAuthSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, **kwargs):
        try:
            profile = self.queryset.get(id=kwargs["id"])
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(
                    {serializer.errors[:]}, status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
