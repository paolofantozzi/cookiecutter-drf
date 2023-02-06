# -*- coding: utf-8 -*-

"""Views for users."""

{%- if cookiecutter.api_only_mode == 'y' %}

from djoser.views import UserViewSet as DjoserUserViewSet
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
{%- else %}

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
{%- endif %}
{%- if cookiecutter.api_only_mode == 'n' %}

from {{ cookiecutter.project_slug }}.users.models import User
{%- else %}

from {{ cookiecutter.project_slug }}.users.serializers import LoginSerializer
from {{ cookiecutter.project_slug }}.users.serializers import LogoutSerializer
{%- endif %}


{%- if cookiecutter.api_only_mode == 'n' %}


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
{%- else %}


class UserViewSet(DjoserUserViewSet):
    """Standard library viewset with destroy modified."""

    def perform_destroy(self, user):
        """Deactivate user instead of deleting it."""
        user.is_active = False
        user.save()


class LogoutView(GenericAPIView):
    """Logout view.

    Originally developed by orehush (https://gist.github.com/orehush/667c79b28fdc94f86746bd15694d1167).
    """

    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated, )

    @extend_schema(
        responses={status.HTTP_200_OK: 'detail: Refresh token invalidated.'},
    )
    def post(self, request, *args):
        """Take refresh token and blacklist it."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Refresh token invalidated.'}, status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    """Change serializer."""

    serializer_class = LoginSerializer
{%- endif %}
