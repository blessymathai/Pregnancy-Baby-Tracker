from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from Guest.models import tbl_registration
from User.models import tbl_PregnancyTracker, tbl_Baby

from .models import (
    tbl_Doctor,
    tbl_Appointment,
    tbl_Prescription,
    tbl_Message
)


# =========================================================
# DOCTOR LOGIN USER
# =========================================================

def doctor_user(request):

    uid = request.session.get('user_id')

    if not uid or request.session.get('role') != 'DOCTOR':
        return None

    return tbl_registration.objects.filter(
        id=uid,
        is_active=True,
        role='DOCTOR'
    ).first()


# =========================================================
# DOCTOR LOGIN GUARD
# =========================================================

def guard(request):

    user = doctor_user(request)

    if user:
        return user, None

    return None, redirect('Guest:Login')


# =========================================================
# DOCTOR DASHBOARD
# =========================================================

def DoctorDashboard(request):

    user, response = guard(request)

    if response:
        return response

    doctor = get_object_or_404(
        tbl_Doctor,
        user=user
    )

    # Store doctor name in session
    request.session['doctor_name'] = doctor.name

    # Current date
    today = timezone.localdate()

    # Doctor appointments
    appointments = doctor.appointments.select_related(
        'patient'
    )

    # -----------------------------------------------------
    # TODAY'S APPOINTMENTS
    # IMPORTANT:
    # Model field = appointment_date
    # -----------------------------------------------------

    today_appointments = appointments.filter(
        appointment_date=today
    ).count()

    # -----------------------------------------------------
    # RECENT 5 APPOINTMENTS
    # IMPORTANT:
    # Model fields = appointment_date, appointment_time
    # -----------------------------------------------------

    recent_appointments = appointments.order_by(
        '-appointment_date',
        '-appointment_time'
    )[:5]

    # -----------------------------------------------------
    # DASHBOARD DATA
    # -----------------------------------------------------

    context = {

        'doctor': doctor,

        # Total registered active users
        'total_patients': tbl_registration.objects.filter(
            role='USER',
            is_active=True
        ).count(),

        # Today's appointments
        'today_appointments': today_appointments,

        # Pregnancy records
        'pregnancy_records': tbl_PregnancyTracker.objects.count(),

        # Baby records
        'baby_records': tbl_Baby.objects.count(),

        # Recent appointments
        'recent_appointments': recent_appointments,
    }

    return render(
        request,
        'Doctor/DoctorDashboard.html',
        context
    )


# =========================================================
# PATIENTS
# =========================================================

def Patients(request):

    user, response = guard(request)

    if response:
        return response

    doctor = get_object_or_404(
        tbl_Doctor,
        user=user
    )

    patients = tbl_registration.objects.filter(
        role='USER',
        is_active=True
    )

    return render(
        request,
        'Doctor/Patients.html',
        {
            'doctor': doctor,
            'patients': patients
        }
    )


# =========================================================
# APPOINTMENTS
# =========================================================

def Appointments(request):

    user, response = guard(request)

    if response:
        return response

    doctor = get_object_or_404(
        tbl_Doctor,
        user=user
    )

    # -----------------------------------------------------
    # UPDATE APPOINTMENT
    # -----------------------------------------------------

    if request.method == 'POST':

        appointment_id = request.POST.get(
            'appointment'
        )

        appointment = get_object_or_404(
            tbl_Appointment,
            id=appointment_id,
            doctor=doctor
        )

        appointment.status = request.POST.get(
            'status',
            appointment.status
        )

        appointment.notes = request.POST.get(
            'notes',
            appointment.notes
        )

        appointment.save()

        messages.success(
            request,
            'Appointment updated successfully.'
        )

        return redirect(
            'Doctor:Appointments'
        )

    # -----------------------------------------------------
    # GET APPOINTMENTS
    # -----------------------------------------------------

    appointments = doctor.appointments.select_related(
        'patient'
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )

    return render(
        request,
        'Doctor/Appointments.html',
        {
            'doctor': doctor,
            'appointments': appointments
        }
    )


# =========================================================
# PREGNANCY RECORDS
# =========================================================

def PregnancyRecords(request):

    user, response = guard(request)

    if response:
        return response

    doctor = get_object_or_404(
        tbl_Doctor,
        user=user
    )

    records = tbl_PregnancyTracker.objects.select_related(
        'user'
    ).all()

    return render(
        request,
        'Doctor/PregnancyRecords.html',
        {
            'doctor': doctor,
            'records': records
        }
    )


