# Generated by Django 4.2.7 on 2024-01-03 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_alter_coursecategory_is_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_name',
            field=models.CharField(default=None, max_length=100),
        ),
    ]