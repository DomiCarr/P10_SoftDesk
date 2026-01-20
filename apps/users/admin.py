# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    readonly_fields = BaseUserAdmin.readonly_fields + ("created_time",)

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Custom fields",
            {
                "fields": (
                    "age",
                    "can_be_contacted",
                    "can_data_be_shared",
                )
            },
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Custom fields",
            {
                "fields": (
                    "age",
                    "can_be_contacted",
                    "can_data_be_shared",
                )
            },
        ),
    )
