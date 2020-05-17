# -*- coding: utf-8 -*-
from django.db import models


class OrderStatus(models.Model): 
    name = models.CharField(verbose_name=u'Название',max_length=128)
    color = models.CharField(verbose_name=u'Цвет', max_length=7,
                             default='#000',
                             help_text=u'HEX цает, as #RRGGBB')
    
    class Meta: 
        verbose_name = 'Статус' 
        verbose_name_plural = 'Статусы' 
    
    def __unicode__(self):
        return u'%s' % self.name


class Order(models.Model): 
    number_order=models.AutoField(primary_key=True,verbose_name=u'Номер заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Создан')
    closed_at = models.DateTimeField(verbose_name=u'Закрыт', blank=True, null=True)
    status = models.ForeignKey('orders.OrderStatus',verbose_name=u'Статус',null=True ,on_delete=models.SET_NULL)
    accounts = models.ForeignKey('lk.Accounts',verbose_name=u'Пользователь',null=True ,on_delete=models.SET_NULL)
    address = models.CharField(max_length=256,verbose_name=u'Адрес', null=True)
    comment = models.TextField(verbose_name=u'Комментарий', null=True)
    name = models.CharField(max_length=64, verbose_name=u'Контактное лицо', null=True)
    
    class Meta: 
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'
        ordering = ('-created_at',)
    
    def __unicode__(self):
        return u'%s' % self.number_order
    
    def price(self): 
        total_price = 0 
        for p in self.positions.all(): 
            total_price += p.price() 
        return total_price
    #price.admin_order_field = 'pub_date'
    #price.boolean = True
    price.short_description = u'Сумма'


class OrderPosition(models.Model): 
    order = models.ForeignKey('Order', related_name='positions',verbose_name=u'Номер заказа')
    product = models.ForeignKey('catalog.Product',verbose_name=u'Товар', null=True ,on_delete=models.SET_NULL)
    id_stock = models.ForeignKey('catalog.Stock',verbose_name=u'Склад',default=1,null=True ,on_delete=models.SET_NULL)
    count = models.PositiveIntegerField(default=0,verbose_name=u'Количество')
    price_purchase = models.DecimalField(max_digits=18, decimal_places=2,default=0,verbose_name=u'Закупка')
    price_sale = models.DecimalField(max_digits=18, decimal_places=2,default=0,verbose_name=u'Цена')
    brand = models.ForeignKey('catalog.ProductManufacturer', verbose_name=u'Бренд', default=1,null=True ,on_delete=models.SET_NULL)
    invoice = models.ForeignKey('supplier.Invoice', verbose_name=u'Накладная', null=True, on_delete=models.SET_NULL)
    status_order = models.PositiveIntegerField(verbose_name=u'Статус запчасти', default=0)

    class Meta: 
        verbose_name = u'Позиция заказа'
        verbose_name_plural = u'Позиции заказа'
        ordering = ['-count']
        
        
    def __unicode__(self):
        return u'%s' % self.product.partnumber
     
    def price(self): 
        return self.price_sale * self.count


