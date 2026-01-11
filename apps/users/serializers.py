# apps/users/serializers.py
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import User


class UserSerializer(serializers.ModelSerializer):
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
        if pw or pw2:  # si un des deux est fourni
            if pw != pw2:
                raise serializers.ValidationError({"password2": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)

        try:
            user.full_clean()  # valide modèle avant save()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop("password2", None)
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.validate_age()
        if password:
            instance.set_password(password)
        instance.save()
        return instance
