# Generated by Django 3.2.19 on 2023-06-19 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_task_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='description',
            new_name='content',
        ),
    ]