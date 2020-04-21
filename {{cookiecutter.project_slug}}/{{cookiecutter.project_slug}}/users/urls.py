# -*- coding: utf-8 -*-

"""Urls for users."""

from django.urls import path
{%- if cookiecutter.api_only_mode == 'y' %}
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from {{ cookiecutter.project_slug }}.users.views import UserViewSet
{%- else %}

from {{ cookiecutter.project_slug }}.users.views import user_detail_view
from {{ cookiecutter.project_slug }}.users.views import user_redirect_view
from {{ cookiecutter.project_slug }}.users.views import user_update_view
{%- endif %}

app_name = "users"
urlpatterns = [
    {%- if cookiecutter.api_only_mode == 'y' %}
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
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
