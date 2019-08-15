# Generated by Django 2.2.4 on 2019-08-15 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricetable',
            name='club',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='golf.GolfClub', verbose_name='Golf club'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pricetable',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='golf.TravelAgent', verbose_name='Travel agent'),
            preserve_default=False,
        ),
    ]
