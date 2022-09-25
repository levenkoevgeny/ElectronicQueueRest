# Generated by Django 4.1.1 on 2022-09-23 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_alter_organization_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='organization',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='appointment.organization', verbose_name='Organization'),
            preserve_default=False,
        ),
    ]