# Generated by Django 4.1.7 on 2023-03-21 06:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idols', '0003_alter_schedule_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='when',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 21, 6, 52, 37, 96364, tzinfo=datetime.timezone.utc)),
        ),
    ]