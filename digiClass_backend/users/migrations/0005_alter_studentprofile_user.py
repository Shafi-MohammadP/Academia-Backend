# Generated by Django 4.2.7 on 2023-12-28 07:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_customuser_phone_number_studentprofile_mobile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
