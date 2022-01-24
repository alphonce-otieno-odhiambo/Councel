# from importlib.abc import PathEntryFinder
from django.db import models
from django.http import request
from django.utils import timezone
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# from accounts.models import Patient,Doctor


# Create your models here.


# Appointment Models
class Appointment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    request = models.TextField(blank=True)
    doctor = models.CharField(max_length=200,default=0)
    description = models.TextField(max_length=10000,default=0)
    sent_date = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.first_name
    
    class Meta:
        ordering = ["-sent_date"]




# Patient Models
class Patient(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    pid=models.AutoField(primary_key=True)
    phone=models.CharField(max_length=10)
    age=models.CharField(max_length=3)
    gender=models.CharField(max_length=10)
    address=models.CharField(max_length=100)
    bloodgroup=models.CharField(max_length=10)
    casepaper=models.CharField(max_length=10)
    otp=models.CharField(max_length=6)
    verify=models.CharField(max_length=1,default=0)
    image=models.ImageField(default='default.jpg',upload_to='med_report')
    
    def __str__(self):
        return f'{self.user.first_name}'
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        image=CloudinaryField('image',null=True)

# Doctor Models            
class Doctor(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    did=models.AutoField(primary_key=True)
    phone=models.CharField(max_length=10)
    age=models.CharField(max_length=3)
    gender=models.CharField(max_length=10)
    Department=models.CharField(max_length=20)
    attendance=models.CharField(max_length=10)
    status=models.CharField(max_length=15)
    salary=models.CharField(max_length=10)
    otp=models.CharField(max_length=6)
    verify=models.CharField(max_length=1,default=0)
    
    def __str__(self):
        return f'{self.user.first_name}'


# Prescription Models
class Prescription(models.Model):
    prid=models.AutoField(primary_key=True)
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    prescription=models.TextField()
    disease=models.CharField(max_length=25)
    date=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.prid}'