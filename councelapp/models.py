from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    tel_no = models.IntegerField()
    groups = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, related_name='groups', blank=True)