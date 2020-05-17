# -*- coding: utf-8 -*-
from django.contrib import admin
from orders.models import Order, OrderPosition,OrderStatus

# Register your models here.

# class OrderPositionInline(admin.StackedInline):
#     model = OrderPosition
#     extra = 3
    

class OrderAdmin(admin.ModelAdmin):

    list_display = ('number_order',
                      'created_at',
                      'status',
                      'accounts',
                      'address',
                      'comment',
                      'name',
                      'closed_at',
                      'price',)


    #inlines = [OrderPositionInline]

    class Meta:
        verbose_name_plural = "Заказ"
        verbose_name = "Заказы"


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderStatus)
admin.site.register(OrderPosition)
