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
    profile_picture = CloudinaryField(blank=True)

    def save(self):
        self.save()

    def __str__(self):
        return self.first_name


class Group(models.Model):
    counsellor = models.ForeignKey('Counselor', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    members = models.IntegerField()

    def save(self):
        self.save()

    def __str__(self):
        return self.name


class Counselor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    description = models.TextField()
    tel_no = models.IntegerField()
    clients = models.ForeignKey('Client', on_delete=models.CASCADE,null=True, related_name='clients')

    def save(self):
        self.save()

    def __str__(self):
        return self.first_name