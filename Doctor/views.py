# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from django.contrib import messages
# from .models import *

# # Create your views here.
# # =========================================================
# # DOCTOR DASHBOARD
# # =========================================================

# def DoctorDashboard(request):

#     # Login ചെയ്ത doctor session
#     doctor_id = request.session.get('doctor_id')

#     if not doctor_id:
#         return redirect('Login')

#     # Doctor information
#     try:
#         doctor = tbl_Doctor.objects.get(id=doctor_id)
#         doctor_name = doctor.name
#     except:
#         doctor = None
#         doctor_name = "Doctor"

#     # Counts
#     try:
#         total_patients = tbl_registration.objects.count()
#     except:
#         total_patients = 0

#     try:
#         total_appointments = tbl_Appointment.objects.count()
#     except:
#         total_appointments = 0

#     try:
#         total_pregnancy_records = tbl_PregnancyTracker.objects.count()
#     except:
#         total_pregnancy_records = 0

#     try:
#         total_baby_records = tbl_BabyProfile.objects.count()
#     except:
#         total_baby_records = 0

#     context = {
#         'doctor': doctor,
#         'doctor_name': doctor_name,
#         'total_patients': total_patients,
#         'total_appointments': total_appointments,
#         'total_pregnancy_records': total_pregnancy_records,
#         'total_baby_records': total_baby_records,
#     }

#     return render(
#         request,
#         'doctor/Dashboard.html',
#         context
#     )


# # =========================================================
# # PATIENTS
# # =========================================================

# def DoctorPatients(request):

#     doctor_id = request.session.get('doctor_id')

#     if not doctor_id:
#         return redirect('Login')

#     try:
#         patients = tbl_registration.objects.all().order_by('-id')
#     except:
#         patients = []

#     context = {
#         'Patients': patients
#     }

#     return render(
#         request,
#         'doctor/Patients.html',
#         context
#     )


# # =========================================================
# # APPOINTMENTS
# # =========================================================

# def DoctorAppointments(request):

#     doctor_id = request.session.get('doctor_id')

#     if not doctor_id:
#         return redirect('Login')

#     try:
#         appointments = tbl_Appointment.objects.all().order_by('-id')
#     except:
#         appointments = []

#     context = {
#         'Appointments': appointments
#     }

#     return render(
#         request,
#         'doctor/Appointments.html',
#         context
#     )


# # =========================================================
# # PREGNANCY RECORDS
# # =========================================================

# def PregnancyRecords(request):

#     doctor_id = request.session.get('doctor_id')

#     if not doctor_id:
#         return redirect('Login')

#     try:
#         pregnancy_records = (
#             tbl_PregnancyTracker.objects
#             .select_related('user')
#             .all()
#             .order_by('-id')
#         )
#     except:
#         pregnancy_records = []

#     context = {
#         'PregnancyRecords': pregnancy_records
#     }

#     return render(
#         request,
#         'doctor/PregnancyRecords.html',
#         context
#     )


# # =========================================================
# # BABY RECORDS
# # =========================================================

# def BabyRecords(request):

#     doctor_id = request.session.get('doctor_id')

#     if not doctor_id:
#         return redirect('Login')

#     try:
#         baby_records = (
#             tbl_BabyProfile.objects
#             .all()
#             .order_by('-id')
#         )
#     except:
#         baby_records = []

#     context = {
#         'BabyRecords': baby_records
#     }

#     return render(
#         request,
#         'doctor/BabyRecords.html',
#         context
#     )


# # =========================================================
# # PRESCRIPTIONS
# # =========================================================

# def Prescriptions(request):

#     doctor_id = request.session.get('doctor_id')

#     if not doctor_id:
#         return redirect('Login')

#     try:
#         patients = tbl_registration.objects.all()
#     except:
#         patients = []

#     if request.method == 'POST':

#         patient_id = request.POST.get('patient')
#         medicine = request.POST.get('medicine')
#         dosage = request.POST.get('dosage')
#         duration = request.POST.get('duration')
#         instructions = request.POST.get('instructions')

#         try:

#             patient = tbl_registration.objects.get(
#                 id=patient_id
#             )

