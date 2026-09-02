from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class tbl_UserProfile(models.Model):
    name = models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    contact = models.CharField(max_length=20,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    address = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/',null=True,blank=True)
    def __str__(self):
        return self.user.username