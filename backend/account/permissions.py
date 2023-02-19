"""Permissions for the account app"""

from rest_framework import permissions


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, account):
        return request.user and account == request.user
