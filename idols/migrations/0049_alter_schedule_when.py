# Generated by Django 4.1.7 on 2023-03-11 09:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idols', '0048_alter_schedule_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='when',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 11, 9, 22, 55, 797695, tzinfo=datetime.timezone.utc)),
        ),
    ]
