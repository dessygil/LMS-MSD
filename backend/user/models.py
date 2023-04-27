from django.db import models

# Email should be unique
#primary key should UUID
class User(models.Model):
    email = models.EmailField(primary_key=True, verbose_name="Email Address", max_length=255)
    name = models.CharField(max_length=255, null=False, blank=False)
    
