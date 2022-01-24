from django.db import models
from counsel_users.models import Account
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from cloudinary import CloudinaryField
from django.utils import timezone
from django.http import request
# Create your models here.

class Counselor(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    experience = models.CharField(max_length=200)
    qualities = models.TextField(max_length=200)

class CounselorProfile(models.Model):
    counselor = models.OneToOneField(Counselor, on_delete=models.CASCADE, related_name='counselor')
    
    bio = models.CharField(max_length=300)
    
    profile_pic =CloudinaryField('image')


    def _str_(self):
        return f'{self.user.username} profile'
    @receiver(post_save, sender=Account)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
             CounselorProfile.objects.create(user=instance)
    @receiver(post_save, sender=Account)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
from django.http import request

# Create your models here.



class Appointment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    request = models.TextField(blank=True)
    sent_date = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.first_name
    
    class Meta:
        ordering = ["-sent_date"]

# Prescription Models
class Prescription(models.Model):
    prid=models.AutoField(primary_key=True)
    clients = models.ForeignKey('ClientProfile', on_delete=models.CASCADE,null=True, related_name='clients')
    counselor = models.OneToOneField('Counselor', on_delete=models.CASCADE, related_name='counselor')
    prescription=models.TextField()
    diagnosis=models.CharField(max_length=25)
    date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'{self.prid}'
