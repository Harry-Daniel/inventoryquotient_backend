from . import models
from rest_framework import serializers

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = "__all__"
        read_only_fields = ("user",)

