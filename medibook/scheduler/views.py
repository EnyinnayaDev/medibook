from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import PatientRegisterForm, AppointmentForm
from .models import Service, Doctor, Appointment

def home(request):
    return render(request, 'scheduler/home.html')

def register(request):
    if request.method == 'POST':
        form = PatientRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = PatientRegisterForm()
    return render(request, 'scheduler/register.html', {'form': form})

def service_list(request):
    services = Service.objects.all()
    return render(request, 'scheduler/service_list.html', {'services': services})


def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'scheduler/doctor_list.html', {'doctors': doctors})

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            return redirect('my_appointments')
    else:
        form = AppointmentForm()
    return render(request, 'scheduler/book_appointment.html', {'form': form})