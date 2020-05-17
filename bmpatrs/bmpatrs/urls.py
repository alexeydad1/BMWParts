# -*- coding: utf-8 -*-
"""bmpatrs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from catalog import views as cat
from cart import views as Cart
from orders import views as orders
from lk import views as lk_w
from staticpage import views as staticPage
from impprice import views as impprice
from draft import views as draft
from offer import views as offer
from offer.forms import CustomerForm
from supplier import views as supplier

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from sitemap import DinamicSitemap, StaticSitemap

from django.contrib.sitemaps.views import sitemap, index

sitemaps = {'products': DinamicSitemap, 'static': StaticSitemap}

urlpatterns = [
    url(r'^robots.txt$', staticPage.robots, name='robots'),
    url(r'^sitemap\.xml$', index, {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^search/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)/$', cat.search, name='search'),
    url(r'^search', cat.search, name='search'),
    url(r'^inquiry/([a-zA-Z0-9]+)/$', cat.inquiry_part, name='inquiry_part'),
    url(r'^to_all_bmw/$', cat.to_all_bmw, name='to_all_bmw'),

    url(r'^to_model_([a-zA-Z0-9]+)_series/([a-zA-Z0-9 ]+)/([a-zA-Z0-9 ]+)/$', cat.model_to, name='model_to'),
    url(r'^to_model_([a-zA-Z0-9]+)_series/$', cat.model_to, name='model_to'),

    url(r'^motor_oil_technical_liquids/$', cat.oil_tech, name='oil_tech'),
    # url(r'^catalog_online/',cat.parser_ilcats, name='parser_ilcats'),
    url(r'^lk/logout/$', lk_w.logout, name='logout'),
    url(r'^lk/login/$', lk_w.login, name='login'),
    url(r'^lk/singup/$', lk_w.singup, name='singup'),
    url(r'^lk/$', lk_w.lk, name='lk'),

    url(r'^lk/offers/$', offer.get_offers, name='get_offers'),
    url(r'^lk/users/$', lk_w.get_users, name='get_users'),
    url(r'^lk/user_detail/(?P<username>.+)/$', lk_w.user_detail, name='user_detail'),
    url(r'^lk/user/(\d+)/replenish_balance/$', lk_w.account_replenish_balance, name='account_replenish_balance'),
    url(r'^lk/new_offer/$', offer.new_offer, name='new_offer'),
    url(r'^lk/offer_detail/(\d+)/$', offer.offer_detail, name='offer_detail'),
    url(r'^lk/offer_save/(\d+)/$', offer.offer_save, name='offer_save'),
    url(r'^lk/offeritem_update/(\d+)/$', offer.offeritem_update, name='offeritem_update'),
    url(r'^lk/offerworks_update/(\d+)/$', offer.offerworks_update, name='offerworks_update'),
    url(r'^add_to_offer/([a-zA-Z0-9]+)_(\d+)_(\d+)_(\d+)/$', offer.add_to_offer, name='add_to_offer'),
    url(r'^del_offer_item/([a-zA-Z0-9]+)_(\d+)_(\d+)_(\d+)/$', offer.offer_item_del, name='offer_item_del'),
    url(r'^lk/customer_offer_add/(\d+)/(\d+)/$', offer.customer_offer_add, name='customer_offer_add'),
    url(r'^lk/del_work/(\d+)/$', offer.del_works, name='offer.del_works'),

    url(r'^lk/offer_print/(\d+)/$', offer.offer_print, name='offer_print'),
    url(r'^lk/offer_print/(\d+)/(\d+)/$', offer.offer_print, name='offer_print'),
    url(r'^lk/offer_print_labels/(\d+)/$', offer.offer_print_labels, name='offer_print_labels'),

    url(r'^lk/customers/$', offer.get_customers, name='get_customers'),
    url(r'^lk/search_customer/$', offer.search_customer, name='search_customer'),
    url(r'^lk/search_works/(\d+)/$', offer.search_works, name='search_works'),

    url(r'^lk/customer/(\d+)/replenish_balance/$', offer.customer_replenish_balance, name='customer_replenish_balance'),
    url(r'^lk/customer/(\d+)/$', offer.customer_detail, name='customer_detail'),
    url(r'^lk/new_customer/$', offer.table_edit, {'Form': CustomerForm, 'redirect_url': '/lk/customers/'}),
    url(r'^lk/edit_customer/(\d+)/$', offer.table_edit, {'Form': CustomerForm, 'redirect_url': '/lk/customers/'}),
    url(r'^lk/del_customer/(\d+)/$', offer.del_customer, name='del_customers'),

    url(r'^lk/statistics/$', offer.get_statistics, name='get_statistics'),

    url(r'^lk/invoices/$', supplier.get_invoces, name='get_invoices'),
    url(r'^lk/invoice/(\d+)/$', supplier.get_invoice, name='get_invoice'),
    url(r'^lk/invoice_update/(\d+)/$', supplier.invoice_update, name='invoice_update'),
    url(r'^lk/invoice_order/(\d+)/$', supplier.invoice_order, name='invoice_order'),
    url(r'^lk/invoice_accept/(\d+)/$', supplier.invoice_accept, name='invoice_accept'),
    url(r'^lk/make_invoices/$', supplier.make_invoices, name='make_invoices'),
    url(r'^lk/del_invoice/(\d+)/$', supplier.del_invoice, name='del_invoice'),

    # url(r'street_edit/$', offer.table_edit, {'Form': CustomerForm, 'redirect_url': '/street_list'}, name='street_edit_new'),
    # url(r'street_edit/(\d+)/$', offer.table_edit, {'Form': CustomerForm, 'redirect_url': '/street_list'}, name='street_edit'),


    url(r'^lk/orders/$', lk_w.lk_orders, name='lk_orders'),
    url(r'^lk/order_detail/(\d+)/$', lk_w.lk_order, name='lk_order'),

    url(r'^lk/drafts/$', draft.drafts, name='drafts'),
    url(r'^lk/add_to_draft/$', draft.add_to_draft_old, name='add_to_draft_old'),
    url(r'^lk/add_draft/$', draft.add_to_draft, name='add_to_draft'),

    url(r'^lk/draft_detail/(\d+)/$', draft.draft_detail, name='draft_detail'),
    url(r'^lk/update_draft/(\d+)/$', draft.draft_update, name='draft_update'),
    url(r'^del_draft_item/([a-zA-Z0-9]+)_(\d+)_(\d+)_(\d+)/$', draft.draft_item_del, name='draft_item_del'),
    url(r'^del_draft/(\d+)/$', draft.draft_del, name='draft_del'),

    # url(r'^add_to_cart/(\d+)/$',cat.add_cart,name='add_cart'),
    url(r'^add_to_cart/([a-zA-Z0-9]+)_(\d+)_(\d+)_(\d+)/$', Cart.add_to_cart, name='add_to_cart'),
    url(r'^del_cart/([a-zA-Z0-9]+)_(\d+)_(\d+)/$', Cart.remove_from_cart, name='remove_from_cart'),
    url(r'^update_cart/$', Cart.update_cart, name='update_cart'),
    url(r'^cart/$', Cart.get_cart, name='get_cart'),

    url(r'^order/$', orders.order, name='order'),
    url(r'^order_finish/$', orders.order_finish, name='order_finish'),
    url(r'^order_draft/(\d+)/$', orders.orderDraft, name='orderDraft'),
    url(r'^lk/import_price/$', impprice.import_csv3, name='import_csv3'),
    url(r'^lk/done_make_csv/$', impprice.make_csv, name='make_csv'),
    url(r'^lk/make_csv/$', impprice.make_csv, name='make_csv'),

    url(r'^lk/make_csv/(?P<name>.+)/$', impprice.download_csv, name='download_csv'),
    # статичные страницы
    url(r'^contacts/$', staticPage.ContactsPage, name='ContactsPage'),
    url(r'^about_us/$', staticPage.AboutUsPage, name='AboutUsPage'),
    url(r'^sale/$', staticPage.SalePage, name='SalePage'),
    url(r'^delivery_payment/$', staticPage.DeliveryPaymentPage, name='DeliveryPaymentPage'),
    url(r'^news/$', staticPage.NewsPage, name='NewsPage'),

    url(r'^$', cat.home, name='home'),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )