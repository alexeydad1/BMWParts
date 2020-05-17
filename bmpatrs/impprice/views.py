# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,HttpResponse
from catalog.models import Stock,Price
from impprice.models import FilePrice
from impprice.forms import UploadFilePrice,UploadFileCSV
from django.views.decorators.csrf import csrf_protect
from django.core.files.uploadedfile import SimpleUploadedFile,UploadedFile
from django.db import transaction
# Create your views here.
import csv
import time
import re
import openpyxl
import os
import codecs
from django.conf import settings
import mimetypes


@csrf_protect
def import_csv3(request):
    patch_dir = '/home/host1409570/bmwminiparts.ru/htdocs/www/media/'
    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == 'POST':
            form = UploadFilePrice(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES['import_filenames'],patch_dir)
            filen = unicode(patch_dir+request.FILES['import_filenames'].name)

            Price.objects.filter(id_stock=form.cleaned_data['stock']).delete()
            with open(filen) as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                stock=Stock.objects.get(id=form.cleaned_data['stock'].pk)
                i_price = []  # список обновленных бъектов
                not_save = []  # список не найденных объектов
                localtime = time.asctime(time.localtime(time.time()))
                bulk = []
                print localtime
                for row in reader:  # пербор строк из файла импорта
                    reg = re.compile('[^a-zA-Z0-9]')
                    p = reg.sub('', row[0])

                    if len(row) == 5:
                        dealer_price = row[4].replace(',', '.')
                    else:
                        dealer_price = 0

                    price = Price(
                        p_product=p,
                        id_stock=stock,
                        qty=row[1].replace(',', '.'),
                        purchase_price=row[2].replace(',', '.'),
                        our_price=row[3].replace(',', '.'),
                        dealer_price=dealer_price

                    )
                    bulk.append(price)
            localtime2 = time.asctime(time.localtime(time.time()))
            print localtime2
            Price.objects.bulk_create(bulk,batch_size=1000)
            localtime3 = time.asctime(time.localtime(time.time()))
            print localtime3
                    #price = Price()
                    # price.p_product = p
                    # price.id_stock = stock
                    # price.qty = row[1]
                    # price.purchase_price = row[2].replace(',','.')
                    # price.our_price = row[3].replace(',','.')
                    # if len(row) == 5:
                    #     price.dealer_price = row[4].replace(',', '.')
                    # else:
                    #     price.dealer_price = 0
                    #

                    # try:
                    #     price.save()
                    #     i_price.append(row)
                    # except Exception:
                    #     not_save.append([p,row[1],row[2].replace(',','.'),row[3].replace(',','.')])


            file_price = FilePrice()
            file_price.import_filenames = request.FILES['import_filenames'].name
            file_price.stock = stock
            file_price.save()

            file_prices = FilePrice.objects.all()

            form_csv = UploadFileCSV()
            return render(request, 'catalog/importprice.html', {'price': i_price,
                                                                'not_product': not_save,
                                                                'form': form,
                                                                'time1' : localtime,
                                                                'time2' : localtime2,
                                                                'file_price': file_prices,
                                                                'form_csv': form_csv})
        else:
            file_prices = FilePrice.objects.all()
            form = UploadFilePrice()
            form_csv = UploadFileCSV()

        return render(request, 'catalog/importprice.html', {'form': form,'file_price' : file_prices,'form_csv': form_csv})
    else:
        # Отображение страницы с ошибкой
        return redirect('%s?next=%s' % ('/lk/login/', request.path))


