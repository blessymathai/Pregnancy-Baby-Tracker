from django.urls import path
from Guest import views
app_name='Guest'
urlpatterns = [
    path('', views.HomePage, name='HomePage'),
    path('Login/', views.Login, name='Login'),
    path('UserRegistration/', views.UserRegistrationView, name='UserRegistration'),
    path('Logout/',views.Logout,name='Logout'),
    # path('UserDashboard/',views.UserDashboard,name='UserDashboard'),
]