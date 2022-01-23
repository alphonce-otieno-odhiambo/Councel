from rest_framework import serializers
from .models import *

class CounselorProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CounselorProfile
        fields = ("id", "url","counselor", "bio","profile_pic")

class CounselorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model =Counselor
        fields = ("id", "url", "user","first_name","last_name", "experience","qualities")
class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Appointment
        fields = ("id", "url","first_name", "last_name","email","phone","request","sent_date", "accepted","accepted_date")
