# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-16 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('impprice', '0005_auto_20151216_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='partnumber',
            field=models.BigIntegerField(verbose_name='Номер запчасти'),
        ),
    ]
