# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-16 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='number_order',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='Номер заказа'),
        ),
    ]
