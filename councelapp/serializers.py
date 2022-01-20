from rest_framework import serializers
from .models import *

class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Appointment
        fields = ("id", "url","first_name", "last_name","email","phone","request","sent_date", "accepted","accepted_date")