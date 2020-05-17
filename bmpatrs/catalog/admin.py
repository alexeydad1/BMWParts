# -*- coding: utf-8 -*-
from django.contrib import admin
from catalog.models import Product,ProductCategory,Stock,Price,CrossProduct,ProductManufacturer
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=('partnumber',
                  'description',
                  'category',
                  'create_date',
                  'image',
                  'bit',)
    search_fields = ['partnumber']
    class Meta:
        verbose_name_plural = "Товар"  
        verbose_name = "Товары"

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display=('name',)
    search_fields = ['name']

    class Meta:
        verbose_name_plural = "Категория"  
        verbose_name = "Категории"
        
class CrossProductAdmin(admin.ModelAdmin):
    list_display=('productnumber',
                  'crossnumber',)
    search_fields = ['productnumber','crossnumber']

    class Meta:
        verbose_name_plural = "Кросс номер"  
        verbose_name = "Кросс Номера"
        
class StockAdmin(admin.ModelAdmin):
    list_display=('name_stock',
                  'delivery_time',
                  'color_stock',)
    
    class Meta:
        verbose_name_plural = "Склад"  
        verbose_name = "Склады"
        
class PriceAdmin(admin.ModelAdmin):
    list_display=('p_product',
                  'id_stock',
                  'qty',
                  'purchase_price',
                  'our_price',)
    search_fields = ['p_product', 'id_stock__name_stock']
    class Meta:
        verbose_name_plural = "Цена"  
        verbose_name = "Цены"

class ProductManufacturerAdmin(admin.ModelAdmin):
    list_display=('name',
                  'margin',)
    search_fields = ['name']
    class Meta:
        verbose_name_plural = "Производитель"  
        verbose_name = "Производители"
          
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductCategory,ProductCategoryAdmin)
admin.site.register(Stock,StockAdmin)
admin.site.register(Price,PriceAdmin)
admin.site.register(CrossProduct,CrossProductAdmin)
admin.site.register(ProductManufacturer,ProductManufacturerAdmin)