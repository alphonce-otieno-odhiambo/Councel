from rest_framework import serializers
from .models import ClientProfile, Group
from .models import *

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ('id', 'first_name', 'last_name', 'age', 'tel_no', 'groups', 'profile_picture')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'counsellor', 'members')


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
