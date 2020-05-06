# -*- coding: utf-8 -*-

"""Views for users."""
{%- if cookiecutter.api_only_mode == 'y' %}

from typing import List
from typing import Type

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework_simplejwt.views import token_obtain_pair
from rest_framework_simplejwt.views import token_refresh
{%- else %}

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
{%- endif %}

from {{ cookiecutter.project_slug }}.users.models import User
{%- if cookiecutter.api_only_mode == 'y' %}
from {{ cookiecutter.project_slug }}.users.permissions import IsStaffOrIsMe
from {{ cookiecutter.project_slug }}.users.serializers import LoginRefreshResponseSerializer
from {{ cookiecutter.project_slug }}.users.serializers import LogoutSerializer
from {{ cookiecutter.project_slug }}.users.serializers import UserRegistrationSerializer
from {{ cookiecutter.project_slug }}.users.serializers import UserSerializer
from {{ cookiecutter.project_slug }}.users.serializers import UserUpdateSerializer
{%- endif %}


{%- if cookiecutter.api_only_mode == 'n' %}


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
{%- else %}


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Create, Update, List and retrieve users.

    When an id is request it is possible to use `me` instead of an id,
    to return self.
    """

    def get_queryset(self):
        """Return all the users if is staff, self otherwise."""
        if getattr(self, 'swagger_fake_view', False):  # noqa: WPS425
            # Queryset just for schema generation metadata
            return User.objects.none()
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        """Return the user requested if it is staff or self, 404 otherwise."""
        pk = self.kwargs['pk']
        if pk == 'me':
            pk = self.request.user.pk
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, user)
        return user

    def get_serializer_class(self):
        """Return detailed serializer only for retrieve."""
        if self.action in {'update', 'partial_update'}:  # type: ignore  # mypy plugin bug
            return UserUpdateSerializer
        elif self.action == 'create':  # type: ignore
            return UserRegistrationSerializer
        return UserSerializer

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this view requires."""
        permission_classes: List[Type[BasePermission]] = []
        if self.action == 'create':  # type: ignore
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, IsStaffOrIsMe]
        return [permission() for permission in permission_classes]


class LogoutView(GenericAPIView):
    """Logout view.

    Originally developed by orehush (https://gist.github.com/orehush/667c79b28fdc94f86746bd15694d1167).
    """

    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated, )

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: 'detail: Refresh token invalidated.',
    })
    def post(self, request, *args):
        """Take refresh token and blacklist it."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Refresh token invalidated.'}, status=status.HTTP_200_OK)


login_view = swagger_auto_schema(
    method='post',
    responses={
        status.HTTP_200_OK: LoginRefreshResponseSerializer,
        status.HTTP_401_UNAUTHORIZED: 'code: authentication_failed',
    },
)(token_obtain_pair)

refresh_token_view = swagger_auto_schema(
    method='post',
    responses={
        status.HTTP_200_OK: LoginRefreshResponseSerializer,
        status.HTTP_401_UNAUTHORIZED: 'code: token_not_valid',
    },
)(token_refresh)

{%- endif %}
