# Generated by Django 4.1.7 on 2023-03-11 08:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_report_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
