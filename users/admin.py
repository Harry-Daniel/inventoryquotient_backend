from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display=['id','first_name','last_name','username']
    search_fields=['first_name','last_name']
