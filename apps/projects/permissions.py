# apps/projects/permissions.py
from rest_framework.permissions import BasePermission
from .models import Contributor


class IsProjectContributor(BasePermission):
    """
    Allow access only if the user is a contributor of the project.
    """

    def has_permission(self, request, view):
        # On récupère l'ID du projet dans l'URL pour vérifier l'accès
        project_id = view.kwargs.get("project_pk")
        if not project_id:
            return False
        return Contributor.objects.filter(project_id=project_id, user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        # Pour les détails d'un projet spécifique
        return obj.contributors.filter(user=request.user).exists()


class IsProjectAuthor(BasePermission):
    """
    Allow access only if the user is the author of the project.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsResourceAuthor(BasePermission):
    """
    Allow access only if the user is the author of the issue or comment.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user