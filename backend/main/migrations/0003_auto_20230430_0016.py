# Generated by Django 3.2.8 on 2023-04-30 00:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_sample_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="experiment",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="machine",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="machineexperimentconnector",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="sample",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="usersampleconnector",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
