# -*- coding: utf-8 -*-

"""Api routers registering."""

from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from {{ cookiecutter.project_slug }}.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('users', UserViewSet)


app_name = 'api'
urlpatterns = router.urls
