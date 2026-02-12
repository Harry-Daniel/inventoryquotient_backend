from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
# Create your views here.

class ItemViewSet(ModelViewSet):
    serializer_class = serializers.ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Item.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)