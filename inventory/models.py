from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Item(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="items"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    image_url = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name