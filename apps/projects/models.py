# apps/projects/models.py
from django.conf import settings
from django.db import models
import uuid


class Project(models.Model):
    """
    Project model with author and type.
    """

    # Project types with DB value and display label
    class Type(models.TextChoices):
        BACKEND = "backend", "Backend"
        FRONTEND = "frontend", "Frontend"
        IOS = "ios", "iOS"
        ANDROID = "android", "Android"

    # Project title and description
    title = models.CharField(max_length=128)
    description = models.TextField()

    # Project type, constrained by Type choices
    type = models.CharField(
        max_length=20,
        choices=Type.choices,
    )

    # Creation timestamp
    created_time = models.DateTimeField(auto_now_add=True)

    # Author link
    # CASCADE: delete project if author deleted
    # related_name: user.authored_projects.all() gives all authored projects
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_projects",
    )

    # String representation
    def __str__(self):
        return self.title


class Contributor(models.Model):
    """
    Django model to link a User to a Project.

    Manages roles (AUTHOR / CONTRIBUTOR) and prevents duplicate contributions.
    Ensures that a user can contribute only once per project.
    """

    # Role constants
    ROLE_AUTHOR = "AUTHOR"
    ROLE_CONTRIBUTOR = "CONTRIBUTOR"

    # Choices for the role field
    ROLE_CHOICES = [
        (ROLE_AUTHOR, "Author"),
        (ROLE_CONTRIBUTOR, "Contributor"),
    ]

    # Link to the User model
    # CASCADE: delete contributions if the user is deleted
    # related_name: user.contributions.all() returns all contributions of the user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributions",
    )

    # Link to the Project model
    # CASCADE: delete contributions if the project is deleted
    # related_name: project.contributors.all() returns all contributors of the project
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        related_name="contributors",
    )

    # Role of the user in the project (AUTHOR or CONTRIBUTOR)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        # Ensure a user can only contribute once per project
        unique_together = ("user", "project")

    # Human-readable representation in admin and shell
    def __str__(self):
        return f"{self.user} - {self.project} ({self.role})"


class Issue(models.Model):
    """
    Issue model linked to a Project.
    """
    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    class Tag(models.TextChoices):
        BUG = "BUG", "Bug"
        FEATURE = "FEATURE", "Feature"
        TASK = "TASK", "Task"

    class Status(models.TextChoices):
        TODO = "To Do", "To Do"
        IN_PROGRESS = "In Progress", "In Progress"
        FINISHED = "Finished", "Finished"

    title = models.CharField(max_length=128)
    description = models.TextField()
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )
    tag = models.CharField(
        max_length=10, choices=Tag.choices, default=Tag.TASK
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.TODO
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_issues"
    )
    assigned_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_issues"
    )
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """
    Comment model linked to an Issue.
    """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.uuid} by {self.author}"