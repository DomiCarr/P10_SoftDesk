# apps/projects/serializers.py
from rest_framework import serializers
from .models import Project, Contributor


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
    """
    Serializer for Contributor.
    - Validates that the user is not already a contributor of the project.
    - Only the project AUTHOR can add/remove contributors.
    """
    class Meta:
        model = Contributor
        fields = ["id", "user", "role"]

    def validate(self, data):
        project = data["project"]
        user = data["user"]

        # Check if user is already a contributor
        if Contributor.objects.filter(project=project, user=user).exists():
            raise serializers.ValidationError("This user is already a contributor.")

        # Check that request.user is author of the project
        request_user = self.context["request"].user
        if project.author != request_user:
            raise serializers.ValidationError("Only the project author can add contributors.")

        return data
