# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-01 18:52
from __future__ import unicode_literals

from django.db import migrations, models
import impprice.models


class Migration(migrations.Migration):

    dependencies = [
        ('impprice', '0012_auto_20160901_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileprice',
            name='import_filenames',
            field=models.FileField(upload_to=impprice.models.get_upload_file_name, verbose_name='\u0424\u0430\u0439\u043b \u043f\u0440\u0430\u0439\u0441\u0430'),
        ),
    ]