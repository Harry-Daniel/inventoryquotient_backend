from django.db import models

# Create your models here.
class Item(models.Model):
    title= models.CharField(max_length=255)
    slug=models.SlugField()
    description= models.TextField()
    last_update=models.DateTimeField(auto_now=True)

class ItemImage(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    image=image_url = models.CharField(max_length=1000, blank=True, null=True)


