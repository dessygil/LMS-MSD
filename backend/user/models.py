from django.db import models
import uuid

# Email should be unique
#primary key should UUID
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True, verbose_name="Email Address", max_length=255)
    name = models.CharField(max_length=255, null=False, blank=False)
    
