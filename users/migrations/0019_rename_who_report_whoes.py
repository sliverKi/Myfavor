# Generated by Django 4.1.7 on 2023-03-12 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_report_who'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='who',
            new_name='whoes',
        ),
    ]
