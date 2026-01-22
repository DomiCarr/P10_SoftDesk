# apps/users/serializers.py

# serializers: The Django Rest Framework (DRF) tool
# that transforms Python objects into JSON (and vice versa).
from rest_framework import serializers

# DjangoValidationError: The standard Django error,
# imported here under an alias to avoid confusion with DRF's.
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import User


class UserSerializer(serializers.ModelSerializer):
    # # ModelSerializer: Indicates that this serializer is linked to a specific model.
    # password & password2: These fields are defined manually. write_only=True is crucial:
    # it means the password can be sent by the user but will never be returned by the API (security).
    password = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
            "created_time",
            "password",
            "password2",
        ]
        read_only_fields = ["id", "created_time"]

    def validate(self, data):
        pw = data.get("password")
        pw2 = data.get("password2")
        if pw or pw2:
            if pw != pw2:
                raise serializers.ValidationError({"password2": "Passwords must match."})
        return data

    def create(self, validated_data):
        # Remove password2 as the model does not need it and extract the raw password
        validated_data.pop("password2")
        password = validated_data.pop("password")

        # Initialize the user instance with remaining validated data
        user = User(**validated_data)

        # Crucial: hashes the password (transforms it into unreadable code) before storage
        user.set_password(password)

        try:
            # Force model-level validation rules (e.g., age >= 15) before saving
            user.full_clean()
        except DjangoValidationError as e:
            # If the model finds an error, return it cleanly to the API user
            raise serializers.ValidationError(e.message_dict)

        user.save()
        return user

    def update(self, instance, validated_data):
        # instance: Represents the existing user that we want to modify
        validated_data.pop("password2", None)
        password = validated_data.pop("password", None)

        # Loop through the dictionary: attr is the field name (e.g., 'email'),
        # and value is the new data (e.g., 'new@mail.com')
        for attr, value in validated_data.items():
            # Dynamically update the user object
            setattr(instance, attr, value)

        # instance.validate_age(): Manually check the age here
        # to ensure a update doesn't make the user too young
        instance.validate_age()

        if password:
            instance.set_password(password)

        # instance.save(): Save the changes.
        # This will also trigger the model's full_clean for security
        instance.save()
        return instance
