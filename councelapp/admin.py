from django.contrib import admin
from .models import Appointment, Prescription
# Register your models here.

admin.site.register(Appointment)

admin.site.register(Prescription)

# from accounts.models import Patient,Doctor

# admin.site.register(Patient)
# admin.site.register(Doctor)
