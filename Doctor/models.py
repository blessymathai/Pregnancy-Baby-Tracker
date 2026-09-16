from django.db import models
from Guest.models import tbl_registration
from django.utils import timezone
# Create your models here.

class tbl_Doctor(models.Model):
    SPECIALTIES = [('Obstetrics & Gynecology','Obstetrics & Gynecology'),('Pediatrics','Pediatrics'),('General Medicine','General Medicine')]
    user = models.OneToOneField(tbl_registration, on_delete=models.CASCADE, related_name='doctor_profile')
    name = models.CharField(max_length=120)
    specialization = models.CharField(max_length=100, choices=SPECIALTIES, default='General Medicine')
    qualification = models.CharField(max_length=150, blank=True)
    license_no = models.CharField(max_length=100, blank=True)
    experience = models.PositiveIntegerField(default=0)
    hospital = models.CharField(max_length=150, blank=True)
    contact = models.CharField(max_length=20, blank=True)
    available = models.BooleanField(default=True)

    class Meta:
        db_table = 'tbl_Doctor'

    # def __str__(self):
    #     return f'Dr. {self.name}'

class tbl_Appointment(models.Model):
    STATUS = [('Pending','Pending'),('Approved','Approved'),('Completed','Completed'),('Cancelled','Cancelled')]
    patient = models.ForeignKey(tbl_registration, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(tbl_Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_Appointment'
        ordering = ['-appointment_date','-appointment_time']

class tbl_Prescription(models.Model):
    patient = models.ForeignKey(tbl_registration, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(tbl_Doctor, on_delete=models.CASCADE, related_name='prescriptions')
    medicine = models.CharField(max_length=150)
    dosage = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)
    prescribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_Prescription'
        ordering = ['-prescribed_at']

class tbl_Message(models.Model):
    sender = models.ForeignKey(tbl_registration, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(tbl_registration, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_Message'
        ordering = ['sent_at']
