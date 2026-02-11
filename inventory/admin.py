from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display=['name','user__id','inventory']
    search_fields=['name','user__id']