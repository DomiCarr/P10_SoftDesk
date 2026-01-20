# apps/projects/urls.py
from django.urls import path, include
from rest_framework_nested import routers
from .views import ProjectViewSet, IssueViewSet, CommentViewSet

# Main router
router = routers.SimpleRouter()
router.register(r"projects", ProjectViewSet, basename="projects")

# Nested router for issues: /api/projects/{project_pk}/issues/
issues_router = routers.NestedSimpleRouter(
    router,
    r"projects",
    lookup="project"
)
issues_router.register(
    r"issues",
    IssueViewSet,
    basename="project-issues"
)

# Nested router for comments: /api/projects/{project_pk}/issues/{issue_pk}/comments/
comments_router = routers.NestedSimpleRouter(
    issues_router,
    r"issues",
    lookup="issue"
)
comments_router.register(
    r"comments",
    CommentViewSet,
    basename="issue-comments"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(issues_router.urls)),
    path("", include(comments_router.urls)),
]