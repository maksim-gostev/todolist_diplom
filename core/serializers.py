from typing import Any

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import exceptions, serializers

from core.models import User


class PasswordFild(serializers.CharField):
    def __init__(self, validate: bool = True, **kwargs: Any) -> None:
        kwargs['style'] = {'input_type': 'password'}
        kwargs.setdefault('write_only', True)
        kwargs.setdefault('required', True)
        super().__init__(**kwargs)
        if validate:
            self.validators.append(validate_password)


class UserCreateSerializer(serializers.ModelSerializer):
    password = PasswordFild(write_only=False)
    password_repeat = PasswordFild(validate=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict:
        if attrs['password'] == attrs['password_repeat']:
            return attrs
        raise exceptions.ValidationError('Пароли не совпадают')

    def create(self, validated_data: dict) -> User:
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = PasswordFild(validate=False)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class ChangingPasswordSerializer(serializers.Serializer):
    old_password = PasswordFild(validate=False)
    new_password = PasswordFild()
