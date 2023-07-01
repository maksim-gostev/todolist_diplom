from typing import Any

from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from core.models import User
from core.serializers import ChangingPasswordSerializer, ProfileSerializer, UserCreateSerializer, UserLoginSerializer

# Create your views here.


class SignUpView(generics.GenericAPIView):
    """
    Регистрация
    """

    queryset = User
    permission_classes = [permissions.AllowAny]
    serializer_class = UserCreateSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    """
    Авторизация пользователя
    """

    queryset = User
    serializer_class = UserLoginSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'], password=serializer.validated_data['password']
        )

        if not user:
            raise AuthenticationFailed

        login(request=request, user=user)
        return Response(ProfileSerializer(user).data, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    Получение, обновление, выход
    """

    serializer_class = ProfileSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self) -> User:
        return self.request.user

    def perform_destroy(self, instance: User) -> None:
        logout(self.request)


class ChangingPasswordView(generics.UpdateAPIView):
    """
    Обновление пороля
    """

    serializer_class = ChangingPasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = request.user

        if not user.check_password(serializer.validated_data['old_password']):
            raise AuthenticationFailed('Не верный пороль')

        user.set_password(serializer.validated_data['new_password'])
        user.save(update_fields=['password'])

        return Response(serializer.data)
