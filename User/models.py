from django.db import models
from django.contrib.auth.models import User
from Guest.models import tbl_registration

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

class tbl_PregnancyTracker(models.Model):
    user = models.ForeignKey(
        tbl_registration,
        on_delete=models.CASCADE,
        related_name='pregnancy_tracker'
    )
    last_period_date = models.DateField()
    expected_delivery_date = models.DateField()
    current_week = models.PositiveIntegerField(default=1)
    weight = models.FloatField(null=True,blank=True)
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return (
            self.user.user_name
            + " - Week "
            + str(self.current_week)
        )
