# apps/projects/permissions.py
from rest_framework.permissions import BasePermission


class IsProjectContributor(BasePermission):
    """
    Allow access only if the user is a contributor of the project.
    """

    def has_object_permission(self, request, view, obj):
        return obj.contributors.filter(user=request.user).exists()


class IsProjectAuthor(BasePermission):
    """
    Allow access only if the user is the author of the project.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
