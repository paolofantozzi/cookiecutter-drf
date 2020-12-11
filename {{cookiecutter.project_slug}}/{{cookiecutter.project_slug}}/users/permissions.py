# -*- coding: utf-8 -*-

"""Permissions based on user."""

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import IsAuthenticated


class IsStaffOrReadOnly(permissions.BasePermission):
    """Gives pemission if the user is staff or if the method is readonly."""

    def has_permission(self, request, view):
        """Check if it is staff or if it is a readonly method."""
        if not super().has_permission(request, view):
            return False

        return request.user.is_staff or (request.method in SAFE_METHODS)


class OnlyStaff(IsAuthenticated):
    """Only staff users have access."""

    def has_permission(self, request, view):
        """Check if it is staff."""
        if not super().has_permission(request, view):
            return False
        return request.user.is_staff


class IsStaffOrIsMe(permissions.BasePermission):
    """Gives permission if the is user is staff or if it is itself."""

    def has_object_permission(self, request, view, obj):  # noqa: WPS110
        """Check if it is staff or itself."""
        if (request.user.pk == obj.id) or (obj.id == 'me'):
            return True
        if request.user.is_staff:
            return True
        return False
