# Generated by Django 4.2.7 on 2024-01-12 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0003_certificate_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='notification',
        ),
    ]