#             tbl_Prescription.objects.create(
#                 patient=patient,
#                 medicine=medicine,
#                 dosage=dosage,
#                 duration=duration,
#                 instructions=instructions
#             )

#             messages.success(
#                 request,
#                 'Prescription saved successfully.'
#             )

#             return redirect('Prescriptions')

#         except Exception as e:

#             messages.error(
#                 request,
#                 f'Error: {e}'
#             )

#     try:
#         prescriptions = (
#             tbl_Prescription.objects
#             .all()
#             .order_by('-id')
#         )
#     except:
#         prescriptions = []

#     context = {
#         'Patients': patients,
#         'Prescriptions': prescriptions
#     }

#     return render(
#         request,
#         'doctor/Prescriptions.html',
#         context
#     )
# # =========================================================
# # MESSAGES
# # =========================================================
# def DoctorMessages(request):
#     doctor_id = request.session.get('doctor_id')
#     if not doctor_id:
#         return redirect('Login')
#     try:
#         patients = tbl_registration.objects.all()
#     except:
#         patients = []
#     if request.method == 'POST':
#         patient_id = request.POST.get('patient')
#         message_text = request.POST.get('message')
#         try:
#             patient = tbl_registration.objects.get(
#                 id=patient_id
#             )
#             tbl_Message.objects.create(
#                 patient=patient,
#                 doctor_id=doctor_id,
#                 message=message_text
#             )
#             messages.success(
#                 request,
#                 'Message sent successfully.'
#             )
#             return redirect('DoctorMessages')
#         except Exception as e:
#             messages.error(
#                 request,
#                 f'Error: {e}'
#             )
#     try:
#         message_list = (
#             tbl_Message.objects
#             .all()
#             .order_by('-id')
#         )
#     except:
#         message_list = []
#     context = {
#         'Patients': patients,
#         'Messages': message_list
#     }
#     return render(request,'doctor/Messages.html',context)
# # =========================================================
# # AI CHATBOX
# # =========================================================
# def DoctorAIChatbox(request):
#     doctor_id = request.session.get('doctor_id')
#     if not doctor_id:
#         return redirect('Login')
#     if request.method == 'POST':
#         user_message = request.POST.get(
#             'message',
#             ''
#         ).strip()
#         if not user_message:
#             return JsonResponse({
#                 'response': 'Please enter a message.'
#             })
#         # Basic AI response
#         message_lower = user_message.lower()
#         if 'pregnancy' in message_lower:
#             response = (
#                 "Pregnancy care depends on the mother's "
#                 "gestational age, symptoms and medical history. "
#                 "Please review the patient's clinical records "
#                 "before making a medical decision."
#             )
#         elif 'baby' in message_lower:
#             response = (
#                 "Baby growth should be monitored using "
#                 "age-appropriate weight, height and developmental "
#                 "milestones."
#             )
#         elif 'nutrition' in message_lower:
#             response = (
#                 "A balanced diet containing adequate protein, "
#                 "iron, folate, calcium and other essential nutrients "
#                 "is important during pregnancy."
#             )
#         elif 'risk' in message_lower:
#             response = (
#                 "Maternal risk assessment should consider "
#                 "clinical parameters and the prediction model "
#                 "results together."
#             )
#         else:
#             response = (
#                 "I can help you with pregnancy tracking, "
#                 "baby growth, nutrition, appointments and "
#                 "patient records."
#             )
#         return JsonResponse({'response': response})
#     return render( request,'doctor/AIChatbox.html')


from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import *


def DoctorDashboard(request):
    return render(request, 'doctor/dashboard.html')


def Patients(request):
    return render(request, 'doctor/patients.html')


def Appointments(request):
    return render(request, 'doctor/appointments.html')


def PregnancyRecords(request):
    return render(request, 'doctor/pregnancy_records.html')


def BabyRecords(request):
    return render(request, 'doctor/baby_records.html')


def Prescriptions(request):
    return render(request, 'doctor/prescriptions.html')


def Messages(request):
    return render(request, 'doctor/messages.html')


def ChatBox(request):
    return render(request, 'doctor/ai_chatbox.html')
