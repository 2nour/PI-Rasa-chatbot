from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Customers(models.Model):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    cin = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    birthdate = models.DateTimeField(blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    login = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)



    objects = models.Manager()
