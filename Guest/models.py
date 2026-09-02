from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class tbl_registration(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(unique=True)
    user_contact = models.CharField(max_length=20)
    user_address = models.TextField(default='', blank=True)
    user_password = models.CharField(max_length=100)
    def __str__(self):
        return self.user_name
