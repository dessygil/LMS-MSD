from django.db import models

class User(models.Model):
    email = models.EmailField(primary_key=True, verbose_name="Email Address", max_length=255)
    name = models.CharField(max_length=255, null=False, blank=False)
    
