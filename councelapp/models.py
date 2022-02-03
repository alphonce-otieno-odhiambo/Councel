from django.db import models
from cloudinary.models import CloudinaryField

from counsel_users.models import Account
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django.db.models.deletion import CASCADE, SET_NULL

# Create your models here.
class ClientProfile(models.Model):
    user = models.OneToOneField(Account,null=False,on_delete=CASCADE,related_name="client_profile")
    counsellor = models.ForeignKey('Counsellor',null=True,blank=True,on_delete=models.SET_NULL,related_name="counsellor")

    def __str__(self):
        return self.user.username + "'s " + "profile"

    @receiver(post_save, sender=Account)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ClientProfile.objects.create(user=instance)

    @receiver(post_save, sender=Account)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Group(models.Model):
    admin = models.OneToOneField(Account,on_delete=SET_NULL,null=True)
    name = models.CharField(max_length=300,unique=True,null=True)
    bio = models.TextField(null=True)
    clients = models.ManyToManyField(ClientProfile)

    def save(self):
        self.save()

    def __str__(self):
        return self.name


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

    def __str__(self):
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



    def __str__(self):
        return self.user.username + "'s " + "profile"

    @receiver(post_save, sender=Account)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ClientProfile.objects.create(user=instance)

class Counselling(models.Model):
	counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE, null=True)
	client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, null=True)
	date_contacted = models.DateField(default=timezone.now)

	def __str__(self):
		return f'{self.counsellor.user.username} and {self.client.user.username}'

	class Meta:
		ordering = ['-date_contacted',]


class Conversation(models.Model):
	client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, null=True)
	counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return f"{self.client.user.username} and {self.counsellor.user.username}'s Conversation"


class Message(models.Model):
	conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True)
	text = models.TextField(null=True)
	time = models.DateTimeField(default=timezone.now, null=True)

	def __str__(self):
		return f"{self.conversation}"

	class Meta:
		ordering = ['-time',]
