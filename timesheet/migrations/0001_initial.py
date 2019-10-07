# Generated by Django 2.2.4 on 2019-09-17 11:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Staff')),
            ],
            options={
                'verbose_name': 'Time sheet',
                'verbose_name_plural': 'Time sheets',
            },
        ),
        migrations.CreateModel(
            name='PunchLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('status', models.IntegerField(choices=[(0, 'Punch-in'), (1, 'Punch-out')], db_index=True, default=0, verbose_name='Punch status')),
                ('punch_time', models.DateTimeField(verbose_name='Punch time')),
                ('punch_latitude', models.DecimalField(decimal_places=16, max_digits=22, verbose_name='Punch latitude')),
                ('punch_longitude', models.DecimalField(decimal_places=16, max_digits=22, verbose_name='Punch longitude')),
                ('user_agent', models.TextField(blank=True, verbose_name='user-agent')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP address')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='Memo')),
                ('sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timesheet.TimeSheet', verbose_name='Time sheet')),
            ],
            options={
                'verbose_name': 'Punch log',
                'verbose_name_plural': 'Punch logs',
            },
        ),
    ]
