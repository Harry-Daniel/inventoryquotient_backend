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
            if models.Item.objects.filter(user=request.user, name__iexact=request.data["name"]).exists():
              return Response(
                {"error": "Item already exists, search and update it instead."},
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

                if not (image_url and public_id):
                    raise Exception("Image upload failed")

                # 🧠 Copy request data
                data = request.data.copy()
                data["image_url"] = image_url
                data["image_public_id"]=public_id

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
    
    def update(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                partial = kwargs.pop("partial", False)
                instance = self.get_object()

                image_file = request.FILES.get("image")
                image_url_from_client = request.data.get("image_url")

                data = request.data.copy()

                # 🖼 CASE 1: New image file uploaded → overwrite in Cloudinary
                if image_file:
                    if not instance.image_public_id:
                        return Response(
                            {"error": "Existing image public_id not found"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    upload_result = cloudinary.uploader.upload(
                        image_file,
                        public_id=instance.image_public_id,
                        overwrite=True,
                        invalidate=True,
                    )

                    image_url = upload_result.get("secure_url")
                    public_id = upload_result.get("public_id")

                    if not (image_url and public_id):
                        raise Exception("Image overwrite failed")

                    data["image_url"] = image_url
                    data["image_public_id"] = public_id

                # 🌐 CASE 2: Existing image URL sent → just reuse it
                elif image_url_from_client:
                    data["image_url"] = image_url_from_client
                    data["image_public_id"] = instance.image_public_id

                # 🔒 CASE 3: No image data sent → keep existing image
                else:
                    data["image_url"] = instance.image_url
                    data["image_public_id"] = instance.image_public_id

                # 🧠 Continue normal update
                serializer = self.get_serializer(
                    instance, data=data, partial=partial
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()

                return Response(serializer.data, status=200)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )