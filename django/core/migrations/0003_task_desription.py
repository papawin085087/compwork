# Generated by Django 3.2.19 on 2023-06-19 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='desription',
            field=models.TextField(blank=True),
        ),
    ]