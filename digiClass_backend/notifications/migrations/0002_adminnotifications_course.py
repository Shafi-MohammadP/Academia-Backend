# Generated by Django 4.2.7 on 2024-01-17 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_alter_course_price'),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminnotifications',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
    ]