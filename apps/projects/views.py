# apps/projects/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Project, Contributor, Comment, Issue
from .serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer
)
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
        serializer = ContributorSerializer(
            data=request.data,
            context={
                "request": request,
                "project": project,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project)

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


class IssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Issues.
    """
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.filter(
            project_id=self.kwargs["project_pk"],
            project__contributors__user=self.request.user
        ).distinct()

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsResourceAuthor()]
        return [IsAuthenticated(), IsProjectContributor()]

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        serializer.save(author=self.request.user, project=project)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comments.
    """
    serializer_class = CommentSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        return Comment.objects.filter(
            issue_id=self.kwargs["issue_pk"],
            issue__project__contributors__user=self.request.user
        ).distinct()

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsResourceAuthor()]
        return [IsAuthenticated(), IsProjectContributor()]

    def perform_create(self, serializer):
        issue = get_object_or_404(Issue, pk=self.kwargs["issue_pk"])
        serializer.save(author=self.request.user, issue=issue)