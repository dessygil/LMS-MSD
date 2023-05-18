# Generated by Django 3.2.8 on 2023-05-15 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_time_takes_machine_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machine',
            name='duration',
        ),
        migrations.AddField(
            model_name='machine',
            name='machine_type',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AddField(
            model_name='machineexperimentconnector',
            name='duration',
            field=models.DecimalField(decimal_places=2, default=3600, max_digits=8),
        ),
    ]
