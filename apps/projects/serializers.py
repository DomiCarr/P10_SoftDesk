# apps/projects/serializers.py
from rest_framework import serializers
from .models import Project, Contributor, Comment, Issue


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project.
    - author and created_time are read-only.
    - On creation, author = request.user.
    - Automatically creates a Contributor with role AUTHOR.
    """
    author = serializers.StringRelatedField(read_only=True)
    created_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = ["id", "title", "description", "type", "author", "created_time"]

    def create(self, validated_data):
        # Assign the current user as author
        user = self.context["request"].user
        project = Project.objects.create(author=user, **validated_data)

        # Create Contributor entry as AUTHOR
        Contributor.objects.create(
            user=user,
            project=project,
            role=Contributor.ROLE_AUTHOR
        )
        return project


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["id", "user", "role"]

    def validate(self, data):
        request = self.context["request"]
        project = self.context["project"]
        user = data["user"]

        if Contributor.objects.filter(project=project, user=user).exists():
            raise serializers.ValidationError(
                "This user is already a contributor."
            )

        if project.author != request.user:
            raise serializers.ValidationError(
                "Only the project author can add contributors."
            )

        return data


class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer for Issue.
    """
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ["author", "project", "created_time"]

    def validate_assigned_user(self, value):
        # Check if the assigned user is a contributor of the project
        project_id = self.context["view"].kwargs.get("project_pk")
        if value and not Contributor.objects.filter(
            project_id=project_id, user=value
        ).exists():
            raise serializers.ValidationError(
                "Assigned user must be a contributor of this project."
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment.
    """
    author = serializers.StringRelatedField(read_only=True)
    created_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ["uuid", "description", "author", "issue", "created_time"]
        read_only_fields = ["uuid", "issue"]

    def create(self, validated_data):
        # validated_data already contains 'issue' and 'author'
        # passed by serializer.save() in the view
        return super().create(validated_data)