# Generated by Django 4.2.7 on 2024-02-13 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0016_videoscourse_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.DecimalField(decimal_places=1, max_digits=3)),
                ('text', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='course.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
