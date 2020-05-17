# -*- coding: utf-8 -*-
from django.contrib import admin
from offer.models import Offer,ItemOffer,Customer,Works,WorkOffer
# Register your models here.
class WorksAdmin(admin.ModelAdmin):
    list_display=('number',
                  'name',)
    search_fields = ['number','name']
    
    class Meta:
        verbose_name_plural = u"Работа СТО"  
        verbose_name = u"Работы СТО"
        

admin.site.register(Works,WorksAdmin)
admin.site.register(Offer)
admin.site.register(ItemOffer)
admin.site.register(Customer)
admin.site.register(WorkOffer)
