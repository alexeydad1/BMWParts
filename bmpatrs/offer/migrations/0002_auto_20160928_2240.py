# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-28 19:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemoffer',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions_offer', to='offer.Offer', verbose_name='\u0417\u0430\u044f\u0432\u043a\u0430'),
        ),
    ]