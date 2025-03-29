from django.db import models
from django.utils import timezone
# Create your models here.
from django.db import models

class Admin(models.Model):
    username=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

class Category(models.Model):
    category=models.CharField(max_length=100)


class TblService(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    service_name = models.CharField(max_length=200)