def handle_uploaded_file(f,patch_dir):
    file=unicode(f.name)
    full_patch = patch_dir + file
    # print full_patch
    destination = open(full_patch, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


@csrf_protect
def make_csv(request):

    patch_dir = '/home/host1409570/bmwminiparts.ru/htdocs/www/media/'
    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == 'POST':
            form_csv = UploadFileCSV(request.POST, request.FILES)
            if form_csv.is_valid():
                cell_number = form_csv.cleaned_data['number']
                cell_qty = form_csv.cleaned_data['qty']
                cell_price = form_csv.cleaned_data['price']
                cell_price_dealer = form_csv.cleaned_data['price_dealer']
                margin = form_csv.cleaned_data['margin']
                round_price = form_csv.cleaned_data['round_price']

                handle_uploaded_file(request.FILES['file'], patch_dir)
                filen = unicode(patch_dir + request.FILES['file'].name)

                wb = openpyxl.load_workbook(filename=filen,read_only=True)

                stop_iter = 0
                ws = wb.active
                f_csv = translit(unicode(filen+'.csv'))
                with open(f_csv, 'wb') as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    for row in ws.rows:
                        list_values = []
                        for cell in row:
                           list_values.append(unicode(cell.value).encode('cp1251'))
                           if list_values[0] == 'None':
                                stop_iter = 1
                                break
                        if stop_iter == 1:
                            break

                        d_price = cell_price_dealer - 1
                        reg = re.compile('[^a-zA-Z0-9.,]')
                        qty = reg.sub('', list_values[cell_qty-1])
                        if qty != '0' and qty and '.' not in qty and ',' not in qty:
                            #print list_values
                            m = float(margin)/100
                            row = []
                            row.append(list_values[cell_number - 1])
                            row.append(qty)
                            row.append(list_values[cell_price - 1])
                            row.append(round_f(float(list_values[cell_price - 1])+(float(list_values[cell_price - 1]) * float(m)),round_price))

                            if d_price != -1:
                                row.append(list_values[d_price])

                            writer.writerow(row)
                            #print '------------------------'
                link = translit(request.FILES['file'].name + '.csv')
                file_prices = FilePrice.objects.all()
                form = UploadFilePrice()
                form_csv = UploadFileCSV(request.POST)

                return render(request, 'catalog/importprice.html',{'form': form,'form_csv': form_csv, 'file_price': file_prices,'link': link , 'form_csv': form_csv})
            else:
                return render(request, 'catalog/importprice.html')
        else:

            file_prices = FilePrice.objects.all()
            form = UploadFilePrice()
            form_csv = UploadFileCSV()

            return render(request, 'catalog/importprice.html',
                      {'form': form, 'file_price': file_prices, 'form_csv': form_csv})
    else:
        return redirect('%s?next=%s' % ('/lk/login/', request.path))

def round_f(x,round_price):
    return int(round(x/float(round_price))*round_price)


def download_csv(request, name):
    file_path = '/home/host1409570/bmwminiparts.ru/htdocs/www/media/'+unicode(name)

    fp = open(file_path, "rb")
    response = HttpResponse(fp.read())
    fp.close()

    # file_type = mimetypes.guess_type(file_path)
    # if file_type is None:
    #     file_type = 'application/octet-stream'
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Length'] = str(os.stat(file_path).st_size)
    response['Content-Disposition'] = "attachment; filename=%s" % os.path.basename(fp.name)
    os.remove(file_path)
    return response


def translit(locallangstring):
    conversion = {
    u'\u0410' : 'A', u'\u0430' : 'a',
    u'\u0411' : 'B', u'\u0431' : 'b',
    u'\u0412' : 'V', u'\u0432' : 'v',
    u'\u0413' : 'G', u'\u0433' : 'g',
    u'\u0414' : 'D', u'\u0434' : 'd',
    u'\u0415' : 'E', u'\u0435' : 'e',
    u'\u0401' : 'Yo', u'\u0451' : 'yo',
    u'\u0416' : 'Zh', u'\u0436' : 'zh',
    u'\u0417' : 'Z', u'\u0437' : 'z',
    u'\u0418' : 'I', u'\u0438' : 'i',
    u'\u0419' : 'Y', u'\u0439' : 'y',
    u'\u041a' : 'K', u'\u043a' : 'k',
    u'\u041b' : 'L', u'\u043b' : 'l',
    u'\u041c' : 'M', u'\u043c' : 'm',
    u'\u041d' : 'N', u'\u043d' : 'n',
    u'\u041e' : 'O', u'\u043e' : 'o',
    u'\u041f' : 'P', u'\u043f' : 'p',
    u'\u0420' : 'R', u'\u0440' : 'r',
    u'\u0421' : 'S', u'\u0441' : 's',
    u'\u0422' : 'T', u'\u0442' : 't',
    u'\u0423' : 'U', u'\u0443' : 'u',
    u'\u0424' : 'F', u'\u0444' : 'f',
    u'\u0425' : 'H', u'\u0445' : 'h',
    u'\u0426' : 'Ts', u'\u0446' : 'ts',
    u'\u0427' : 'Ch', u'\u0447' : 'ch',
    u'\u0428' : 'Sh', u'\u0448' : 'sh',
    u'\u0429' : 'Sch', u'\u0449' : 'sch',
    u'\u042a' : '"', u'\u044a' : '"',
    u'\u042b' : 'Y', u'\u044b' : 'y',
    u'\u042c' : '\'', u'\u044c' : '\'',
    u'\u042d' : 'E', u'\u044d' : 'e',
    u'\u042e' : 'Yu', u'\u044e' : 'yu',
    u'\u042f' : 'Ya', u'\u044f' : 'ya',
    }
    translitstring = []
    for c in locallangstring:
        translitstring.append(conversion.setdefault(c, c))
    return ''.join(translitstring)