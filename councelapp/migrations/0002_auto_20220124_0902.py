# Generated by Django 3.2.9 on 2022-01-24 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('councelapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='counsellor',
            old_name='account',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='counsellor',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='counsellor',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='counsellor',
            name='qualities',
        ),
        migrations.RemoveField(
            model_name='counsellor',
            name='work_experience',
        ),
    ]