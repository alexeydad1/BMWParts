# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-25 13:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20160403_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrossProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productnumber', models.BigIntegerField(unique=True, verbose_name='Номер запчасти')),
                ('crossnumber', models.TextField(verbose_name='Кросс Номера')),
            ],
            options={
                'verbose_name_plural': 'Кросс Номера',
                'verbose_name': 'Кросс Номер',
            },
        ),
    ]
