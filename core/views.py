from typing import Any
from urllib.request import Request

from django.contrib.auth import authenticate, login
from rest_framework import permissions, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from core.models import User
from core.serializers import UserCreateSerializer, UserLoginSerializer

# Create your views here.


class SignUpView(CreateAPIView):
    """
    Регистрация
    """

    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserCreateSerializer


class UserLoginView(GenericAPIView):
    """
    Авторизация пользователя
    """

    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'], password=serializer.validated_data['password']
        )

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed
