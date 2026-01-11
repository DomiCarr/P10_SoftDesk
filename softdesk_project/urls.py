# softdesk_project/urls.py
from django.urls import path, include

urlpatterns = [
    # Inclut toutes les URLs de l'app users
    path("api/", include("apps.users.urls")),
]
