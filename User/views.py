# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from .models import tbl_UserProfile

def UserDashboard(request):
    if "user_id" not in request.session:
        return redirect("Guest:Login")
    return render(request,"User/UserDashboard.html")

# def UserDashboard(request):
#     context = {
#         'current_week': 1,
#         'total_weeks': 40,
#         'week_milestone': (
#             "Your body is preparing for pregnancy. "
#             "Maintain a healthy lifestyle and start tracking your pregnancy."
#         ),
#         'symptoms': [
#             "Mild abdominal discomfort",
#             "Feeling tired",
#         ],
#         'mood': "Happy",
#     }
#     return render(request, 'User/user_dashboard.html', context)

def PregnancyProfile(request): 
    return render(request, 'User/PregnancyProfile.html')

def PregnancyTracker(request): 
    return render(request, 'User/PregnancyTracker.html')

def BabyGrowth(request): 
    return render(request, 'User/BabyGrowth.html')

def Nutrition(request): 
    return render(request, 'User/Nutrition.html')

def Appointments(request): 
    return render(request, 'User/Appointments.html')

def MyProfile(request):
    profile = tbl_UserProfile.objects.get(name=request.user)
    if request.method == "POST":
        request.user.first_name = request.POST.get('txt_name')
        request.user.email = request.POST.get('txt_email')
        request.user.save()
        profile.age = request.POST.get('txt_age')
        profile.contact = request.POST.get('txt_contact')
        profile.date_of_birth = request.POST.get('txt_date_of_birth')
        profile.address = request.POST.get('txt_address')
        profile.save()
        return redirect('User:UserDashboard')
    return render(request, 'User/MyProfile.html', {'profile': profile})

def Profile(request): 
    return render(request, 'User/Profile.html')

def MyProfile(request):
    if not request.user.is_authenticated:
        return redirect('Guest:Login')
    profile, created = tbl_UserProfile.objects.get_or_create(name=request.user)
    if request.method == "POST":
        request.user.first_name = request.POST.get('txt_name')
        request.user.email = request.POST.get('txt_email')
        request.user.save()
        profile.save()
        return redirect('User:UserDashboard')
    return render(request, 'User/MyProfile.html', {'profile': profile})

def EditProfile(request): 
    return render(request, 'User/EditProfile.html')

def ChangePassword(request): 
    return render(request, 'User/ChangePassword.html')
