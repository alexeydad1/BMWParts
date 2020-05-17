# -*- coding: utf-8 -*-
from django.db.models import Q
from django.shortcuts import render,redirect,render_to_response,get_object_or_404
from django.template import RequestContext
from cart.Cart import Cart
#from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from catalog.models import Price,Stock,Product,ProductManufacturer
from orders.models import OrderStatus
from django.contrib import auth
from offer.models import Offer,ItemOffer,Customer,BalanceHistory,WorkOffer,Works
from offer.forms import OfferForm,Dateform
from decimal import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
from django.db.models import Sum

def custom_proc(request):
    "A context processor that provides 'app', 'user' and 'ip_address'."
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    args = {}
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username
    return args

# Create your views here.
@csrf_protect
def get_offers(request):

    args = custom_proc(request)
    if request.user.is_authenticated() and request.user.is_staff:

        if request.method == 'POST':

            form = OfferForm(request.POST)
            form.fields["status"].empty_label = u"Все" # решить проблему со статусом все
            if request.POST['status'] != 0:
                offers = Offer.objects.filter(status_id=int(request.POST['status'])).order_by('status', '-created_at')
            else:
                offers = Offer.objects.all().order_by('status', '-created_at')
        else:
            offers = Offer.objects.all().order_by('status', '-created_at')
