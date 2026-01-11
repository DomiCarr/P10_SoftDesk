# apps/users/permissions.py
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Permet uniquement au propriétaire de modifier/supprimer ses données.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
