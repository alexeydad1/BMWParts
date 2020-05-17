# -*- coding: utf-8 -*-
from django.db import models
from time import time,strftime,localtime
import datetime
from catalog.models import Stock
import csv

def get_upload_file_name(instance,filename):
	return "%s_%s" % (strftime('%d_%m_%Y_%H_%M_%S', localtime(time())),filename)


class FilePrice(models.Model):
    import_filenames = models.FileField(upload_to=get_upload_file_name,verbose_name='Файл прайса')# Название файла загрузки
    stock = models.ForeignKey('catalog.Stock',verbose_name='Склад',default=1,null=True ,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Создан')
    
    def __unicode__(self):
        return u'%s' % self.import_filenames

    class Meta:
    	verbose_name='Прайс'
    	verbose_name_plural='Прайсы'
    	ordering = ('-created_at',)


   
    


