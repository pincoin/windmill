# Generated by Django 2.2.4 on 2019-09-07 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='fullname',
            field=models.CharField(default='', max_length=255, verbose_name='Full name'),
            preserve_default=False,
        ),
    ]
