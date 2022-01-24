from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from counsel_users.models import Account
from cloudinary.models import CloudinaryField

# Create your models here.
class ClientProfile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    tel_no = models.IntegerField()
    groups = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, related_name='groups', blank=True)
    profile_picture = CloudinaryField(blank=True)

    def save(self):
        self.save()

    def __str__(self):
        return self.first_name


class Group(models.Model):
    counselor = models.ForeignKey('Counselor', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def save(self):
        self.save()

    def __str__(self):
        return self.name


class Counselor(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    experience = models.CharField(max_length=200)
    qualities = models.TextField(max_length=200)
    tel_no = models.IntegerField()
    clients = models.ForeignKey('ClientProfile', on_delete=models.CASCADE,null=True, related_name='clients')

    def save(self):
        self.save()

    def __str__(self):
        return self.first_name