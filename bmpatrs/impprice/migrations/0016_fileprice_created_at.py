# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-11 18:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('impprice', '0015_auto_20160914_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileprice',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='\u0421\u043e\u0437\u0434\u0430\u043d'),
            preserve_default=False,
        ),
    ]