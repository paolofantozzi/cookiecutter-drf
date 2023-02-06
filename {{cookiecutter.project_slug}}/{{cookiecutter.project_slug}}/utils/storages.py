# -*- coding: utf-8 -*-

"""Storage settings."""

{% if cookiecutter.cloud_provider == 'AWS' -%}
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """Storage for static files."""

    location = 'static'
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    """Storage for media files."""

    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    """Storage for private files."""

    location = 'private'
    default_acl = 'private'
    file_overwrite = False
{%- elif cookiecutter.cloud_provider == 'GCP' -%}
from storages.backends.gcloud import GoogleCloudStorage


class StaticRootGoogleCloudStorage(GoogleCloudStorage):
    location = "static"
    default_acl = "publicRead"


class MediaRootGoogleCloudStorage(GoogleCloudStorage):
    location = "media"
    file_overwrite = False
{%- elif cookiecutter.cloud_provider == 'Azure' -%}
from storages.backends.azure_storage import AzureStorage


class StaticRootAzureStorage(AzureStorage):
    location = "static"


class MediaRootAzureStorage(AzureStorage):
    location = "media"
    file_overwrite = False
{%- endif %}
