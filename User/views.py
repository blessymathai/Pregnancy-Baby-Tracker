# # Create your views here.
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required 
# from .models import tbl_UserProfile

# def UserDashboard(request):
#     if "user_id" not in request.session:
#         return redirect("Guest:Login")
#     return render(request,"User/UserDashboard.html")

# # def UserDashboard(request):
# #     context = {
# #         'current_week': 1,
# #         'total_weeks': 40,
# #         'week_milestone': (
# #             "Your body is preparing for pregnancy. "
# #             "Maintain a healthy lifestyle and start tracking your pregnancy."
# #         ),
# #         'symptoms': [
# #             "Mild abdominal discomfort",
# #             "Feeling tired",
# #         ],
# #         'mood': "Happy",
# #     }
# #     return render(request, 'User/user_dashboard.html', context)

# def PregnancyProfile(request): 
#     return render(request, 'User/PregnancyProfile.html')

# def PregnancyTracker(request): 
#     return render(request, 'User/PregnancyTracker.html')

# def BabyGrowth(request): 
#     return render(request, 'User/BabyGrowth.html')

# def Nutrition(request): 
#     return render(request, 'User/Nutrition.html')

# def Appointments(request): 
#     return render(request, 'User/Appointments.html')

# def MyProfile(request):
#     profile = tbl_UserProfile.objects.get(name=request.user)
#     if request.method == "POST":
#         request.user.first_name = request.POST.get('txt_name')
#         request.user.email = request.POST.get('txt_email')
#         request.user.save()
#         profile.age = request.POST.get('txt_age')
#         profile.contact = request.POST.get('txt_contact')
#         profile.date_of_birth = request.POST.get('txt_date_of_birth')
#         profile.address = request.POST.get('txt_address')
#         profile.save()
#         return redirect('User:UserDashboard')
#     return render(request, 'User/MyProfile.html', {'profile': profile})

# def Profile(request): 
#     return render(request, 'User/Profile.html')

# def MyProfile(request):
#     if not request.user.is_authenticated:
#         return redirect('Guest:Login')
#     profile, created = tbl_UserProfile.objects.get_or_create(name=request.user)
#     if request.method == "POST":
#         request.user.first_name = request.POST.get('txt_name')
#         request.user.email = request.POST.get('txt_email')
#         request.user.save()
#         profile.save()
#         return redirect('User:UserDashboard')
#     return render(request, 'User/MyProfile.html', {'profile': profile})

# def EditProfile(request): 
#     return render(request, 'User/EditProfile.html')

# def ChangePassword(request): 
#     return render(request, 'User/ChangePassword.html')

from datetime import date, timedelta
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from Guest.models import tbl_registration
from Doctor.models import tbl_Doctor, tbl_Appointment, tbl_Prescription, tbl_Message
from Administrator.models import tbl_Milestone
from .models import tbl_UserProfile, tbl_PregnancyTracker, tbl_PregnancyWeeklyRecord, tbl_Baby
from .ml_model import predict_maternal_risk, nutrition_recommendations

def current_user(request):
    uid = request.session.get('user_id')
    if not uid or request.session.get('role') != 'USER':
        return None
    return tbl_registration.objects.filter(id=uid, is_active=True).first()

def guard(request):
    user = current_user(request)
    if not user:
        return None, redirect('Guest:Login')
    return user, None

def UserDashboard(request):
    user, response = guard(request)
    if response: return response
    pregnancy = user.pregnancy_records.first()
    baby = user.babies.first()
    risk = None
    if pregnancy:
        risk = predict_maternal_risk(
            age=(getattr(user.profile,'age',None) or 28) if hasattr(user,'profile') else 28,
            systolicbp=120, diastolicbp=80, blood_sugar=7,
            bodytemp=98.6, heartrate=78
        )
    return render(request,'User/UserDashboard.html',{
        'user':user,'pregnancy':pregnancy,'baby':baby,'risk':risk,
        'appointments':user.appointments.select_related('doctor').all()[:5]
    })

def PregnancyProfile(request):
    user, response = guard(request)
    if response: return response
    pregnancy = user.pregnancy_records.first()
    if request.method == 'POST':
        lmp = request.POST.get('last_period_date')
        if lmp:
            from datetime import datetime
            lmp_date=datetime.strptime(lmp,'%Y-%m-%d').date()
            edd=lmp_date+timedelta(days=280)
            pregnancy, _ = tbl_PregnancyTracker.objects.update_or_create(
                user=user, defaults={'last_period_date':lmp_date,'expected_delivery_date':edd}
            )
            messages.success(request,'Pregnancy profile saved.')
            return redirect('User:PregnancyTracker')
    return render(request,'User/PregnancyProfile.html',{'user':user,'pregnancy':pregnancy})

