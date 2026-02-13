from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from . import models


class CustomUserSerializer(BaseUserSerializer):

    full_name = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = models.User
        fields = (
            "id",
            "email",
            "username",
            "profile_image_url",
            "full_name",
        )
        read_only_fields = ("email", "full_name")

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()