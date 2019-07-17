from django.db import models

# Create your models here.
class LoginUser(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