def PregnancyTracker(request):
    user, response = guard(request)
    if response: return response
    pregnancy=user.pregnancy_records.first()
    if request.method=='POST':
        lmp=request.POST.get('last_period_date')
        if lmp:
            from datetime import datetime
            lmp_date=datetime.strptime(lmp,'%Y-%m-%d').date()
            edd=lmp_date+timedelta(days=280)
        elif pregnancy:
            lmp_date=pregnancy.last_period_date; edd=pregnancy.expected_delivery_date
        else:
            messages.error(request,'Enter the last menstrual period date first.')
            return redirect('User:PregnancyProfile')
        week=max(1,min(40,(date.today()-lmp_date).days//7+1))
        pregnancy, _=tbl_PregnancyTracker.objects.update_or_create(
            user=user, defaults={
                'last_period_date':lmp_date,'expected_delivery_date':edd,
                'current_week':week,'weight':request.POST.get('weight') or None,
                'symptoms':request.POST.get('symptoms',''),'notes':request.POST.get('notes','')
            }
        )
        tbl_PregnancyWeeklyRecord.objects.create(
            pregnancy=pregnancy, week=week, weight=request.POST.get('weight') or None,
            symptoms=request.POST.get('symptoms',''), mood=request.POST.get('mood',''),
            notes=request.POST.get('notes','')
        )
        messages.success(request,'Weekly pregnancy record saved.')
        return redirect('User:PregnancyTracker')
    milestone = tbl_Milestone.objects.filter(week=pregnancy.current_week).first() if pregnancy else None
    return render(request,'User/PregnancyTracker.html',{
        'user':user,'pregnancy':pregnancy,'milestone':milestone,
        'weekly_records': pregnancy.weekly_records.all() if pregnancy else []
    })

def BabyGrowth(request):
    user,response=guard(request)
    if response:return response
    baby=user.babies.first()
    if request.method=='POST':
        baby=tbl_Baby.objects.create(
            user=user,baby_name=request.POST.get('baby_name',''),
            date_of_birth=request.POST.get('date_of_birth') or None,
            gender=request.POST.get('gender',''),birth_weight=request.POST.get('birth_weight') or None,
            current_weight=request.POST.get('current_weight') or None,
            height=request.POST.get('height') or None,notes=request.POST.get('notes','')
        )
        messages.success(request,'Baby record saved.')
        return redirect('User:BabyGrowth')
    return render(request,'User/BabyGrowth.html',{'user':user,'baby':baby,'babies':user.babies.all()})

def Nutrition(request):
    user,response=guard(request)
    if response:return response
    query=request.GET.get('q','')
    recs=nutrition_recommendations(query)
    return render(request,'User/Nutrition.html',{'user':user,'recommendations':recs,'query':query})

def Appointments(request):
    user,response=guard(request)
    if response:return response
    doctors=tbl_Doctor.objects.filter(available=True).select_related('user')
    if request.method=='POST':
        doctor=get_object_or_404(tbl_Doctor,id=request.POST.get('doctor'))
        tbl_Appointment.objects.create(
            patient=user,doctor=doctor,appointment_date=request.POST.get('appointment_date'),
            appointment_time=request.POST.get('appointment_time'),reason=request.POST.get('reason','')
        )
        messages.success(request,'Appointment requested.')
        return redirect('User:Appointments')
    return render(request,'User/Appointments.html',{'user':user,'doctors':doctors,'appointments':user.appointments.select_related('doctor').all()})

def Profile(request):
    user,response=guard(request)
    if response:return response
    profile, _=tbl_UserProfile.objects.get_or_create(user=user,defaults={'contact':user.user_contact,'address':user.user_address})
    return render(request,'User/Profile.html',{'user':user,'profile':profile})

def MyProfile(request):
    user,response=guard(request)
    if response:return response
    profile,_=tbl_UserProfile.objects.get_or_create(user=user)
    if request.method=='POST':
        user.user_name=request.POST.get('txt_name',user.user_name)
        user.user_email=request.POST.get('txt_email',user.user_email).lower()
        user.user_contact=request.POST.get('txt_contact',user.user_contact)
        user.user_address=request.POST.get('txt_address',user.user_address)
        user.save()
        profile.age=request.POST.get('txt_age') or None
        profile.date_of_birth=request.POST.get('txt_date_of_birth') or None
        profile.contact=user.user_contact
        profile.address=user.user_address
        if request.FILES.get('profile_photo'): profile.profile_photo=request.FILES['profile_photo']
        profile.save()
        request.session['user_name']=user.user_name
        messages.success(request,'Profile updated.')
        return redirect('User:MyProfile')
    return render(request,'User/MyProfile.html',{'user':user,'profile':profile})

def EditProfile(request):
    return MyProfile(request)

def ChangePassword(request):
    user,response=guard(request)
    if response:return response
    from django.contrib.auth.hashers import check_password,make_password
    if request.method=='POST':
        old=request.POST.get('old_password',''); new=request.POST.get('new_password','')
        if not check_password(old,user.user_password):
            messages.error(request,'Current password is incorrect.')
        elif len(new)<6:
            messages.error(request,'New password must be at least 6 characters.')
        else:
            user.user_password=make_password(new); user.save()
            messages.success(request,'Password changed successfully.')
            return redirect('User:Profile')
    return render(request,'User/ChangePassword.html')

def Messages(request):
    user,response=guard(request)
    if response:return response
    doctors=tbl_Doctor.objects.filter(available=True)
    if request.method=='POST':
        doctor=get_object_or_404(tbl_Doctor,id=request.POST.get('doctor'))
        tbl_Message.objects.create(sender=user,receiver=doctor.user,message=request.POST.get('message',''))
        messages.success(request,'Message sent.')
    msgs=tbl_Message.objects.filter(sender=user).select_related('receiver') | tbl_Message.objects.filter(receiver=user).select_related('sender')
    return render(request,'User/Messages.html',{'user':user,'doctors':doctors,'messages_list':msgs.order_by('-sent_at')})

def AIPrediction(request):
    user,response=guard(request)
    if response:return response
    result=None
    if request.method=='POST':
        result=predict_maternal_risk(
            request.POST.get('age',28),request.POST.get('systolicbp',120),
            request.POST.get('diastolicbp',80),request.POST.get('blood_sugar',7),
            request.POST.get('bodytemp',98.6),request.POST.get('heartrate',78)
        )
    return render(request,'User/AIPrediction.html',{'user':user,'result':result})
