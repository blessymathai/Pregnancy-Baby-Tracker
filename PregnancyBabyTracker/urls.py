from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('admin/', admin.site.urls),

    # Guest Module
    path('', include('Guest.urls')),

    # User Module
    path('User/', include('User.urls')),

    # Doctor Module
    path('Doctor/', include('Doctor.urls')),

    # Administrator Module
    path('Administrator/', include('Administrator.urls')),
]