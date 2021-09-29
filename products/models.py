from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length = 500,blank=True,null=True)
    price = models.CharField(max_length = 50,blank=True,null=True)
    image = models.ImageField(blank=True,null=True)
    rating = models.CharField(max_length = 50,blank=True,null=True)
    availability = models.CharField(max_length = 50,blank=True,null=True)
    url = models.CharField(max_length = 5000,null=True,blank=True)
    site = models.CharField(max_length = 50,null=True,blank=True)

    def __str__(self):
        return self.name


