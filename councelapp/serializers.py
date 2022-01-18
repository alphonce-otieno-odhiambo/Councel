from rest_framework import serializers
from .models import *

class CounselorProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CounselorProfile
        fields = ("id", "url","full_name","bio","profile_pic")