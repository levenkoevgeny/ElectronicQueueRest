# Generated by Django 4.0.7 on 2022-09-29 14:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0006_queue_random_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='comment',
            new_name='appointment_comment',
        ),
        migrations.AlterField(
            model_name='queue',
            name='random_uuid',
            field=models.UUIDField(default=uuid.uuid4, verbose_name='Is active'),
        ),
    ]
