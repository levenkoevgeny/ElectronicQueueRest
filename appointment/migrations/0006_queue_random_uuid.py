# Generated by Django 4.0.7 on 2022-09-28 19:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0005_alter_appointment_appointment_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='random_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Is active'),
        ),
    ]