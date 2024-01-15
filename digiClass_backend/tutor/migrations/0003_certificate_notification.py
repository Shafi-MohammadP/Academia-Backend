# Generated by Django 4.2.7 on 2024-01-06 04:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
        ('tutor', '0002_certificate_delete_teachercertificate'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='notification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='notifications.adminnotifications'),
        ),
    ]