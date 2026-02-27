from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import cloudinary.uploader

from . import models, serializers


class ItemViewSet(ModelViewSet):
    serializer_class = serializers.ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Item.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            if models.Item.objects.filter(user=request.user, name=request.data["name"]).exists():
              return Response(
                {"error": "Item already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

            with transaction.atomic():

                image_file = request.FILES.get("image")

                if not image_file:
                    return Response(
                        {"error": "Image is required"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # 🔥 Upload to Cloudinary
                upload_result = cloudinary.uploader.upload(
                    image_file,
                    folder=f"user_{request.user.id}/items"
                )

                image_url = upload_result.get("secure_url")
                public_id = upload_result.get("public_id")

                if not image_url:
                    raise Exception("Image upload failed")

                # 🧠 Copy request data
                data = request.data.copy()
                data["image_url"] = image_url

                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(user=request.user)

                return Response(serializer.data, status=201)

        except Exception as e:
            # 🧹 Cleanup uploaded image if DB fails
            if "public_id" in locals():
                cloudinary.uploader.destroy(public_id)

            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )