# Generated by Django 3.2.19 on 2023-06-26 01:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkin',
            name='check_out_time',
        ),
        migrations.AlterField(
            model_name='checkin',
            name='check_status',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.CreateModel(
            name='CheckOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_status', models.BooleanField(blank=True, default=False, null=True)),
                ('check_out_time', models.DateTimeField(auto_now_add=True)),
                ('check_in', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.checkin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
