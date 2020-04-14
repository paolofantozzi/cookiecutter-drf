# -*- coding: utf-8 -*-

"""Urls for users."""

from django.urls import path

from {{ cookiecutter.project_slug }}.users.views import user_detail_view
from {{ cookiecutter.project_slug }}.users.views import user_redirect_view
from {{ cookiecutter.project_slug }}.users.views import user_update_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
