from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField, related
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from cloudinary.models import CloudinaryField
from django.utils import timezone
# Create your models here.
class CounselorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=50)
    bio = models.CharField(max_length=300)
    profile_pic =CloudinaryField('image')

    def _str_(self):
        return f'{self.user.username} profile'
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
             CounselorProfile.objects.create(user=instance)
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()