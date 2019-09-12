# Generated by Django 2.2.4 on 2019-09-11 17:04

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('booking_date', models.DateField(db_index=True, verbose_name='Booking date')),
                ('counter', models.PositiveIntegerField(db_index=True, default=0, verbose_name='Booking counter')),
                ('day_of_week', models.IntegerField(choices=[(0, 'Weekday'), (1, 'Weekend')], db_index=True, default=0, verbose_name='Day of week')),
            ],
            options={
                'verbose_name': 'Booking counter',
                'verbose_name_plural': 'Booking counters',
                'ordering': ('-booking_date',),
                'unique_together': {('booking_date',)},
            },
        ),
    ]