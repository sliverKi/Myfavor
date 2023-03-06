# Generated by Django 4.1.7 on 2023-03-06 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0008_alter_category_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='type',
            field=models.CharField(blank=True, choices=[('broadcast', 'BROADCASTS'), ('event', 'EVENTS'), ('release', 'RELEASES'), ('congrats', 'CONGRATS'), ('sns', 'SNS'), ('etc', 'ETC')], default='', max_length=15),
        ),
    ]