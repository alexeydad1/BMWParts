# -*- coding: utf-8 -*-
from django.contrib import admin
from draft.models import Draft,ItemD


# Register your models here.
class ItemInline(admin.TabularInline):
    model = ItemD


class ItemAdmin(admin.ModelAdmin):
    list_display = ('draft',
                    'product',
                    'stock',)
    class Meta:
        verbose_name_plural = u'Позиция черновика'
        verbose_name = u'Позиции черновиков'

class DraftAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
   ]
    list_display = ('pk',
                    'name',
                    'creation_date',
                    'accounts',)

    class Meta:
        verbose_name_plural = u'Черновик'
        verbose_name = u'Черновики'


admin.site.register(Draft, DraftAdmin)
admin.site.register(ItemD)


