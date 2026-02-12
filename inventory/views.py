from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from . import models
from . import serializers
# Create your views here.

class ItemViewSet(ModelViewSet):
    queryset=models.Item.objects.all()
    serializer_class=serializers.ItemSerializer