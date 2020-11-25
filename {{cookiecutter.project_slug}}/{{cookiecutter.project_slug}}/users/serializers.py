# -*- coding: utf-8 -*-

"""Serializers for users."""

import re

from localflavor.it.util import ssn_validation
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import TokenError

from {{ cookiecutter.project_slug }}.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User."""

    is_staff = serializers.BooleanField(required=False)

    class Meta:
        """Metadata for serializer."""

        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'name',
            'first_name',
            'last_name',
            'cf',
            'is_privacy_accepted',
            'is_email_validated',
            'is_staff',
        )
        read_only_fields = ('is_email_validated', )
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
        }

    def validate(self, data_sent):
        """Check if the data sent are valid."""
        cf = data_sent.get('cf', '').upper()
        if len(cf) != 16:  # noqa: WPS432 - length of a standard cf
            raise serializers.ValidationError({
                'cf': ['Not valid cf. It should have 16 characters.'],
            })
        if re.match(r'[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]', cf) is None:
            raise serializers.ValidationError({
                'cf': ['Not valid cf'],
            })
        try:
            ssn_validation(cf)
        except ValueError:
            raise serializers.ValidationError({
                'cf': ['Not valid cf'],
            })

        if User.objects.filter(cf=cf).exists():
            raise serializers.ValidationError({
                'cf': ['User with this cf already exists.'],
            })

        user = self.context['request'].user
        if data_sent.get('is_staff', False) and (not user.is_staff):
            raise serializers.ValidationError({
                'is_staff': ['Only staff user can grant privileges.'],
            })

        return super().validate(data_sent)

    def create(self, validated_data):
        """Override creation."""
        valid_data = validated_data.copy()
        return User.objects.create_user(**valid_data)


login_fields = {'username', 'password'}
unmutable_fields = login_fields | {'email'}


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for user update."""

    class Meta:
        """Metadata for UserSerializer."""

        model = UserSerializer.Meta.model
        fields = [fd for fd in UserSerializer.Meta.fields if fd not in unmutable_fields]
        read_only_fields = UserSerializer.Meta.read_only_fields
        extra_kwargs = {
            key: vl for key, vl in UserSerializer.Meta.extra_kwargs.items() if key not in unmutable_fields
        }


class UserRegistrationSerializer(UserSerializer):
    """Serializer for user regitration."""

    class Meta:
        """Metadata for UserRegistrationSerializer."""

        model = UserSerializer.Meta.model
        fields = UserSerializer.Meta.fields + (
            'access', 'refresh', 'access_token_expiring_time', 'refresh_token_expiring_time',
        )
        read_only_fields = UserSerializer.Meta.read_only_fields + (
            'access', 'refresh', 'access_token_expiring_time', 'refresh_token_expiring_time',
        )
        extra_kwargs = {
            **UserSerializer.Meta.extra_kwargs,  # type: ignore
            'access': {
                'source': 'get_jwt_access_token',
                'help_text': 'JWT access token',
            },
            'refresh': {
                'source': 'get_jwt_refresh_token',
                'help_text': 'JWT refresh token',
            },
            'access_token_expiring_time': {
                'source': 'get_jwt_access_token_expiring_time',
                'help_text': 'JWT access token expiring time',
            },
            'refresh_token_expiring_time': {
                'source': 'get_jwt_refresh_token_expiring_time',
                'help_text': 'JWT refresh token expiring time',
            },
        }


class UserLoginSerializer(UserRegistrationSerializer):
    """Serializer for user login."""

    class Meta:
        """Metadata for UserLoginSerializer."""

        model = UserRegistrationSerializer.Meta.model
        fields = UserRegistrationSerializer.Meta.fields
        read_only_fields = [
            fd for fd in UserRegistrationSerializer.Meta.fields if fd not in login_fields
        ]
        extra_kwargs = {
            key: vl for key, vl in UserRegistrationSerializer.Meta.extra_kwargs.items() if key not in login_fields
        }


class LogoutSerializer(serializers.Serializer):
    """Serializer for logout action.

    Originally developed by orehush (https://gist.github.com/orehush/667c79b28fdc94f86746bd15694d1167).
    """

    refresh = serializers.CharField(write_only=True)

    default_error_messages = {
        'bad_token': 'Token is invalid or expired',
    }

    def validate(self, data_sent):
        """Validate refresh token passed."""
        try:
            RefreshToken(data_sent['refresh'])
        except TokenError:
            raise serializers.ValidationError({
                'refresh': ['Refresh token not valid or expired.'],
            })

        return super().validate(data_sent)

    def save(self):
        """Put in blacklist the refresh token."""
        RefreshToken(self.validated_data['refresh']).blacklist()


class RefreshResponseSerializer(serializers.Serializer):
    """Serializer used only in refresh documentation."""

    access = serializers.CharField(help_text='Access token, to be passed in JWT header auth.')


class LoginResponseSerializer(RefreshResponseSerializer):
    """Serializer used only in login documentation."""

    refresh = serializers.CharField(help_text='Refresh token, used to obtain a new access token when it is expired.')
