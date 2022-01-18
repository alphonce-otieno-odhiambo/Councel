from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CounselorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=50)
    bio = models.CharField(max_length=300)
    profile_pic = ClaudinaryField('image')