# =========================================================
# BABY RECORDS
# =========================================================

def BabyRecords(request):

    user, response = guard(request)

    if response:
        return response

    doctor = get_object_or_404(
        tbl_Doctor,
        user=user
    )

    records = tbl_Baby.objects.select_related(
        'user'
    ).all()

    return render(
        request,
        'Doctor/BabyRecords.html',
        {
            'doctor': doctor,
            'records': records
        }
    )


# =========================================================
# PRESCRIPTIONS
# =========================================================

def Prescriptions(request):

    user, response = guard(request)

    if response:
        return response

    doctor = get_object_or_404(
        tbl_Doctor,
        user=user
    )

    patients = tbl_registration.objects.filter(
        role='USER',
        is_active=True
    )

    # -----------------------------------------------------
    # CREATE PRESCRIPTION
    # -----------------------------------------------------

    if request.method == 'POST':

        patient_id = request.POST.get(
            'patient'
        )

        medicine = request.POST.get(
            'medicine',
            ''
        )

        dosage = request.POST.get(
            'dosage',
            ''
        )

        duration = request.POST.get(
            'duration',
            ''
        )

        instructions = request.POST.get(
            'instructions',
            ''
        )

        patient = get_object_or_404(
            tbl_registration,
            id=patient_id,
            role='USER'
        )

        tbl_Prescription.objects.create(

            patient=patient,

            doctor=doctor,

            medicine=medicine,

            dosage=dosage,

            duration=duration,

            instructions=instructions
        )

        messages.success(
            request,
            'Prescription saved successfully.'
        )

        return redirect(
            'Doctor:Prescriptions'
        )

    # -----------------------------------------------------
    # GET PRESCRIPTIONS
    # -----------------------------------------------------

    prescriptions = doctor.prescriptions.select_related(
        'patient'
    )

    return render(
        request,
        'Doctor/Prescriptions.html',
        {
            'doctor': doctor,
            'patients': patients,
            'prescriptions': prescriptions
        }
    )


# =========================================================
# MESSAGES
# =========================================================

def Messages(request):

    user, response = guard(request)

    if response:
        return response

    doctor = get_object_or_404(
        tbl_Doctor,
        user=user
    )

    patients = tbl_registration.objects.filter(
        role='USER',
        is_active=True
    )

    # -----------------------------------------------------
    # SEND MESSAGE
    # -----------------------------------------------------

    if request.method == 'POST':

        patient_id = request.POST.get(
            'patient'
        )

        text = request.POST.get(
            'message',
            ''
        ).strip()

        patient = get_object_or_404(
            tbl_registration,
            id=patient_id,
            role='USER'
        )

        if text:

            tbl_Message.objects.create(

                sender=user,

                receiver=patient,

                message=text
            )

            messages.success(
                request,
                'Message sent successfully.'
            )

        return redirect(
            'Doctor:Messages'
        )

    # -----------------------------------------------------
    # MESSAGE LIST
    # -----------------------------------------------------

    sent_messages = tbl_Message.objects.filter(
        sender=user
    )

    received_messages = tbl_Message.objects.filter(
        receiver=user
    )

    message_list = (
        sent_messages | received_messages
    ).order_by('-sent_at')

    return render(
        request,
        'Doctor/Messages.html',
        {
            'doctor': doctor,
            'patients': patients,
            'messages_list': message_list
        }
    )


# =========================================================
# DOCTOR AI CHAT BOX
# =========================================================

