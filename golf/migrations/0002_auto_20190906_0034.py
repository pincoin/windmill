# Generated by Django 2.2.4 on 2019-09-05 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.IntegerField(choices=[(0, 'order pending'), (1, 'payment_pending'), (2, 'voucher issued'), (3, 'order revoked'), (4, 'refund requested'), (5, 'refund pending'), (6, 'order refunded(original)'), (7, 'order refunded(reverse)'), (8, 'order voided')], db_index=True, default=0, verbose_name='Booking status'),
        ),
    ]