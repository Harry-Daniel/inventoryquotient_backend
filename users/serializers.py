from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.db import transaction
import cloudinary.uploader

from . import models


class CustomUserSerializer(BaseUserSerializer):

    full_name = serializers.SerializerMethodField()

    profile_image = serializers.ImageField(
        write_only=True,
        required=False
    )

    class Meta(BaseUserSerializer.Meta):
        model = models.User
        fields = (
            "id",
            "email",
            "username",
            "profile_image_url",
            "profile_image_public_id",
            "profile_image",  
            "full_name",
        )
        read_only_fields = (
            "email",
            "profile_image_url",
            "profile_image_public_id",
            "full_name",
        )

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

     
    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                # 👇 Pop image if provided
                image_file = validated_data.pop("profile_image", None)

                if image_file:
                    # 🔥 If user already has image → overwrite
                    if instance.profile_image_public_id:
                        upload_result = cloudinary.uploader.upload(
                            image_file,
                            public_id=instance.profile_image_public_id,
                            overwrite=True,
                            invalidate=True,
                        )
                    else:
                        upload_result = cloudinary.uploader.upload(image_file)

                    image_url = upload_result.get("secure_url")
                    public_id = upload_result.get("public_id")

                    if not (image_url and public_id):
                        raise Exception("Cloudinary upload failed")

                    instance.profile_image_url = image_url
                    instance.profile_image_public_id = public_id

                # 👇 Update other editable fields (like username)
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)

                instance.save()
                return instance

        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})
        

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": "Email or password is incorrect"
    }