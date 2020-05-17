# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,render_to_response,get_object_or_404
from cart.Cart import Cart
from django.template.context_processors import csrf
from django.contrib import auth
from offer.models import ItemOffer,Offer,Customer,BalanceHistory
from orders.models import OrderPosition,Order
from lk.models import Accounts,BalanceHistoryAccounts
from supplier.models import Invoice,ItemInvoice,Supplier
from django.views.decorators.csrf import csrf_protect
from decimal import *

def get_invoces(request):
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    args = {}
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username

    if request.user.is_authenticated() and request.user.is_staff:
        invoices = Invoice.objects.all()
        args['invoices'] = invoices
        return render(request, "supplier/invoices.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


def get_invoice(request,id_invoice):
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    args = {}
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username

    if request.user.is_authenticated() and request.user.is_staff:
        itemInvoice = ItemInvoice.objects.select_related().filter(invoice=id_invoice)
        args['invoice'] = itemInvoice[0].invoice
        args['itemInvoice'] = itemInvoice
        return render(request, "supplier/invoice_detail.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


def listmerge1(lst1,lst2):
    all=[]
    for lst in lst1:
        all.append(lst)
    for lst in lst2:
        all.append(lst)
    return all


def make_invoices(request):
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    args = {}
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username

    if request.user.is_authenticated() and request.user.is_staff:
        itemOffer = ItemOffer.objects.select_related().filter(offer__status_id=2, status_offer=0).order_by('stock')
        itemOrder = OrderPosition.objects.select_related().filter(order__status_id=2, status_order=0).order_by('id_stock')
        stock_list = listmerge1([item.stock.pk for item in itemOffer],[item.id_stock.pk for item in itemOrder])
        suppliers = Supplier.objects.filter(stock__in=stock_list).distinct()

        for sup in suppliers:
            for stk in sup.stock.all():
                # Обработка заявок
                if len(itemOffer.filter(stock=stk)) or len(itemOrder.filter(id_stock=stk)):
                    invoice = Invoice()
                    invoice.supplier = sup
                    invoice.stock_sup = stk
                    invoice.save()

                    for item in itemOffer.filter(stock=stk,offer__status_id=2).order_by('product'):
                        try:
                            iteminvoice = ItemInvoice.objects.get(
                                invoice=invoice,
                                product=item.product,
                                stock=item.stock,
                                brand=item.brand,
                            )
                        except ItemInvoice.DoesNotExist:
                            iteminvoice = ItemInvoice()
                            iteminvoice.invoice = invoice
                            iteminvoice.quantity = item.quantity
                            iteminvoice.quantity_in = item.quantity
                            iteminvoice.purchase_price = item.purchase_price
                            iteminvoice.product = item.product
                            iteminvoice.stock = item.stock
                            iteminvoice.brand = item.brand
                            iteminvoice.save()
                            iteminvoice.offers.add(item.offer)
                            iteminvoice.save()
                            item.status_offer = 1
                            item.invoice = invoice
                            item.save()

                        else:  # ItemAlreadyExists
                            iteminvoice.quantity += item.quantity
                            iteminvoice.quantity_in += item.quantity
                            iteminvoice.offers.add(item.offer)
                            iteminvoice.save()
                            item.status_offer = 1
                            item.invoice = invoice
                            item.save()

                # Обработка ЗАКАЗОВ
                    for item in itemOrder.filter(id_stock=stk, order__status_id=2).order_by('product'):
                        try:
                            iteminvoice = ItemInvoice.objects.get(
                                invoice=invoice,
                                product=item.product,
                                stock=item.id_stock,
                                brand=item.brand,
                            )
                        except ItemInvoice.DoesNotExist:
                            iteminvoice = ItemInvoice()
                            iteminvoice.invoice = invoice
                            iteminvoice.quantity = item.count
                            iteminvoice.quantity_in = item.count
                            iteminvoice.purchase_price = item.price_purchase
                            iteminvoice.product = item.product
                            iteminvoice.stock = item.id_stock
                            iteminvoice.brand = item.brand
                            iteminvoice.save()
                            iteminvoice.orders.add(item.order)
                            iteminvoice.save()
                            item.status_order = 1
                            item.invoice = invoice
                            item.save()

                        else:  # ItemAlreadyExists
                            iteminvoice.quantity += item.count
                            iteminvoice.quantity_in += item.count
                            iteminvoice.orders.add(item.order)
                            iteminvoice.save()
                            item.status_order = 1
                            item.invoice = invoice
                            item.save()

        invoices = Invoice.objects.all()
        args['invoices'] = invoices
        return render(request, "supplier/invoices.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


def del_invoice(request,id_invoice):
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    args = {}
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username

    if request.user.is_authenticated() and request.user.is_staff:
        invoice = Invoice.objects.get(pk=id_invoice)
        itemInvoice = ItemInvoice.objects.filter(invoice=id_invoice)
        itemInvoice.delete()
        invoice.delete()
        return redirect('/lk/invoices/', "supplier/invoices.html", args)
    else:
    # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)

@csrf_protect
def invoice_update(request,id_invoice):
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    args = {}
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username
    url = request.META.get('HTTP_REFERER', '/')
    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == "POST":
            i = 0
            for item in request.POST.getlist('pk'):
                iteminvoce = ItemInvoice.objects.get(invoice_id=id_invoice, pk=item)
                iteminvoce.purchase_price = Decimal(request.POST.getlist('price_in')[i])
                iteminvoce.quantity_in = int(request.POST.getlist('qty_in')[i])
                iteminvoce.save()
                i += 1
        return redirect(url, "supplier/invoice_detail.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


@csrf_protect
def invoice_order(request,id_invoice):
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    args = {}
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username

    url = request.META.get('HTTP_REFERER', '/')
    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == "POST":
            iteminvoice = ItemInvoice.objects.select_related().filter(invoice_id=id_invoice)
            for item in iteminvoice:
                #Обработка заявок
                for offer in item.offers.all():
                    itemoffer = ItemOffer.objects.get(offer_id=offer,
                                                      product=item.product,
                                                      stock=item.stock,
                                                      brand=item.brand)
                    itemoffer.status_offer = int(2)
                    itemoffer.save()
                    offeritem_count = ItemOffer.objects.filter(offer_id=offer).count()
                    offeritem_count_status = ItemOffer.objects.filter(offer_id=offer,status_offer=2).count()
                    if offeritem_count_status == offeritem_count:
                        offer_s = Offer.objects.get(pk=str(offer))
                        offer_s.status_id = int(3)
                        offer_s.save()
                # Обработка заказов с сайта
                for order in item.orders.all():
                    itemorder = OrderPosition.objects.get(order_id=order,
                                                      product=item.product,
                                                      id_stock=item.stock,
                                                      brand=item.brand)
                    itemorder.status_order = int(2)
                    itemorder.save()
                    orderitem_count = OrderPosition.objects.filter(order_id=order).count()
                    orderitem_count_status = OrderPosition.objects.filter(order_id=order,status_order=2).count()
                    if orderitem_count_status == orderitem_count:
                        order_s = Order.objects.get(pk=str(order))
                        order_s.status_id = int(3)
                        order_s.save()
            invoice = Invoice.objects.get(pk=id_invoice)
            invoice.status = int(1)
            invoice.save()
        return redirect(url, "supplier/invoice_detail.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


@csrf_protect
def invoice_accept(request,id_invoice):
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    args = {}
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username

    url = request.META.get('HTTP_REFERER', '/')
    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == "POST":
            iteminvoice = ItemInvoice.objects.select_related().filter(invoice_id=id_invoice)
            for item in iteminvoice:
                offersort = item.offers.all().order_by('created_at')
                ordersort = item.orders.all().order_by('created_at')

                count_out = item.quantity
                count_in = item.quantity_in

                # Обработка заказов
                for order in ordersort:
                    itemorder = OrderPosition.objects.get(order_id=order,
                                                          product=item.product,
                                                          id_stock=item.stock,
                                                          brand=item.brand)
                    if count_in == count_out:
                        itemorder.status_order = 3
                        itemorder.price_purchase = item.purchase_price
                        itemorder.save()

                        orderitem_count = OrderPosition.objects.filter(order_id=order).count()
                        orderitem_count_status = OrderPosition.objects.filter(order_id=order, status_order=3).count()

                        if orderitem_count_status == orderitem_count:
                            order_s = Order.objects.get(number_order=str(order))
                            order_s.status_id = int(4)
                            order_s.save()
                    else:
                        if count_out > count_in:

                            if itemorder.count <= count_in:
                                itemorder.status_order = 3
                                itemorder.price_purchase = item.purchase_price
                                itemorder.save()

                                orderitem_count = OrderPosition.objects.filter(order_id=order).count()
                                orderitem_count_status = OrderPosition.objects.filter(order_id=order,
                                                                                      status_order=3).count()
                                if orderitem_count_status == orderitem_count:
                                    order_s = Order.objects.get(number_order=str(order))
                                    order_s.status_id = int(4)
                                    order_s.save()
                                count_in -= itemorder.count
                            else:
                                if count_in != 0:
                                    itemCount_in = itemorder.count - count_in
                                    itemorder.count -= itemCount_in
                                    itemorder.save()

                                    account = Accounts.objects.get(pk=order.accounts_id)
                                    account.balance += Decimal(itemCount_in * itemorder.price_sale)
                                    account.save()
                                    balance = BalanceHistoryAccounts()
                                    balance.balance_price = Decimal(itemCount_in * itemorder.price_sale)
                                    balance.account = account
                                    balance.operations = '' \
                                                         'Возврат средств по заказу №' + str(order) + '' \
                                                                                                      ' не пришла запчасть ' + str(
                                        itemorder.product) + '' \
                                                             ' в колличестве ' + str(itemCount_in) + ' штук'

                                    balance.save()

                                    count_in = 0

                                    itemorder.status_offer = 4
                                    itemorder.price_purchase = item.purchase_price
                                    itemorder.save()
                                    order_s = Order.objects.get(number_order=str(order))
                                    order_s.status_id = int(7)
                                    order_s.save()
                                else:

                                    account = Accounts.objects.get(pk=order.accounts_id)
                                    account.balance += Decimal(itemorder.count * itemorder.price_sale)
                                    account.save()
                                    balance = BalanceHistoryAccounts()
                                    balance.balance_price = Decimal(itemorder.count * itemorder.price_sale)
                                    balance.account = account
                                    balance.operations = 'Возврат средств по заказу №' + str(order) + '' \
                                                                                                      ' не пришла запчасть ' + str(
                                        itemorder.product) + '' \
                                                             ' в колличестве ' + str(itemorder.count) + ' штук'

                                    balance.save()

                                    itemorder.status_offer = 4
                                    itemorder.price_purchase = item.purchase_price
                                    itemorder.count = 0
                                    itemorder.save()
                                    order_s = Order.objects.get(number_order=str(order))
                                    order_s.status_id = int(7)
                                    order_s.save()

              #Обработка заявок
                for offer in offersort:
                    itemoffer = ItemOffer.objects.get(offer_id=offer,
                                                      product=item.product,
                                                      stock=item.stock,
                                                      brand=item.brand)
                    if count_in == count_out:
                        itemoffer.status_offer = 3
                        itemoffer.purchase_price = item.purchase_price
                        itemoffer.save()

                        offeritem_count = ItemOffer.objects.filter(offer_id=offer).count()
                        offeritem_count_status = ItemOffer.objects.filter(offer_id=offer,status_offer=3).count()
                        if offeritem_count_status == offeritem_count:
                            offer_s = Offer.objects.get(pk=str(offer))
                            offer_s.status_id = int(4)
                            offer_s.save()
                    else:
                        if count_out > count_in:

                            if itemoffer.quantity <= count_in:
                                itemoffer.status_offer = 3
                                itemoffer.purchase_price = item.purchase_price
                                itemoffer.save()

                                offeritem_count = ItemOffer.objects.filter(offer_id=offer).count()
                                offeritem_count_status = ItemOffer.objects.filter(offer_id=offer,
                                                                                  status_offer=3).count()
                                if offeritem_count_status == offeritem_count:
                                    offer_s = Offer.objects.get(pk=str(offer))
                                    offer_s.status_id = int(4)
                                    offer_s.save()
                                count_in -= itemoffer.quantity
                            else:
                                if count_in != 0:
                                    itemCount_in = itemoffer.quantity - count_in
                                    itemoffer.quantity -= itemCount_in
                                    itemoffer.save()

                                    customer = Customer.objects.get(pk=offer.customer_id)
                                    customer.balance += Decimal(itemCount_in * itemoffer.unit_price_discount)
                                    customer.save()
                                    balance = BalanceHistory()
                                    balance.balance_price = Decimal(itemCount_in * itemoffer.unit_price_discount)
                                    balance.customer = customer
                                    balance.operations = 'Возврат средств по заказу №'+str(offer)+'' \
                                                         ' не пришла запчасть '+str(itemoffer.product)+'' \
                                                         ' в колличестве '+str(itemCount_in)+' штук'

                                    balance.save()

                                    count_in = 0

                                    itemoffer.status_offer = 4
                                    itemoffer.purchase_price = item.purchase_price
                                    itemoffer.save()
                                    offer_s = Offer.objects.get(pk=str(offer))
                                    offer_s.status_id = int(7)
                                    offer_s.save()
                                else:

                                    customer = Customer.objects.get(pk=offer.customer_id)
                                    customer.balance += Decimal(itemoffer.quantity * itemoffer.unit_price_discount)
                                    customer.save()
                                    balance = BalanceHistory()
                                    balance.balance_price = Decimal(itemoffer.quantity * itemoffer.unit_price_discount)
                                    balance.customer = customer
                                    balance.operations = 'Возврат средств по заказу №' + str(offer) + '' \
                                                         ' не пришла запчасть ' + str(itemoffer.product) + '' \
                                                         ' в колличестве ' + str(itemoffer.quantity) + ' штук'

                                    balance.save()

                                    itemoffer.status_offer = 4
                                    itemoffer.purchase_price = item.purchase_price
                                    itemoffer.quantity = 0
                                    itemoffer.save()
                                    offer_s = Offer.objects.get(pk=str(offer))
                                    offer_s.status_id = int(7)
                                    offer_s.save()



            invoice = Invoice.objects.get(pk=id_invoice)
            invoice.status = int(2)
            invoice.save()
        return redirect(url, "supplier/invoice_detail.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)