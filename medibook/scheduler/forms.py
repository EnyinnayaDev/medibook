from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Appointment


class PatientRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'service', 'date', 'time']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.localdate():
            raise forms.ValidationError("You can't book an appointment in the past.")
        return date

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if doctor and date and time:
            conflict = Appointment.objects.filter(
                doctor=doctor,
                date=date,
                time=time,
            ).exclude(status='cancelled')

            if conflict.exists():
                raise forms.ValidationError(
                    "This doctor is already booked at that date and time. Please choose another slot."
                )
        return cleaned_data