from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from .models import User
from rest_framework import serializers
from rest_framework.exceptions import (ValidationError, NotAuthenticated, AuthenticationFailed)


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs['style'] = {'input_type': 'password'}
        kwargs.setdefault('write_only', True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)


class CreateUserSerializer(serializers.ModelSerializer):
    password = PasswordField
    password_repeat = PasswordField

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    def validate(self, attrs: dict) -> dict:
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data: dict) -> User:
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        read_only_fields = ['username', 'first_name', 'last_name', 'email']

    def create(self, validated_data: dict) -> User:
        if not (user := authenticate(username=validated_data['username'], password=validated_data['password'])):
            raise AuthenticationFailed
        return user


class ChangePasswordSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = PasswordField(required=True)
    new_password = PasswordField(required=True)

    def validate(self, attrs: dict) -> dict:
        if not (user := attrs['user']):
            raise NotAuthenticated
        if not user.check_password(attrs['old_password']):
            raise ValidationError("Password is incorrect")
        return attrs

    def create(self, validated_data: dict):
        raise NotImplementedError

    def update(self, instance: User, validated_data: dict) -> User:
        instance.password = make_password(validated_data['new_password'])
        instance.save()
        return instance


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        read_only_fields = ['username']
