# Generated by Django 4.2.7 on 2024-01-12 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_studentprofile_qualification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='qualification',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
