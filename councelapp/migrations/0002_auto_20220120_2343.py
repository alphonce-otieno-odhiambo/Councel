# Generated by Django 3.2.7 on 2022-01-20 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('councelapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='description',
            field=models.TextField(default=0, max_length=10000),
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.CharField(default=0, max_length=200),
        ),
    ]
