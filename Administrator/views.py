from django.shortcuts import render

# Create your views here.

def AdminDashboard(request):
    return render(request, 'Administrator/AdminDashboard.html')

def ManageUser(request):
    return render(request, 'Administrator/ManageUser.html')

def ManageDoctor(request):
    return render(request, 'Administrator/ManageDoctor.html')

def ManageMilestones(request):
    return render(request, 'Administrator/ManageMilestones.html')

def ManageNutrition(request):
    return render(request, 'Administrator/ManageNutrition.html')

def ManageMedicines(request):
    return render(request, 'Administrator/ManageMedicines.html')

def Reports(request):
    return render(request, 'Administrator/Reports.html')

def UploadDataset(request):
    return render(request,'Administrator/UploadDataset.html')

def ChatBox(request):
    return render(request,'Administrator/ChatBox.html')