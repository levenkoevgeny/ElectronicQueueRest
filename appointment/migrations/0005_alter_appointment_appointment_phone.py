# Generated by Django 4.0.7 on 2022-09-26 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0004_queue_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Appointment phone'),
        ),
    ]
