from django.contrib import admin
from .models import * 

# Register your models here.
admin.site.register(CounselorProfile)
admin.site.register(Prescription)
admin.site.register(Appointment)
