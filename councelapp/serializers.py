from rest_framework import serializers
from .models import ClientProfile, Group

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ('id', 'first_name', 'last_name', 'age', 'tel_no', 'groups', 'profile_picture')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'counsellor', 'members')