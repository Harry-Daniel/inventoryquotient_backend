from django.db import models
from django.core.validators import MinValueValidator


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)

    image_url = models.CharField(
        max_length=1000,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name