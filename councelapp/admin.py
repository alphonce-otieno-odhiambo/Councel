from django.contrib import admin
from .models import ClientProfile, Group, Counselor

# Register your models here.
admin.site.register(ClientProfile)
admin.site.register(Group)
admin.site.register(Counselor)