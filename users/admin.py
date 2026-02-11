from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.User)
class ItemAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','username']