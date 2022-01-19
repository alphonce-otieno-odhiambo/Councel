from django.contrib import admin
from .models import Client, Group, Counsellor

# Register your models here.
admin.site.register(Client)
admin.site.register(Group)
admin.site.register(Counsellor)