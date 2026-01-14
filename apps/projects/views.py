# apps/projects/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer
from .permissions import IsProjectContributor, IsProjectAuthor


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Projects.
    - Users see only projects where they are contributors.
    - Only the AUTHOR can update, delete, or manage contributors.
    """
    serializer_class = ProjectSerializer

    def get_queryset(self):
        # Only return projects where request.user is a contributor
        return Project.objects.filter(contributors__user=self.request.user).distinct()

    def get_permissions(self):
        """
        Assign permissions depending on the action.
        """
        if self.action in ['update', 'partial_update', 'destroy', 'add_contributor', 'remove_contributor']:
            permission_classes = [IsAuthenticated, IsProjectAuthor]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated, IsProjectContributor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["post"], url_path="contributors")
    def add_contributor(self, request, pk=None):
        """
        Add a contributor to the project (AUTHOR only).
        """
        project = self.get_object()
        serializer = ContributorSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"], url_path="contributors/(?P<user_id>[^/.]+)")
    def remove_contributor(self, request, pk=None, user_id=None):
        """
        Remove a contributor from the project (AUTHOR only).
        """
        project = self.get_object()
        contributor = get_object_or_404(Contributor, project=project, user_id=user_id)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
