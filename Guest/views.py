from django.shortcuts import render, redirect
from django.contrib import messages
from .models import tbl_registration

def HomePage(request):
    return render(request, 'Guest/HomePage.html')

# def Login(request):
#     if request.method == "POST":
#         email = request.POST.get('user_email')
#         password = request.POST.get('user_password')
#         try:
#             user = tbl_registration.objects.get(
#                 user_email=email,
#                 user_password=password
#             )
#             request.session['user_id'] = user.id
#             request.session['user_name'] = user.user_name
#             request.session['user_email'] = user.user_email
#             return redirect('User:UserDashboard')
#         except tbl_registration.DoesNotExist:
#             return render(
#                 request,
#                 'Guest/login.html',
#                 {
#                     'error': 'Invalid email or password'
#                 }
#             )
#     return render(request, 'Guest/login.html')

def Login(request):
    if request.method == "POST":
        email = request.POST.get("txt_email", "").strip()
        password = request.POST.get("txt_password", "")
        try:
            user = tbl_registration.objects.get(
                user_email=email,
                user_password=password
            )
            request.session["user_id"] = user.id
            request.session["user_name"] = user.user_name
            request.session["user_email"] = user.user_email
            return redirect("User:UserDashboard")
        except tbl_registration.DoesNotExist:
            messages.error(request, "Invalid email or password.")
    return render(request, "Guest/Login.html")

def UserRegistrationView(request):
    if request.method == "POST":
        name = request.POST.get("txt_name", "").strip()
        email = request.POST.get("txt_email", "").strip()
        contact = request.POST.get("txt_contact", "").strip()
        address = request.POST.get("txt_Address", "").strip()
        password = request.POST.get("txt_password", "")

        if not name:
            return render(
                request,
                "Guest/UserRegistration.html",
                {"error": "Name is required."}
            )

        if not email:
            return render(
                request,
                "Guest/UserRegistration.html",
                {"error": "Email is required."}
            )

        if not contact:
            return render(
                request,
                "Guest/UserRegistration.html",
                {"error": "Contact is required."}
            )

        if not password:
            return render(
                request,
                "Guest/UserRegistration.html",
                {"error": "Password is required."}
            )

        if tbl_registration.objects.filter(user_email=email).exists():
            return render(
                request,
                "Guest/UserRegistration.html",
                {"error": "Email already registered."}
            )

        tbl_registration.objects.create(
            user_name=name,
            user_email=email,
            user_contact=contact,
            user_address=address,
            user_password=password
        )

        messages.success(
            request,
            "Registration successful! Please login."
        )
        return redirect("Guest:Login")
    return render(request, "Guest/UserRegistration.html")

def Logout(request):
    logout(request)
    return redirect('Login')
