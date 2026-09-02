from django.urls import path
from User import views
app_name='User'
urlpatterns = [
    path('UserDashboard/', views.UserDashboard, name='UserDashboard'),
    path('PregnancyProfile/', views.PregnancyProfile, name='PregnancyProfile'),
    path('PregnancyTracker/', views.PregnancyTracker, name='PregnancyTracker'),
    path('BabyGrowth/', views.BabyGrowth, name='BabyGrowth'),
    path('Nutrition/', views.Nutrition, name='Nutrition'),
    path('Appointments/', views.Appointments, name='Appointments'),
    # path('Messages/', views.Messages, name='Messages'),
    path('Profile/', views.Profile, name='Profile'),
    path('MyProfile/', views.MyProfile, name='MyProfile'),
    path('EditProfile/', views.EditProfile, name='EditProfile'),
    path('ChangePassword/', views.ChangePassword, name='ChangePassword'),
]