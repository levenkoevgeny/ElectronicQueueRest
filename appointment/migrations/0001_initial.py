# Generated by Django 4.0.2 on 2022-09-23 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('queue_name', models.CharField(max_length=255, verbose_name='Queue name')),
                ('date_time_added', models.DateTimeField(auto_now_add=True, verbose_name='Date time added')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is active')),
            ],
            options={
                'verbose_name': 'Queue',
                'verbose_name_plural': 'Queues',
                'ordering': ('queue_name',),
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.TextField(verbose_name='Organization name')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
                'ordering': ('organization_name',),
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=100, verbose_name='Last name')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointment.organization', verbose_name='Organization')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
                'ordering': ('last_name',),
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date_time', models.DateTimeField(verbose_name='Appointment date-time')),
                ('appointment_lastname', models.CharField(max_length=100, verbose_name='Appointment lastname')),
                ('appointment_firstname', models.CharField(blank=True, max_length=100, null=True, verbose_name='Appointment firstname')),
                ('appointment_patronymic', models.CharField(blank=True, max_length=100, null=True, verbose_name='Appointment patronymic')),
                ('appointment_email', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Appointment email')),
                ('appointment_phone', models.EmailField(blank=True, max_length=20, null=True, verbose_name='Appointment email')),
                ('date_time_added', models.DateTimeField(auto_now_add=True, verbose_name='Date time added')),
                ('is_booked', models.BooleanField(default=False, verbose_name='Booked')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointment.employee', verbose_name='Employee')),
                ('queue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointment.queue', verbose_name='Queue')),
            ],
            options={
                'verbose_name': 'Appointment',
                'verbose_name_plural': 'Appointments',
                'ordering': ('appointment_date_time',),
            },
        ),
    ]
