# Generated by Django 4.1.7 on 2023-03-10 12:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idols', '0027_alter_schedule_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='when',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 10, 12, 3, 54, 5548, tzinfo=datetime.timezone.utc)),
        ),
    ]
