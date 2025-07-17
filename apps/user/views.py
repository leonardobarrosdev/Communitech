from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from apps.user.utils import Util
from apps.user.serializers import (
    ProfileSerializer,
    RegisterSerializer,
    AuthTokenSerializer,
    UpdateProfileSerializer,
    UpdateAuthSerializer
)
from apps.user.models import Profile


class RegisterAPIView(generics.CreateAPIView):
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
        token = Token.objects.create(user=profile)
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
                "token": token.key,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        profile = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=profile)
        return Response({
            'token': token.key,
            'user': {
                'id': profile.pk,
                'first_name': profile.first_name,
                'username': profile.username,
                'email': profile.email
            }
        })


class UpdateProfileAPIView(generics.UpdateAPIView):
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


class UpdateAuthAPIView(generics.UpdateAPIView):
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
