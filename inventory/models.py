from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Item(models.Model):
    name= models.CharField(max_length=255)
    description= models.TextField()
    inventory=models.IntegerField(validators=[MinValueValidator(0)])
    last_update=models.DateTimeField(auto_now=True)

class ItemImage(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE,related_name='image')
    image=image_url = models.CharField(max_length=1000, blank=True, null=True)


