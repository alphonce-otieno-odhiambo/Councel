from django.db import models
from counsel_users.models import Account
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from cloudinary.models import CloudinaryField
from django.utils import timezone
from django.db.models.deletion import CASCADE, SET_NULL


from counsel_users.serializers import UserSerializers
# Create your models here.

class Details(models.Model):
    owner = models.OneToOneField(Account,on_delete=models.CASCADE,)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    quantiles = models.TextField(null=True)
    experiences = models.TextField(null=True)

class Counsellor(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='profile')
    details = models.ForeignKey(Details,on_delete=models.CASCADE,null=True,related_name='user')

    def __str__(self):
        return self.user.username + "'s " + "profile"

    @receiver(post_save, sender=Account)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
         Counsellor.objects.create(user=instance)

    @receiver(post_save, sender=Account)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class CounselorProfile(models.Model):
    counselor = models.OneToOneField(Counsellor, on_delete=models.CASCADE, related_name='counselor')
    
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


# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(Account,null=False,on_delete=CASCADE,related_name="client_profile")
    counsellor = models.ForeignKey(Counsellor,null=True,blank=True,on_delete=models.SET_NULL,related_name="counsellor")

    def __str__(self):
        return self.user.username + "'s " + "profile"

    @receiver(post_save, sender=Account)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Client.objects.create(user=instance)

    @receiver(post_save, sender=Account)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()



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
class Group(models.Model):
    counselor = models.ForeignKey('Counselor', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def save(self):
        self.save()

    def _str_(self):
        return self.name

class ClientProfile(models.Model):
    user = models.OneToOneField(Account,null=False,on_delete=CASCADE,related_name="client_profile")
    counsellor = models.ForeignKey('Counselor',null=True,blank=True,on_delete=models.SET_NULL,related_name="counsellor")

    def _str_(self):
        return self.user.username + "'s " + "profile"

    @receiver(post_save, sender=Account)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ClientProfile.objects.create(user=instance)

    @receiver(post_save, sender=Account)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


# Prescription Models
class Prescription(models.Model):
    prid=models.AutoField(primary_key=True)
    clients = models.ForeignKey('ClientProfile', on_delete=models.CASCADE,null=True, related_name='clients')
    counsel = models.OneToOneField('Counselor', on_delete=models.CASCADE, related_name='counsel')
    prescription=models.TextField()
    diagnosis=models.CharField(max_length=25)
    date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'{self.prid}'
