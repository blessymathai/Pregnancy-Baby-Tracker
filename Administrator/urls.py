from django.urls import path
from . import views
app_name = 'Administrator'

urlpatterns = [
    path('', views.AdminDashboard, name='AdminDashboard'),
    path('ManageUser/', views.ManageUser, name='ManageUser'),
    path('ManageDoctor/', views.ManageDoctor, name='ManageDoctor'),
    path('ManageMilestones/', views.ManageMilestones, name='ManageMilestones'),
    path('ManageNutrition/', views.ManageNutrition, name='ManageNutrition'),
    path('ManageMedicines/', views.ManageMedicines, name='ManageMedicines'),
    path('Reports/', views.Reports, name='Reports'),
    path('UploadDataset/', views.UploadDataset, name='UploadDataset'),
    path('ChatBox/',views.ChatBox,name='ChatBox'),
]