# -*- coding: utf-8 -*-

"""Serializers for users."""

from localflavor.it.util import ssn_validation
from rest_framework import serializers

from {{ cookiecutter.project_slug }}.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User."""

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
            'is_privacy_accepted',
            'is_email_validated',
        )
        read_only_fields = ('is_email_validated', )
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
        }

    def validate(self, data_sent):
        """Check if the data sent are valid."""
        try:
            ssn_validation(data_sent.get('cf', ''))
        except ValueError:
            raise serializers.ValidationError({
                'cf': ['Not valid cf'],
            })

        if User.objects.filter(cf=data_sent['cf']).exists():
            raise serializers.ValidationError({
                'cf': ['User with this cf already exists.'],
            })

        return super().validate(data_sent)

    def create(self, validated_data):
        """Override creation."""
        valid_data = validated_data.copy()
        return User.objects.create_user(**valid_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for user update."""

    class Meta:
        """Metadata for UserSerializer."""

        model = UserSerializer.Meta.model
        fields = [fd for fd in UserSerializer.Meta.fields if fd not in {'password', 'email'}]
        read_only_fields = UserSerializer.Meta.read_only_fields
        extra_kwargs = {
            key: vl for key, vl in UserSerializer.Meta.extra_kwargs.items() if key not in {'password', 'email'}
        }


class UserRegistrationSerializer(serializers.ModelSerializer):
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


login_fields = {'username', 'password'}


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
