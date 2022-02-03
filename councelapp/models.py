from tokenize import group
from urllib import request
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from django.db.models.deletion import CASCADE, SET_NULL
from django.db import models

from counsel_users.models import Account
counsellor = Account.objects.filter(is_counsellor=True)
client = Account.objects.filter(is_counsellor=False)

class Group(models.Model):
    name = models.CharField(max_length=300,unique=True,null=True)
    admin = models.ForeignKey(Account,on_delete=SET_NULL,null=True)
    bio = models.TextField(null=True)

class GroupChat(models.Model):
    group = models.ForeignKey(Group,on_delete=SET_NULL,null=True)
    reporter = models.ForeignKey(Account,on_delete=CASCADE,null=True)
    text = models.TextField()
    time_sent = models.DateTimeField(auto_now_add=True,null=True)

    def get_messages(pk):
        """This returns all the messages sent in a group
        Args:
            pk ([type]): [description]
        """
        group = Group.objects.get(pk = pk)
        messages = GroupChat.objects.filter(group = group)

        return messages

class Details(models.Model):
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    qualities = models.TextField(null=True)
    experiences = models.TextField(null=True)


class Counsellor(models.Model):
    user = models.OneToOneField(Account,null=False,on_delete=CASCADE,related_name="profile")
    details = models.ForeignKey(Details,null=True,on_delete=CASCADE,related_name="details")

    def __str__(self):
        return self.user.username + "'s " + "profile"

    @receiver(post_save, sender=Account)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Counsellor.objects.create(user=instance)

    @receiver(post_save, sender=Account)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def get_counsellors():
        counsellors = Account.objects.filter(is_counsellor=True)
        return counsellors

    def get_single_counsellor(pk):
        user = Account.objects.get(pk=pk)
        counsellor = Counsellor.objects.get(user=user)
        return counsellor
        

class Client(models.Model):
    user = models.OneToOneField(Account(client),null=False,on_delete=CASCADE,related_name="client_profile")
    counsellor = models.ForeignKey(Counsellor,null=True,blank=True,on_delete=models.SET_NULL,related_name="counsellor")
    group = models.ForeignKey(Group,on_delete=SET_NULL,null=True)

    def __str__(self):
        return self.user.username + "'s " + "profile"

    @receiver(post_save, sender=Account)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Client.objects.create(user=instance)

    @receiver(post_save, sender=Account)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def get_clients(pk):
        """This will return all users in a given neighbourhood
        Args:
            pk ([type]): [description]
        Returns:
            [type]: [description]
        """
        counsellor = Counsellor.objects.get(pk=pk)
        clients = Client.objects.filter(counsellor = counsellor)

        return clients

class Appointment(models.Model):
    user = models.ForeignKey(Account,on_delete=CASCADE,null=True)
    date = models.DateField()
    topic = models.TextField()

    def delete_appointment(self):
        """This deletes the image from the database using its pk
        Args:
            id ([type]): [description]
        """
        self.delete()

    def get_appointments():
        """This will return all users in a given neighbourhood
        Args:
            pk ([type]): [description]
        Returns:
            [type]: [description]
        """
        appointments = Appointment.objects.filter(client__counsellor = counsellor)

        return appointments