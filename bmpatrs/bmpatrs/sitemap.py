# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from catalog.models import Product
from django.core.urlresolvers import reverse


class DinamicSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def location(self, product):
        return "/search?partnumber=" + product.partnumber




class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return ['home','ContactsPage','SalePage','NewsPage','AboutUsPage','DeliveryPaymentPage','oil_tech']

    def location(self, object):
        return reverse(object)