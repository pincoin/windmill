# Generated by Django 2.2.4 on 2019-09-08 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0002_booking_fullname'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='tee_off_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Tee off time'),
        ),
    ]