def ChatBox(request):

    user, response = guard(request)

    if response:
        return response

    doctor = get_object_or_404(
        tbl_Doctor,
        user=user
    )

    if request.method == 'POST':

        question = request.POST.get(
            'message',
            ''
        ).strip().lower()

        # -------------------------------------------------
        # RISK
        # -------------------------------------------------

        if 'risk' in question:

            answer = (
                'Please review the patient pregnancy data '
                'and use the AI risk prediction module '
                'for the risk assessment.'
            )

        # -------------------------------------------------
        # NUTRITION
        # -------------------------------------------------

        elif 'nutrition' in question:

            answer = (
                'Nutrition recommendations can be '
                'generated using the nutrition dataset '
                'connected to the AI module.'
            )

        # -------------------------------------------------
        # APPOINTMENT
        # -------------------------------------------------

        elif 'appointment' in question:

            answer = (
                'You can view and manage patient '
                'appointments from the Appointments section.'
            )

        # -------------------------------------------------
        # PREGNANCY
        # -------------------------------------------------

        elif 'pregnancy' in question:

            answer = (
                'Pregnancy records and weekly tracking '
                'information are available in Pregnancy Records.'
            )

        # -------------------------------------------------
        # BABY
        # -------------------------------------------------

        elif 'baby' in question:

            answer = (
                'Baby growth and baby records can be '
                'viewed from the Baby Records section.'
            )

        # -------------------------------------------------
        # DEFAULT
        # -------------------------------------------------

        else:

            answer = (
                'Doctor AI Assistant: I can help with '
                'pregnancy tracking, appointments, '
                'nutrition, baby growth and general '
                'project information.'
            )

        # -------------------------------------------------
        # AJAX RESPONSE
        # -------------------------------------------------

        if request.headers.get(
            'x-requested-with'
        ) == 'XMLHttpRequest':

            return JsonResponse({
                'answer': answer
            })

    return render(
        request,
        'Doctor/ChatBox.html',
        {
            'doctor': doctor
        }
    )


# =========================================================
# DOCTOR LOGOUT
# =========================================================

def Logout(request):

    request.session.flush()

    return redirect(
        'Guest:HomePage'
    )


# =========================================================
# DOCTOR REGISTRATION
# =========================================================

def DoctorRegistrationView(request):

    if request.method == 'POST':

        # -------------------------------------------------
        # BASIC DETAILS
        # -------------------------------------------------

        name = request.POST.get(
            'txt_name',
            ''
        ).strip()

        email = request.POST.get(
            'txt_email',
            ''
        ).strip().lower()

        contact = request.POST.get(
            'txt_contact',
            ''
        ).strip()

        address = request.POST.get(
            'txt_address',
            ''
        ).strip()

        password = request.POST.get(
            'txt_password',
            ''
        )

        # -------------------------------------------------
        # DOCTOR DETAILS
        # -------------------------------------------------

        specialization = request.POST.get(
            'txt_specialization',
            'General Medicine'
        ).strip()

        qualification = request.POST.get(
            'txt_qualification',
            ''
        ).strip()

        license_no = request.POST.get(
            'txt_license_no',
            ''
        ).strip()

        hospital = request.POST.get(
            'txt_hospital',
            ''
        ).strip()

        # -------------------------------------------------
        # EXPERIENCE
        # -------------------------------------------------

        try:

            experience = int(
                request.POST.get(
                    'txt_experience',
                    0
                ) or 0
            )

        except (ValueError, TypeError):

            experience = 0

        experience = max(
            0,
            experience
        )

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not name:

            return render(
                request,
                'Doctor/DoctorRegistration.html',
                {
                    'error': 'Name is required.'
                }
            )

        if not email:

            return render(
                request,
                'Doctor/DoctorRegistration.html',
                {
                    'error': 'Email is required.'
                }
            )

        if not contact:

            return render(
                request,
                'Doctor/DoctorRegistration.html',
                {
                    'error': 'Contact is required.'
                }
            )

        if not password:

            return render(
                request,
                'Doctor/DoctorRegistration.html',
                {
                    'error': 'Password is required.'
                }
            )

        # -------------------------------------------------
        # CHECK EMAIL
        # -------------------------------------------------

        if tbl_registration.objects.filter(
            user_email=email
        ).exists():

            return render(
                request,
                'Doctor/DoctorRegistration.html',
                {
                    'error': 'Email already registered.'
                }
            )

        # -------------------------------------------------
        # CREATE REGISTRATION
        # -------------------------------------------------

        registration = tbl_registration.objects.create(

            user_name=name,

            user_email=email,

            user_contact=contact,

            user_address=address,

            user_password=make_password(
                password
            ),

            role='DOCTOR',

            is_active=True
        )

        # -------------------------------------------------
        # CREATE DOCTOR PROFILE
        # -------------------------------------------------

        tbl_Doctor.objects.create(

            user=registration,

            name=name,

            specialization=specialization,

            qualification=qualification,

            license_no=license_no,

            experience=experience,

            hospital=hospital,

            contact=contact,

            available=True
        )

        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        messages.success(
            request,
            'Doctor registration successful! Please login.'
        )

        return redirect(
            'Guest:DoctorLogin'
        )

    # -----------------------------------------------------
    # GET REGISTRATION PAGE
    # -----------------------------------------------------

    return render(
        request,
        'Doctor/DoctorRegistration.html'
    )