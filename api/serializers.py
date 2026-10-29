
from rest_framework import serializers
from .models import ReadingMaterials, Ratings

import secrets
import string

from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "first_name", "username", "password"]
        read_only_fields = ["id", "username", "password"]

    def create(self, validated_data):
        full_name = validated_data["first_name"].strip()

        if not full_name:
            raise serializers.ValidationError({
                "first_name": "Full name is required."
            })

        validated_data["first_name"] = full_name

        with transaction.atomic():
            # Generate the next sequential username.
            number = 1

            while True:
                username = f"student2026{number}"

                if not User.objects.filter(username=username).exists():
                    break

                number += 1

            # Generate a random password and retry if it already exists.
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
            
            while True:
                password = "".join(
                    secrets.choice(alphabet) for _ in range(16)
                )

                if not User.objects.filter(
                    password__exact=password
                ).exists():
                    break

            user = User(
                username=username,
                **validated_data
            )
            user.set_password(password)
            user.save()

            # Return the plaintext password only for this creation response.
            user.generated_password = password

        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)

        generated_password = getattr(
            instance, "generated_password", None
        )

        if generated_password:
            data["password"] = generated_password

        return data


class ReadingMaterialsSerializer(serializers.ModelSerializer):
    student_count = serializers.IntegerField(read_only=True, default=0)
    word_count = serializers.SerializerMethodField()

    class Meta:
        model = ReadingMaterials
        fields = [
            "id",
            "title",
            "difficulty",
            "content",
            "date_added",
            "student_count",
            "word_count",
        ]
        read_only_fields = [
            "id",
            "date_added",
            "student_count",
            "word_count",
        ]

    def get_word_count(self, obj):
        return len((obj.content or "").split())



class StudentDropdownSerializer(serializers.ModelSerializer):
    """Fields needed to populate the student dropdown."""

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]


class RatingsSerializer(serializers.ModelSerializer):
    """Create and retrieve reading assessment ratings."""

    student_name = serializers.SerializerMethodField(read_only=True)
    material_title_text = serializers.CharField(
        source="material_title.title",
        read_only=True
    )

    class Meta:
        model = Ratings
        fields = [
            "id",
            "student",
            "student_name",
            "material_title",
            "material_title_text",
            "rate",
            "feedback",
            "created",
        ]
        read_only_fields = [
            "id",
            "student_name",
            "material_title_text",
            "created",
        ]

    def get_student_name(self, obj):
        student = obj.student
        full_name = f"{student.first_name} {student.last_name}".strip()
        return full_name or student.get_username()

    def validate_student(self, value):
        if not value:
            raise serializers.ValidationError("Please select a student.")
        return value

    def validate_material_title(self, value):
        if not value:
            raise serializers.ValidationError(
                "Please select a reading material."
            )
        return value

    def validate_rate(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("A rating is required.")
        return value.strip()
