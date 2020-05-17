# -*- coding: utf-8 -*-
from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import auth
from lk.forms import SingupForm,FindOrderUsers
from lk.models import BalanceHistoryAccounts,Accounts
from orders.models import Order,OrderPosition,OrderStatus
from cart.Cart import Cart
from django.views.decorators.csrf import csrf_protect
import decimal
import urllib
import urllib2
import json

from django.conf import settings
from django.contrib import messages

def custom_proc(request):
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    args = {}
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username
    return args


def fDecimal(d):
    return decimal.Decimal(str(d))


@csrf_protect
def singup(request):
    cart = Cart(request)
    cartItem=cart.count()
    totalprice=cart.summary()
    
    args = {}

    args['form']=SingupForm()
    args['cartItem']=cartItem
    args['cartTotal']=totalprice
    
    if request.method == 'POST':
        newuser_form=SingupForm(request.POST)
        if newuser_form.is_valid():
	    recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            result = json.load(response)
	    if result['success']:
                newuser_form.save()
		newuser=auth.authenticate(username=newuser_form.cleaned_data['username'],password=newuser_form.cleaned_data['password2'])
		auth.login(request, newuser)
                messages.success(request, u'Вы успешно зарегистрировались')
                return redirect('/lk/')
            else:
                messages.error(request, u'Вы не правильно ввели CAPTCHA')
                args['form']= newuser_form
                args['messages'] = messages
                return render(request, 'lk/registration.html', args)
        else:
            args['form']= newuser_form
    
    return render(request, 'lk/registration.html', args)


@csrf_protect
def login(request):# периписать все как логин все!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    cart = Cart(request)
    cartItem=cart.count()
    totalprice=cart.summary()
    args = {}

    if 'login_errors' not in request.session:
       request.session['login_errors']=''
    
    if request.session['login_errors']!='':
        args['login_errors']=request.session['login_errors']
        request.session['login_errors']=''
        request.session.save()
    
    args['cartItem']=cartItem
    args['cartTotal']=totalprice
    url_referer_next=request.META.get('HTTP_REFERER','/')
    #print url_referer_next

    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None :#and user.is_active
            # Правильный пароль и пользователь "активен"
            if user.accounts.cart_id == 0:
                #print(user.accounts.cart_id)
                user.accounts.cart_id = request.session['CART-ID']
                user.accounts.save()
                #print(user.accounts.cart_id)
            else:
                request.session['CART-ID'] = user.accounts.cart_id
                request.session.save()
                cart = Cart(request)
                cartItem = cart.count()
                totalprice = cart.summary()
                args['cartItem']=cartItem
                args['cartTotal']=totalprice
                            
            auth.login(request, user)
            # Перенаправление на "правильную" страницу
            args['username']=auth.get_user(request).username
            
            return redirect('/lk/',args)
        else:
            # Отображение страницы с ошибкой
            #args['login_errors']='Пользователь не найден!'
            request.session['login_errors']='Данный пользователь не существует или указана не правильная пара Логин и Пароль!'
            request.session.save()
            return redirect('/lk/login/',args)
    else:
         if request.user.is_authenticated():
             args['username'] = auth.get_user(request).username
             cart = Cart(request)
             cartItem = cart.count()
             totalprice = cart.summary()
             args['cartItem'] = cartItem
             args['cartTotal'] = totalprice
         return render(request,"lk/login.html",args)


def logout(request):
    url_referer=request.META.get('HTTP_REFERER','/')
    #cartid=request.session['CART-ID']
    auth.logout(request)
    #request.session['CART-ID']=cartid
    #request.session.save()
    # Перенаправление на страницу.
    cart = Cart(request)
    cartItem=cart.count()
    totalprice=cart.summary()
    return redirect(url_referer,{'username':auth.get_user(request).username,'cartItem':cartItem,'cartTotal':totalprice})


