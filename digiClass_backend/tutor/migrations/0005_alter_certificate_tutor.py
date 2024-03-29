# Generated by Django 4.2.7 on 2024-02-22 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_tutorprofile_user'),
        ('tutor', '0004_remove_certificate_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutor_certificate', to='users.tutorprofile'),
        ),
    ]
