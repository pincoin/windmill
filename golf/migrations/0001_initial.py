# Generated by Django 2.2.4 on 2019-08-15 16:29

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GolfClub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='Golf club name')),
                ('phone', models.CharField(blank=True, max_length=16, null=True, verbose_name='Phone number')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email address')),
                ('website', models.URLField(blank=True, max_length=255, null=True, verbose_name='Website')),
            ],
            options={
                'verbose_name': 'Golf club',
                'verbose_name_plural': 'Golf clubs',
            },
        ),
        migrations.CreateModel(
            name='TravelAgent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='Travel agent name')),
                ('bank_account', models.CharField(blank=True, max_length=255, null=True, verbose_name='Bank account')),
                ('phone', models.CharField(max_length=16, verbose_name='Phone number')),
                ('email', models.EmailField(max_length=255, verbose_name='Email address')),
                ('website', models.URLField(blank=True, max_length=255, null=True, verbose_name='Website')),
                ('deposit', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='Deposit amount')),
                ('memo', models.TextField(blank=True, help_text='A short description', null=True, verbose_name='Memo')),
            ],
            options={
                'verbose_name': 'Travel agent',
                'verbose_name_plural': 'Travel agents',
            },
        ),
    ]
