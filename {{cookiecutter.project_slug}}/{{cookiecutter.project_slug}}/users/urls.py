# -*- coding: utf-8 -*-

"""Urls for users."""

from django.urls import path
{%- if cookiecutter.api_only_mode == 'y' %}
from django.urls import re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from {{ cookiecutter.project_slug }}.users.views import LoginView
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
    re_path(r'^jwt/create/?', LoginView.as_view(), name='jwt-create'),
    re_path(r'^jwt/refresh/?', jwt_views.TokenRefreshView.as_view(), name='jwt-refresh'),
    re_path(r'^jwt/verify/?', jwt_views.TokenVerifyView.as_view(), name='jwt-verify'),
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