def lk(request):
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    args={}
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username
    
    if request.user.is_authenticated():  
        #if user is not None and user.is_active:
            # Правильный пароль и пользователь "активен"
        balance_history = BalanceHistoryAccounts.objects.filter(account_id=request.user.id)
        args['balance_history'] = balance_history
        #auth.login(request, user)
        # Перенаправление на "правильную" страницу
        return render(request,"lk/lk.html",args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors']='Пользователь не найден!'
        args['username']=auth.get_user(request).username
       
        
        return redirect('%s?next=%s' % ('/lk/login/', request.path),args)


@csrf_protect
def lk_orders(request):
    cart = Cart(request)
    cartItem=cart.count()
    totalprice=cart.summary()
    args={}
    args['cartItem']=cartItem
    args['cartTotal']=totalprice
    args['username']=auth.get_user(request).username
    
    if request.user.is_authenticated():  
        #if user is not None and user.is_active:
            # Правильный пароль и пользователь "активен"
        if request.method == 'POST':
            if request.user.is_staff:
                status = request.POST.getlist('status')
                find_str = request.POST['find']
                if find_str != '':
                    orders = Order.objects.filter(Q(number_order__icontains=find_str) |
                                                  Q(accounts__telephone__icontains=find_str) |
                                                  Q(status__in=status) |
                                                  Q(accounts__first_name__icontains=find_str) |
                                                  Q(accounts__last_name__icontains=find_str))
                else:
                    orders = Order.objects.filter(Q(status_id__in=status))

                if request.user.is_staff:
                    form = FindOrderUsers()
                    form.fields['status'].choices = [(x.pk, x) for x in OrderStatus.objects.all()]
                    args['find_form'] = form

                order_status = OrderStatus.objects.all()
                orderStatus = []

                for os in order_status:
                    order = orders.filter(status=os)
                    orderStatus.append([os, order])
                if orders:
                    totalOrders = fDecimal('0.00')
                    countOrders = 0
                    for o in orders:
                        totalOrders += o.price()
                        countOrders += 1
                    args['countOrders'] = countOrders
                    args['totalOrders'] = totalOrders
                else:
                    args['countOrders'] = 0
                    args['totalOrders'] = 0
                args['orders'] = orders
                args['orderStatus'] = orderStatus
                return render(request, "lk/lk_orders.html", args)
            else:
                return render(request, "lk/lk_orders.html", args)
        else:
            if request.user.is_staff:
                form = FindOrderUsers()
                form.fields['status'].choices = [(x.pk, x) for x in OrderStatus.objects.all()]
                args['find_form'] = form
                orders = Order.objects.all()
            else:
                orders = Order.objects.filter(accounts=request.user.id)
            order_status = OrderStatus.objects.all()
            orderStatus = []
            for os in order_status:
                order = orders.filter(status=os)
                orderStatus.append([os , order])
            if orders:
                totalOrders = fDecimal('0.00')
                countOrders = 0
                for o in orders:
                    totalOrders += o.price()
                    countOrders += 1
                args['countOrders'] = countOrders
                args['totalOrders'] = totalOrders
            else:
                args['countOrders'] = 0
                args['totalOrders'] = 0
            args['orders'] = orders
            args['orderStatus'] = orderStatus
            #auth.login(request, user)
            # Перенаправление на "правильную" страницу
            return render(request,"lk/lk_orders.html",args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors']='Пользователь не найден!'
        args['username']=auth.get_user(request).username
       
        
        return redirect('%s?next=%s' % ('/lk/login/', request.path),args)


@csrf_protect
def lk_order(request,id=1):
    cart = Cart(request)
    cartItem=cart.count()
    totalprice=cart.summary()
    args={}
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username
    
    if request.user.is_authenticated():  
        #if user is not None and user.is_active:
            # Правильный пароль и пользователь "активен"
        if request.method == 'POST':
            order = Order.objects.get(pk=id)
            order.status_id = int(request.POST['status'])
            order.save()

        itemorder = OrderPosition.objects.select_related().filter(order=id)
        order = Order.objects.get(pk=id)
        if request.user.is_staff:
            status = OrderStatus.objects.all()
            args['status'] = status
        args['numOrder'] = id
        args['statusO'] = itemorder[0].order.status
        args['order'] = itemorder
        args['orderPrice'] = order
        #auth.login(request, user)
        # Перенаправление на "правильную" страницу
        return render(request,"lk/order_detail.html",args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username
       
        
        return redirect('%s?next=%s' % ('/lk/login/', request.path),args)


@csrf_protect
def get_users(request):
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    args = {}
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username

    if request.user.is_authenticated():
        # if user is not None and user.is_active:
        # Правильный пароль и пользователь "активен"
        # if request.method == 'POST':
        #     if request.user.is_staff:
        #         find_str = ''
        #         if find_str != '':
        #             orders = Order.objects.filter(Q(number_order__icontains=find_str) |
        #                                           Q(accounts__telephone__icontains=find_str) |
        #                                           Q(accounts__first_name__icontains=find_str) |
        #                                           Q(accounts__last_name__icontains=find_str))
        #         if request.user.is_staff:
        #             form = FindOrderUsers()
        #             form.fields['status'].choices = [(x.pk, x) for x in OrderStatus.objects.all()]
        #             args['find_form'] = form
        #
        #         return render(request, "lk/lk_users.html", args)
        #     else:
        #         return render(request, "lk/lk_users.html", args)
        # else:
        if request.user.is_staff:
            accounts = Accounts.objects.all()
            args['accounts'] = accounts
        return render(request, "lk/lk_users.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


@csrf_protect
def user_detail(request,username):
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    args = {}
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username

    if request.user.is_authenticated():
        # if user is not None and user.is_active:
        # Правильный пароль и пользователь "активен"
        # if request.method == 'POST':
        #     if request.user.is_staff:
        #         find_str = ''
        #         if find_str != '':
        #             orders = Order.objects.filter(Q(number_order__icontains=find_str) |
        #                                           Q(accounts__telephone__icontains=find_str) |
        #                                           Q(accounts__first_name__icontains=find_str) |
        #                                           Q(accounts__last_name__icontains=find_str))
        #         if request.user.is_staff:
        #             form = FindOrderUsers()
        #             form.fields['status'].choices = [(x.pk, x) for x in OrderStatus.objects.all()]
        #             args['find_form'] = form
        #
        #         return render(request, "lk/lk_users.html", args)
        #     else:
        #         return render(request, "lk/lk_users.html", args)
        # else:
        if request.user.is_staff:
            account = Accounts.objects.get(pk=username)
            orders = Order.objects.filter(accounts=account)
            history_pay = BalanceHistoryAccounts.objects.filter(account=username)
            args['account'] = account
            args['orders'] = orders
            args['history_pay'] = history_pay
        return render(request, "lk/user_detail.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


@csrf_protect
def account_replenish_balance(request,id_account):
    args = custom_proc(request)
    url = request.META.get('HTTP_REFERER', '/')

    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == "POST":

            account = get_object_or_404(Accounts,pk=id_account)
            account.balance += decimal.Decimal(request.POST['balance'])
            account.save()
            balance = BalanceHistoryAccounts()
            balance.balance_price = decimal.Decimal(request.POST['balance'])
            balance.account = account
            balance.operations = 'Пополнение баланса'
            balance.save()
        return redirect(url, "lk/user_detail.html", args)
    else:
        # Отображение страницы с ошибкой
        args['login_errors'] = 'Пользователь не найден!'
        args['username'] = auth.get_user(request).username

        return redirect('%s?next=%s' % ('/lk/login/', request.path), args)