from typing import Any

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import User


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs: Any) -> None:
        kwargs['style'] = {'input_type': 'password'}
        kwargs.setdefault('write_only', True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)


class UserCreateSerializer(serializers.ModelSerializer):
    password = PasswordField(min_length=8)
    password_repeat = PasswordField(min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict:
        if attrs['password'] == attrs['password_repeat']:
            return attrs
        raise ValidationError('Пароли не совпадают')

    def create(self, validated_data: dict) -> User:
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)
