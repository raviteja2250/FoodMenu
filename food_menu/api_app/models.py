from django.db import models

# Create your models here.


class Category(models.Model):

    category_name = models.CharField(max_length=50,unique=True)
    category_detail = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.category_name


class MenuItem(models.Model):
    item_id = models.PositiveIntegerField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items',null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    thumb_image_url = models.CharField(max_length=500, null=True, blank=True)
