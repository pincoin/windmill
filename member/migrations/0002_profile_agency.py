# Generated by Django 2.2.4 on 2019-08-16 01:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0002_auto_20190816_0153'),
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='agency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='golf.Agency', verbose_name='Agency'),
            preserve_default=False,
        ),
    ]
