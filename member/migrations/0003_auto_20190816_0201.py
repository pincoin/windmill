# Generated by Django 2.2.4 on 2019-08-16 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_profile_agency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='agency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='golf.Agency', verbose_name='Agency'),
        ),
    ]
