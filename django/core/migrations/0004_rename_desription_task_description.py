# Generated by Django 3.2.19 on 2023-06-19 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_task_desription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='desription',
            new_name='description',
        ),
    ]