from rest_framework import serializers
from .models import Client, Group

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'age', 'tel_no', 'groups', 'profile_picture')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'counsellor', 'members')