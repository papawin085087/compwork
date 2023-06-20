# Generated by Django 3.2.19 on 2023-06-19 06:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('content', models.TextField(blank=True)),
                ('date_start', models.DateField(auto_now_add=True)),
                ('date_end', models.DateField(blank=True, null=True)),
                ('time_start', models.TimeField(auto_now_add=True)),
                ('time_end', models.TimeField(blank=True, null=True)),
                ('task_status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
