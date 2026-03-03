from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    profile_image_url = models.CharField(   # 👈 made uniform
        max_length=1000,
        blank=True,
        null=True,
        help_text="Cloudinary URL for user's profile picture"
    )
    profile_image_public_id = models.CharField(max_length=1000,blank=True,null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.email