from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import PatientRegisterForm, AppointmentForm
from .models import Service, Doctor, Appointment
from django.utils import timezone

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

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'scheduler/my_appointments.html', {'appointments': appointments})


@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)

    if appointment.status == 'cancelled':
        messages.info(request, "This appointment is already cancelled.")
    elif appointment.date < timezone.localdate():
        messages.error(request, "You can't cancel a past appointment.")
    else:
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, "Appointment cancelled successfully.")

    return redirect('my_appointments')