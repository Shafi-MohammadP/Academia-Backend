# Generated by Django 4.2.7 on 2024-01-12 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_customuser_is_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorprofile',
            name='is_certificate',
            field=models.BooleanField(default=False),
        ),
    ]