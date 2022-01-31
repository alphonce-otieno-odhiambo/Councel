
from django.db import models
from django.http import request

from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField



from django.utils import timezone
from django.urls import reverse





# Create your models here.


# Appointment Models
class Appointment(models.Model):
	TYPE = (
		('first', 'First appointment'),
		('follow-up', 'Follow-up appointment'),
		('final', 'Final appointment'),
	)
	description = models.CharField('Short Description', max_length=256, null=True, blank=True)
	client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
	counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE, null=True)
	time = models.DateField('Appointment Date')
	appointment_type = models.CharField('Appointment Type', max_length=20, choices=TYPE, null=True)
	requested = models.BooleanField(default=True)
	fixed = models.BooleanField('fix appointment?', default=False)
	held = models.BooleanField('appointment held?', default=False)
	remarks = models.TextField(null=True, blank=True)
	recommendations = models.TextField(null=True, blank=True)
	counsellee_archived = models.BooleanField(default=False)
	counsellor_archived = models.BooleanField(default=False)
	
	def __str__(self):
		return self.description

	class Meta:
		ordering = ['time',]


# Prescription Models
class Prescription(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    client=models.ForeignKey(Client,on_delete=models.CASCADE)
    counsellor=models.ForeignKey(Counsellor,on_delete=models.CASCADE)
    prescription=models.TextField()
    diagnosis=models.CharField(max_length=25)
    date=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.user.first_name}' 
