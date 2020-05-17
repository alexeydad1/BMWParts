# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-01 12:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_orderposition_brand'),
        ('offer', '0003_auto_20161001_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='orders.OrderStatus', verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441'),
        ),
    ]