# разобраться с пагинацией для пост запроса
#         paginator = Paginator(offers, 25)  # Show 25 contacts per page
#
#         page = request.GET.get('page')
#         try:
#             offers = paginator.page(page)
#         except PageNotAnInteger:
#             # If page is not an integer, deliver first page.
#             offers = paginator.page(1)
#         except EmptyPage:
#             # If page is out of range (e.g. 9999), deliver last page of results.
#             offers = paginator.page(paginator.num_pages)

        form = OfferForm()
        form.fields["status"].queryset = OrderStatus.objects.all()
        form.fields["status"].initial = 0
        #total_offers = 0
        # for o in offers.exclude(status_id=1):
        #     total_offers += o.price_offer()
        # args['total_offers'] = total_offers
        args['offers'] = offers
        args['form'] = form
        return render(request,"offer/offers.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


def get_customers(request):
    args = custom_proc(request)

    if request.user.is_authenticated() and request.user.is_staff:
        customers = Customer.objects.all()
        args['customers'] = customers

        return render(request, "offer/customers.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


def customer_detail(request,id_customer):
    args = custom_proc(request)

    if request.user.is_authenticated() and request.user.is_staff:
        customer = Customer.objects.get(pk=id_customer)
        offers = Offer.objects.filter(customer_id=id_customer)
        balance = BalanceHistory.objects.filter(customer_id=id_customer)
        args['customer'] = customer
        args['Offers'] = offers
        args['history_pay'] = balance

        return render(request, "offer/customer_detail.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


def offer_detail(request,id_offer):
    args = custom_proc(request)
    if request.user.is_authenticated() and request.user.is_staff:
        offer = Offer.objects.get(pk=id_offer)
        oil_link = Product.objects.filter(category_id=2)
        liquids_link = Product.objects.filter(category_id=3)
        workOffer = WorkOffer.objects.select_related().filter(offer=id_offer)
        args['oil_link'] = oil_link
        args['liquids_link'] = liquids_link
        args['offer'] = offer
        args['workOffer'] = workOffer
        form = OfferForm()


        if offer.customer != None:
            args['customer'] = offer.customer
            form.fields["customer"].initial = offer.customer.fio
        form.fields["status"].initial = offer.status.pk
        form.fields["comment"].initial = offer.comment
        form.fields["vin"].initial = offer.vin
        form.fields["phone"].initial = offer.phone
        form.fields["fio"].initial = offer.fio
        form.fields["discount"].initial = offer.discount

        args['form'] = form

        itemOffer = ItemOffer.objects.filter(offer=offer)

        args['itemOffer'] = itemOffer
        args['parts'] = request.session.get('offer',None)
        args['no_price'] = request.session.get('no_price_offer',None)
        args['parts_cross'] = request.session.get('offer_cross', None)
        args['error_request'] = request.session.get('error_request', None)
        args['error_work'] = request.session.get('error_work', None)
        args['customers'] = request.session.get('customers', None)

        if 'offer' in request.session:
            del request.session['offer']

        if 'no_price_offer' in request.session:
            del request.session['no_price_offer']

        if 'offer_cross' in request.session:
            del request.session['offer_cross']

        if 'error_request' in request.session:
            del request.session['error_request']

        if 'error_work' in request.session:
            del request.session['error_work']

        if 'customers' in request.session:
            del request.session['customers']

        request.session.save()
        return render(request, "offer/offer_detail.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


def add_to_offer(request,product_p,id_stock,id_brand,id_offer):
    url_referer = request.META.get('HTTP_REFERER', '/')
    args = custom_proc(request)

    if request.method == 'GET':
        if request.user.is_authenticated() and request.user.is_staff:
            offer = Offer.objects.get(pk=id_offer)
            offer.save()

            itemOffer = ItemOffer.objects.filter(offer=id_offer)

            product = Product.objects.filter(partnumber=product_p,producer_id=id_brand)
            brand = ProductManufacturer.objects.get(pk=id_brand)
            stock = Stock.objects.get(pk=id_stock)

            flagItem = 0
            for item in itemOffer:
                if item.product == product[0] and item.stock == stock and item.brand == brand:
                    item.quantity += 1
                    item.save()
                    flagItem=1

            if flagItem != 1:
                price = Price.objects.get(p_product=product_p,id_stock=id_stock)
                itemOffer = ItemOffer()
                itemOffer.offer = offer
                itemOffer.product = product[0]
                itemOffer.stock = stock
                itemOffer.quantity = 1
                itemOffer.purchase_price = price.purchase_price
                itemOffer.unit_price = price.our_price
                itemOffer.unit_price_discount = price.our_price
                itemOffer.brand = brand
                itemOffer.save()


######## ВАЖНО ПЕРЕПИСАТЬ ПЕРЕНАПРАВЛЕНИЕ корзина тут не к месту)))))!!!!!
            return redirect(url_referer, "offer/offer_detail.html", args)
        else:
            return redirect('/cart/', "cart/cart.html", args)

    else:
        return render(request, "cart/cart.html", args)


def offer_item_del(request,product,stock,offer,brand):
    url_referer = request.META.get('HTTP_REFERER', '/')
    cart = Cart(request)

    cartItem = cart.count()
    totalprice = cart.summary()

    args = dict(cart=Cart(request))

    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username

    if request.method == 'GET':
        if request.user.is_authenticated() and request.user.is_staff:
            args['username'] = auth.get_user(request).username
            itemOffer = ItemOffer.objects.get(
                offer_id=offer,
                # поставил заглушку от дублей вместо get
                product=Product.objects.filter(partnumber=product,producer_id=brand)[0],
                stock_id=stock,
                brand_id=brand,
            )
            itemOffer.delete()
            offerN=ItemOffer.objects.select_related().filter(offer_id=offer)
            if len(offerN)==0:
                offer_del=Offer.objects.get(pk=offer)
                offer_del.delete()
                return redirect('/lk/offers/', "offer/offers.html", args)
            else:
                args['offer'] = offerN
                return redirect('/lk/offer_detail/'+ offer +'/', "offer/offer_detail.html", args)
        else:
            # Отображение страницы с ошибкой
            args['login_errors'] = 'Войдите под своей учетной записью'
            args['username'] = auth.get_user(request).username

            return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


    else:
        return render(request, "offer/offers.html", args)


def new_offer(request):
    args = custom_proc(request)

    if request.user.is_authenticated() and request.user.is_staff:
        offer = Offer()
        offer.save()

        args['offer'] = offer
        str_offer = unicode(offer.pk)
        url = u'/lk/offer_detail/'+str_offer+u'/'
        return redirect(url, "offer/offer_detail.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


def del_customer(request,id_customer):
    args = custom_proc(request)

    if request.user.is_authenticated() and request.user.is_staff:
        customer=get_object_or_404(Customer,pk=id_customer)
        customer.delete()

        return redirect('/lk/customers/', "offer/customers.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


@csrf_protect
def table_edit(request, object_id=None, Form=None, redirect_url=None):
    if request.method == 'POST':
        if object_id is None:
            edit_form = Form(request.POST)
        else:
            edit_form = Form(request.POST, instance=Form.Meta.model.objects.get(id=object_id))
    elif object_id is None:
        edit_form = Form()
    else:
        edit_form = Form(instance=Form.Meta.model.objects.get(id=object_id))
    if edit_form.is_valid():
        edit_form.save()
        if redirect_url is not None:
            return redirect(redirect_url)
    return render(request,'offer/edit_model.html', {
        'edit_form': edit_form,
    })


def offer_print(request,id_offer,offer_p=None):
    offer = Offer.objects.get(pk=id_offer)
    offeritem = ItemOffer.objects.select_related().filter(offer=id_offer)
    workoffer = WorkOffer.objects.select_related().filter(offer=id_offer)
    args={}
    args['offeritem'] = offeritem
    args['workoffer'] = workoffer
    args['offer'] = offer
    if offer_p is not None:
        args['offer_p'] = offer_p

    return render(request, 'offer/print_offer.html', args)


def offer_print_labels(request,id_offer):
    offeritem = ItemOffer.objects.select_related().filter(offer=id_offer)
    args={}
    args['offeritem'] = offeritem
    args['offer'] = offeritem[0].offer
    return render(request, 'offer/print_labels.html', args)


def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


@csrf_protect
def search_customer(request):
    args = custom_proc(request)
    url = request.META.get('HTTP_REFERER', '/')

    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == 'POST':

            find_str = request.POST['customer']
            customers = Customer.objects.filter(Q(fio__icontains=find_str) |
                                                Q(vin__icontains=find_str) |
                                                Q(email__icontains=find_str) |
                                                Q(phone__icontains=find_str)
                                                )

            if 'customers' not in request.session:
                request.session['customers'] = list()
                for customer in customers:

                    request.session['customers'].append({
                        'pk' : customer.pk,
                        'created_at' : time.strftime(str(customer.created_at)),
                        'fio' : customer.fio,
                        'phone' : customer.phone,
                        'email' : customer.email,
                        'vin' : customer.vin,
                        'address' : customer.address,
                        'comment' : customer.comment,
                        'balance' : str(customer.balance)
                    })
                request.session.save()

            return redirect(url, "offer/offer_detail.html", args)
        else:
            return redirect(url, "offer/offer_detail.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


def customer_offer_add(request,id_customer,id_offer):
    args = custom_proc(request)

    if request.user.is_authenticated() and request.user.is_staff:
        url = request.META.get('HTTP_REFERER','/')
        offer = Offer.objects.get(pk=id_offer)
        customer = Customer.objects.get(pk=id_customer)

        offer.customer = customer
        offer.phone = customer.phone
        offer.vin = customer.vin
        offer.email = customer.email
        offer.save()
        return redirect(url, "offer/offer_detail.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


@csrf_protect
def offeritem_update(request,id_offer):
    args = custom_proc(request)

    if request.user.is_authenticated() and request.user.is_staff:
        url = request.META.get('HTTP_REFERER', '/')
        offer = Offer.objects.get(pk=id_offer)
        if request.method == "POST":

            i = 0
            for item in request.POST.getlist('pk'):
                itemOffer = ItemOffer.objects.get(offer_id=id_offer,
                                                  pk=item
                                                  )

                if request.POST.getlist('qty')[i] != '' and request.POST.getlist('qty')[i].isdigit():
                    quantity = int(request.POST.getlist('qty')[i])
                else:
                    quantity = 1

                if request.POST.getlist('unit_price') and request.POST.getlist('unit_price')[i] != '' and is_number(request.POST.getlist('unit_price')[i]):
                    unit_price = Decimal(request.POST.getlist('unit_price')[i])
                else:
                    unit_price = itemOffer.unit_price

                discount = (Decimal(100) - Decimal(offer.discount)) / 100
                itemOffer.quantity = int(quantity)
                itemOffer.unit_price_discount = unit_price * discount
                itemOffer.save()
                i += 1

        return redirect(url, "offer/offer_detail.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


@csrf_protect
def offer_save(request,id_offer):
    args = custom_proc(request)
    url = request.META.get('HTTP_REFERER', '/')

    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == "POST":

            offer = Offer.objects.select_related().get(pk=id_offer)
            old_status = offer.status_id
            old_discount = offer.discount

            offer.customer_id = request.POST['id_customer']
            offer.phone = request.POST['phone']
            offer.vin = request.POST['vin']
            offer.comment = request.POST['comment']
            offer.status_id = int(request.POST['status'])
            offer.discount = int(request.POST['discount'])
            offer.save()

            new_discount = offer.discount
            itemoffer = ItemOffer.objects.filter(offer=offer)
            if new_discount != old_discount:
                if offer.discount == 0:
                    for item in itemoffer:
                        item.unit_price_discount = item.unit_price
                        item.save()
                else:
                    discount = (Decimal(100) - Decimal(offer.discount)) / 100
                    for item in itemoffer:
                        item.unit_price_discount = item.unit_price * discount
                        item.save()
            new_status = offer.status_id
            # обработка баланса--------------------------------------------
            if old_status != new_status:
                if old_status == 1 and new_status == 2:
                    customer = Customer.objects.get(pk=int(request.POST['id_customer']))
                    customer.balance -= offer.price_offer()
                    customer.save()

                    balance = BalanceHistory()
                    balance.balance_price = offer.price_offer()
                    balance.customer = customer
                    balance.operations = 'Списание по заявке №'+str(offer.pk)
                    balance.save()

                if old_status == 2 and new_status == 1:
                    customer = Customer.objects.get(pk=int(request.POST['id_customer']))
                    customer.balance += offer.price_offer()
                    customer.save()

                    balance = BalanceHistory()
                    balance.balance_price = offer.price_offer()
                    balance.customer = customer
                    balance.operations = 'Возврат по заявке №' + str(offer.pk)
                    balance.save()
        return redirect(url, "offer/offer_detail.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


@csrf_protect
def customer_replenish_balance(request,id_customer):
    args = custom_proc(request)
    url = request.META.get('HTTP_REFERER', '/')

    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == "POST":

            customer = get_object_or_404(Customer,pk=id_customer)
            customer.balance += Decimal(request.POST['balance'])
            customer.save()
            balance = BalanceHistory()
            balance.balance_price = Decimal(request.POST['balance'])
            balance.customer = customer
            balance.operations = 'Пополнение баланса'
            balance.save()
        return redirect(url, "offer/customer_detail.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


def get_statistics(request):
    args = custom_proc(request)
    url = request.META.get('HTTP_REFERER', '/')

    if request.user.is_authenticated() and request.user.is_staff:
        form = Dateform()

        args['form'] = form
        status = OrderStatus.objects.all()
        offers =[]
        for s in status:
            offer = {}
            offer_s = Offer.objects.filter(status=s)
            if len(offer_s)>0:
                total_offers = 0
                for o in offer_s:
                    total_offers += o.price_offer()

                offer['status'] = offer_s[0].status
                offer['count'] = len(offer_s)
                offer['summ'] = total_offers

                offers.append(offer)
            else:
                offer['status'] = s
                offer['count'] = 0
                offer['summ'] = Decimal('0.00')
                offers.append(offer)

        item = ItemOffer.objects.all().values('product','product__partnumber','product__description','brand','brand__name').order_by().distinct()
        parts = []
        for p in item:
            p_dict = {}
            product_summ = ItemOffer.objects.filter(product=p.get('product'),
                                               brand=p.get('brand')).aggregate(quantity=Sum('quantity'))
            p_dict['brand'] = p.get('brand__name')
            p_dict['product'] = p.get('product__partnumber')
            p_dict['description'] = p.get('product__description')
            p_dict['quantity'] = product_summ.get('quantity')
            parts.append(p_dict)

        args['parts'] = parts
        args['offers'] = offers
        return render(request, "offer/statistics.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)

@csrf_protect
def search_works(request,id_offer):
    args = custom_proc(request)
    url = request.META.get('HTTP_REFERER', '/')

    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == 'POST':
            offer = Offer.objects.get(pk=id_offer)
            find_str = unicode(request.POST['work'])
            work = Works.objects.filter(number=find_str)
            if len(work) == 1:
                workO = WorkOffer()
                workO.offer = offer
                workO.work = work[0]
                workO.save()
            else:
                if 'error_work' not in request.session:
                    request.session['error_work'] = u'Такой работы нет!'
            return redirect(url, "offer/offer_detail.html", args)
        else:
            return redirect(url, "offer/offer_detail.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


def del_works(request,id_work):
    args = custom_proc(request)
    url = request.META.get('HTTP_REFERER', '/')

    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == 'GET':
            work_del = WorkOffer.objects.get(pk=id_work)
            work_del.delete()
            return redirect(url, "offer/offer_detail.html", args)
        else:
            return redirect(url, "offer/offer_detail.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


@csrf_protect
def offerworks_update(request,id_offer):
    args = custom_proc(request)

    if request.user.is_authenticated() and request.user.is_staff:
        url = request.META.get('HTTP_REFERER', '/')
        offer = Offer.objects.get(pk=id_offer)
        if request.method == "POST":
            if request.POST['aw_price'].replace(",", ".") != '' and is_number(request.POST['aw_price'].replace(",", ".")):
                aw_price = Decimal(request.POST['aw_price'].replace(",", "."))
                offer.aw_price = aw_price
                offer.save()
            else:
                aw_price = Decimal(0)
                offer.aw_price = aw_price
                offer.save()
            i = 0
            for item in request.POST.getlist('pk'):
                workOffer = WorkOffer.objects.get(offer_id=id_offer,
                                                  pk=item
                                                  )

                if request.POST.getlist('aw')[i] != '' and request.POST.getlist('aw')[i].isdigit():
                    aw = int(request.POST.getlist('aw')[i])
                else:
                    aw = 1
                unit_price = aw * aw_price
                workOffer.aw = aw
                workOffer.unit_price = unit_price
                workOffer.save()
                i += 1

        return redirect(url, "offer/offer_detail.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)