# -*- coding: utf-8 -*-

"""Urls for users."""

{%- if cookiecutter.api_only_mode == 'y' %}
from django.urls import include
{%- endif %}
from django.urls import path
{%- if cookiecutter.api_only_mode == 'y' %}
from rest_framework.routers import DefaultRouter

from {{ cookiecutter.project_slug }}.users.views import LogoutView
from {{ cookiecutter.project_slug }}.users.views import UserViewSet
{%- else %}

from {{ cookiecutter.project_slug }}.users.views import user_detail_view
from {{ cookiecutter.project_slug }}.users.views import user_redirect_view
from {{ cookiecutter.project_slug }}.users.views import user_update_view
{%- endif %}

app_name = 'users'
urlpatterns = [
    {%- if cookiecutter.api_only_mode == 'y' %}
    path('', include('djoser.urls.jwt')),
    path('jwt/logout/', LogoutView.as_view(), name='jwt-logout'),
    {%- else %}
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    {%- endif %}
]

{%- if cookiecutter.api_only_mode == 'y' %}
router = DefaultRouter()
router.register('', UserViewSet, basename='user')
urlpatterns += router.urls
{%- endif %}
