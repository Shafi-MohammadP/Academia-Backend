# Generated by Django 4.2.7 on 2024-02-12 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0015_coursevideolikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoscourse',
            name='likes',
            field=models.IntegerField(default=True),
        ),
    ]
