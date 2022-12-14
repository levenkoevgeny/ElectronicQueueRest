# Generated by Django 4.0.7 on 2022-09-30 16:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0007_rename_comment_appointment_appointment_comment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='First name'),
        ),
        migrations.AddField(
            model_name='employee',
            name='patronymic',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Patronymic'),
        ),
        migrations.AddField(
            model_name='employee',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='employees', verbose_name='Photo'),
        ),
        migrations.AlterField(
            model_name='queue',
            name='random_uuid',
            field=models.UUIDField(default=uuid.uuid4, verbose_name='UUID'),
        ),
    ]
