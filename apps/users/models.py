# apps/users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Inherited fields from AbstractUser:
    - username
    - first_name
    - last_name
    - email
    - password
    - groups
    - user_permissions
    - is_staff
    - is_active
    - is_superuser
    - last_login
    - date_joined

    Inherited methods from AbstractUser / PermissionsMixin:
    - set_password()
    - check_password()
    - get_full_name()
    - get_short_name()
    - has_perm()
    - has_perms()
    - has_module_perms()
    - save()
    - delete()
    """

    # Custom fields for SoftDesk
    age = models.PositiveIntegerField()
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def validate_age(self):
        """
        Raise ValidationError if the user's age is less than 15.
        """
        if self.age < 15:
            raise ValidationError("User must be at least 15 years old")

    def clean(self):
        """
        Override clean() to automatically validate fields when using
        full_clean(), including serializers or admin forms.
        """
        super().clean()
        self.validate_age()

    def save(self, *args, **kwargs):
        """
        Override save() to ensure full_clean() is called before saving,
        enforcing model-level validation automatically.
        """
        self.full_clean()  # triggers clean() -> validate_age()
        super().save(*args, **kwargs)
