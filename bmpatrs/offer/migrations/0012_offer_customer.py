# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-12 17:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0011_itemoffer_status_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='customer',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='offer.Customer', verbose_name='\u041a\u043b\u0438\u0435\u043d\u0442'),
        ),
    ]
