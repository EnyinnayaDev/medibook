# MediBook — Clinic Appointment Scheduler

A Django web app for booking, viewing, and cancelling clinic appointments.
Built for SEN 310.

## Problem
Clinics often deal with double-booking, walk-in chaos, and missed follow-ups.
MediBook lets patients book appointments with doctors online, with built-in
conflict checking so no doctor is ever double-booked.

## Features
- Patient registration, login, logout (Django auth)
- Browse doctors and services
- Book an appointment with automatic conflict detection
- View and cancel your own appointments
- Appointment lifecycle: Pending → Confirmed/Completed/Cancelled
  (staff manage status via Django admin)

## Tech stack
- Python / Django (function-based views)
- SQLite (default Django DB)
- Bootstrap 5 (CDN, no build step)

## Models
- Doctor — name, specialization, bio
- Service — name, duration, price
- Appointment — patient (User), doctor, service, date, time, status
(Patients use Django's built-in User model.)

## Setup
1. Clone the repo
2. `python -m venv venv` then activate it
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py createsuperuser` (for admin access)
6. `python manage.py runserver`
7. Visit `/admin/` to add doctors and services before testing booking

## Known limitations / future work
- Doctors don't have their own login (managed via admin)
- No email notifications
- No automatic status transitions (staff manually mark Completed)
- No doctor weekly availability schedules (any date/time is bookable)