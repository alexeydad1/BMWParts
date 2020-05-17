# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-03 13:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20160217_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderposition',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Product', verbose_name='Товар'),
        ),
    ]