# Generated by Django 4.2.7 on 2024-02-12 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0012_remove_coursepurchase_is_purchased'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
