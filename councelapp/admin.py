from django.contrib import admin
from .models import Client, Group

# Register your models here.
admin.site.register(Client)
admin.site.register(Group)