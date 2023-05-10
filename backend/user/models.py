from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True, verbose_name="Email Address", max_length=255)
    name = models.CharField(max_length=255, null=False, blank=False)
    lab_manager = models.BooleanField(default=False)
