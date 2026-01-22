# apps/users/models.py

# AbstractUser: A template model provided by Django containing
# all standard user fields (username, password, email).
# We import it to avoid recreating a user system from scratch.
from django.contrib.auth.models import AbstractUser

# models: A toolbox used to define database columns
# (numbers, text, dates).
from django.db import models

# ValidationError: A specific tool to tell the program:
# "Stop everything, there is an error in the entered data".
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

    # Custom and overridden methods for SoftDesk
    def validate_age(self):
        # CUSTOM: Specific business logic to check user age
        """
        Raise ValidationError if the user's age is less than 15.
        """
        if self.age < 15:
            raise ValidationError("User must be at least 15 years old")

    def clean(self):
        # OVERRIDDEN: Extends Django's standard validation process
        """
        By writing super().clean(), you are basically saying: "First,
        execute Django's standard validation code, then, once that is
        done, proceed with my custom age verification."
        It is a security measure to stack rules instead of replacing them.
        """
        super().clean()
        self.validate_age()

    def save(self, *args, **kwargs):
        # OVERRIDDEN: Extends Django's standard save process
        """
        Force model validation before saving to database.
        This ensures all custom rules (like age) are always enforced.
        """
        self.full_clean()  # triggers clean() -> validate_age()
        super().save(*args, **kwargs)
