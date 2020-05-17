# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class Draft(models.Model):
    name = models.TextField(verbose_name=u'Название',max_length=128, blank=False)
    creation_date = models.DateTimeField(verbose_name= u'Дата')
    accounts = models.ForeignKey('lk.Accounts', verbose_name = u'Пользователь')

    class Meta:
        verbose_name = u'Черновик'
        verbose_name_plural = u'Черновики'
        ordering = ('-creation_date',)

    def __unicode__(self):
        return u'%s' % self.name

    def price_d(self):
        total_price = 0
        for p in self.positions_d.all():
            total_price += p.total_price_d()
        return total_price


class ItemD(models.Model):
    draft = models.ForeignKey(Draft,related_name='positions_d', verbose_name= u'Черновик')
    quantity = models.PositiveIntegerField(verbose_name= u'Кол-во')
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name= u'Цена')
    product = models.ForeignKey('catalog.Product', verbose_name= u'Товар',null=True ,on_delete=models.SET_NULL)
    stock = models.ForeignKey('catalog.Stock', verbose_name= u'Склад',null=True ,on_delete=models.SET_NULL)
    brand = models.ForeignKey('catalog.ProductManufacturer', verbose_name=u'Бренд', default=1,null=True ,on_delete=models.SET_NULL)

    class Meta:
        verbose_name = u'Позиция'
        verbose_name_plural = u'Позиции'
        ordering = ('draft',)

    def __unicode__(self):
        return u'%d units of %s' % (self.quantity, self.product.__class__.__name__)

    def total_price_d(self):
        return self.quantity * self.unit_price

   
