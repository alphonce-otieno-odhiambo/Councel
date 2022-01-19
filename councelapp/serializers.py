from rest_framework import serializers
from .models import Client 

class ClientSerializer(serializers.ModelSerializer):
    