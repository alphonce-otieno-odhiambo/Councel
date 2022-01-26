from django.contrib import admin
from .models import Appointment
# Register your models here.

class AppointmentAdmin(admin.ModelAdmin):
	list_display = ['description', 'counsellor', 'counsellee', 'time']
	list_filter = ['time', 'counsellor', 'counsellee']


admin.site.register(Appointment, AppointmentAdmin)


# from accounts.models import Patient,Doctor

# admin.site.register(Patient)
# admin.site.register(Doctor)
