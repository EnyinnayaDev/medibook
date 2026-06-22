from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import PatientRegisterForm


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

def home(request):
    return render(request, 'scheduler/home.html')