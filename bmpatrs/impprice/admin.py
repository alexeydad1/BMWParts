# -*- coding: utf-8 -*- 
from django.contrib import admin
from .models import FilePrice
import csv
  
class FilePriceAdmin(admin.ModelAdmin):
    list_display=['stock','import_filenames']
    
    class Meta:
        verbose_name = "Прайс лист" 
        verbose_name_plural = "Прайс листы"  
        

'''class PriceAdmin(admin.ModelAdmin):
    list_display=['partnumber',
                  'description_part',
                  'quantity_stock_spb',
                  'quantity_stock_msk',
                  'purchase_price',
                  'our_price']
    
    
    pass
    class Meta:
        verbose_name_plural = "Цены"  
admin.site.register(Price, PriceAdmin)'''
admin.site.register(FilePrice, FilePriceAdmin)