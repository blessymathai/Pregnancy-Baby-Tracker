from django.urls import path
from . import views

app_name = 'Doctor'

urlpatterns = [
    path('Registration/', views.DoctorRegistrationView, name='DoctorRegistration'),
    path('', views.DoctorDashboard, name='DoctorDashboard'),
    path('Patients/', views.Patients, name='Patients'),
    path('Appointments/', views.Appointments, name='Appointments'),
    path('PregnancyRecords/', views.PregnancyRecords, name='PregnancyRecords'),
    path('BabyRecords/', views.BabyRecords, name='BabyRecords'),
    path('Prescriptions/', views.Prescriptions, name='Prescriptions'),
    path('Messages/', views.Messages, name='Messages'),
    path('ChatBox/', views.ChatBox, name='ChatBox'),
    path('Logout/', views.Logout, name='Logout'),
]