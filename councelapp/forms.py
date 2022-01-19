from django.db.models import fields
from django import forms
from .models import *

class CounselorProfile(forms.ModelForm):
    class Meta:
        model = CounselorProfile
        fields = ("full_name","bio", "profile_pic")