from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
