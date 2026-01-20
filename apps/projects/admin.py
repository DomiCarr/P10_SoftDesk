# projects/admin.py
from django.contrib import admin
from .models import Project, Contributor


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    pass
