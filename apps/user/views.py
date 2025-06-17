from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from knox.models import AuthToken

from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from .serializers import UserSerializer, RegisterSerializer
from .ultils import Util, CsrfExemptSessionAuthentication


class RegisterAPIView(CreateAPIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid fields."}, status=status.HTTP_400_BAD_REQUEST
            )
        user = serializer.save()
        token_object, token = AuthToken.objects.create(user)
        email_body = render_to_string("emails/welcome.txt", {"user": user})
        data = {
            "email_subject": _(
                "Welcome to Comunitu - Your Ultimate Community Platform!"
            ),
            "email_body": _(email_body),
            "to_email": user.email,
        }
        Util.send_email(data=data)
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": token,
            },
            status=status.HTTP_201_CREATED,
        )
