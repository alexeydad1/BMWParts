# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-19 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20160404_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(null=True, verbose_name='Комментарий'),
        ),
    ]