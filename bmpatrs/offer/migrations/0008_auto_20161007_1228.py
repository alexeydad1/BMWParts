# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-07 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0007_auto_20161001_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d'),
        ),
    ]
