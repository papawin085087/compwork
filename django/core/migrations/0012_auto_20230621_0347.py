# Generated by Django 3.2.19 on 2023-06-21 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_checkin_check_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='employee_type',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='l_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]