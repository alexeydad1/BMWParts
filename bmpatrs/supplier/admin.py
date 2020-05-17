# -*- coding: utf-8 -*-
from django.contrib import admin

from supplier.models import Supplier,Invoice,ItemInvoice

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name','inn','get_stock_name']



admin.site.register(Supplier,SupplierAdmin)
admin.site.register(Invoice)
admin.site.register(ItemInvoice)

