from tkinter import CASCADE
from django.db import models

from counsel_users.models import Account

class Counsellor(models.Model):
    account = models.ForeignKey(Account,on_delete=CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    qualities = models.TextField()
    work_experience = models.TextField()
