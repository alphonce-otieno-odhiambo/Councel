from django.db import models
from counsel_users.models import Account
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from cloudinary.models import CloudinaryField
from django.utils import timezone
from django.db.models.deletion import CASCADE, SET_NULL
from django.http import request


from counsel_users.serializers import UserSerializers
# Create your models here.

class Counsellor(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    experience = models.CharField(max_length=200)
    qualities = models.TextField(max_length=200)
    tel_no = models.IntegerField()
    clients = models.ForeignKey('ClientProfile', on_delete=models.CASCADE,null=True, related_name='clients')

    def save(self):
        self.save()

    def _str_(self):
        return self.first_name


class CounselorProfile(models.Model):
    counselor = models.OneToOneField(Counsellor, on_delete=models.CASCADE, related_name='counselor')
    
    bio = models.CharField(max_length=300)
    
    profile_pic =CloudinaryField('image')


    def str(self):
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
        ordering = ["-sent_date"]

class Group(models.Model):
    admin = models.OneToOneField(Account,on_delete=SET_NULL,null=True)
    name = models.CharField(max_length=300,unique=True,null=True)
    bio = models.TextField(null=True)
    clients = models.ManyToManyField(ClientProfile)

    def save(self):
        self.save()

    def _str_(self):
        return self.name

class Counselling(models.Model):
	counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE, null=True)
	client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, null=True)
	date_contacted = models.DateField(default=timezone.now)

	def _str_(self):
		return f'{self.counsellor.user.username} and {self.client.user.username}'

	class Meta:
		ordering = ['-date_contacted',]

class Conversation(models.Model):
	client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, null=True)
	counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE, null=True)

	def _str_(self):
		return f"{self.client.user.username} and {self.counsellor.user.username}'s Conversation"


class Message(models.Model):
	conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True)
	text = models.TextField(null=True)
	time = models.DateTimeField(default=timezone.now, null=True)

	def _str_(self):
		return f"{self.conversation}"

	class Meta:
		ordering = ['-time',]

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
# class Prescription(models.Model):
#     prid=models.AutoField(primary_key=True)
#     clients = models.ForeignKey('ClientProfile', on_delete=models.CASCADE,null=True, related_name='clients')
#     counsel = models.OneToOneField('Counselor', on_delete=models.CASCADE, related_name='counsel')
#     prescription=models.TextField()
#     diagnosis=models.CharField(max_length=25)
#     date=models.DateTimeField(default=timezone.now)
#     def __str__(self):
#         return f'{self.prid}'
