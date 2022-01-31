from tokenize import group
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



class Counsellor(models.Model):
    user = models.OneToOneField(Account,null=False,on_delete=CASCADE,related_name="profile")

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
        


class Details(models.Model):
    counsellor = models.OneToOneField(Counsellor,on_delete=CASCADE,null=True)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    quantiles = models.TextField(null=True)
    experiences = models.TextField(null=True)


class Client(models.Model):
    user = models.OneToOneField(Account(client),null=False,on_delete=CASCADE,related_name="client_profile")
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