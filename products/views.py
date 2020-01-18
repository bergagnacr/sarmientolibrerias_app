from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import xlrd
import os
import datetime
from .models import Product, ProductManager
from decimal import Decimal, InvalidOperation

# Create your views here.


def products_home(request):
    all_objects = Product.objects.all()
    context = {'all_objects': all_objects}
    return render(request, 'products/products_home.html', context)


def products_import_home(request):
    if request.method == "POST":
        filename = upload_file(request.FILES)
        provider = obtain_provider(filename)
        if provider is not None:
            context = read_workbook(request, filename, provider)
            return render(request, 'products/display_progress.html', context)
    else:
        return render(request, 'products/display_progress.html', {'value': 0, 'total': 100})


def upload_file(price_list_file):
    f = price_list_file['myfile']
    fs = FileSystemStorage()
    f_name = f.name.replace(' ', '')
    if fs.exists(f_name):
        os.remove(os.path.join(settings.MEDIA_ROOT, f_name))
    filename = fs.save(f_name, f)
    return filename


def parse_price(price, provider):
    if provider == 1:
        return float(str(price).split('$ ')[1].replace(',', '.').replace("'", ''))
    elif provider == 2:
        return float(price.replace(",", '.'))


def obtain_provider(filename):
    if 'ARTEC' in filename:
        return 1
    elif 'MONTENEGRO' in filename:
        return 2
    elif 'AUDITOR' in filename:
        return 3
    elif 'FREIBERG' in filename:
        return 4
    else:
        return None


def convert_code_to_string(code):
    return str(code).replace('.0', '')


def read_workbook(request, excel_file, provider):
    workbook = xlrd.open_workbook(os.path.join(settings.MEDIA_ROOT, excel_file))
    sheet = workbook.sheet_by_index(0)
    dict_list = return_dict_from_list(request, sheet, provider)
    return dict_list


def return_dict_from_list(request, sheet, provider):
    # dict_list = []
    context = {}
    code = 0
    description = ''
    list_price = 0.00
    for row_index in range(0, sheet.nrows):
        if provider == 1:  # ARTEC
            code = sheet.cell(row_index, 0).value.encode('utf-8').decode('utf-8')
            if len(code) == 0:
                break
            description = sheet.cell(row_index, 1).value.encode('utf-8').decode('utf-8')
            list_price = Decimal(parse_price(sheet.cell(row_index, 2).value.encode('utf-8'), provider))
        elif provider == 2:  # MONTENEGRO
            code = sheet.cell(row_index, 0).value.encode('utf-8').decode('utf-8')
            if len(code) == 0:
                break
            description = sheet.cell(row_index, 1).value.encode('utf-8').decode('utf-8')
            try:
                list_price = Decimal(sheet.cell(row_index, 2).value)
            except InvalidOperation:
                list_price = Decimal(0.00)
        elif provider == 3:  # AUDITOR
            # code = str(sheet.cell(row_index, 1).value).encode('utf-8').decode('utf-8')
            code = convert_code_to_string(sheet.cell(row_index, 1).value).encode('utf-8').decode('utf-8')
            if len(code) == 0:
                break
            description = sheet.cell(row_index, 2).value.encode('utf-8').decode('utf-8')
            list_price = Decimal(sheet.cell(row_index, 6).value)
        elif provider == 4:  # FREIBERG
            code = sheet.cell(row_index, 0).value.encode('utf-8').decode('utf-8')
            if len(code) == 0:
                break
            description = sheet.cell(row_index, 1).value.encode('utf-8').decode('utf-8')
            list_price = Decimal(sheet.cell(row_index, 3).value) * Decimal(1.21) * Decimal(0.9)
        product = Product(provider_code=code,
                          title=description,
                          provider=provider,
                          provider_price=list_price,
                          retailer_price=Decimal(list_price*Decimal(1.93)),
                          wholesaler_price=Decimal(list_price*Decimal(1.73)),
                          updated=str(datetime.datetime.today()))
        if Product.objects.filter(title=description, provider_code=code).exists():
            obj = Product.objects.filter(title__iexact=description, provider_code__iexact=code)
            if "%.2f" % obj.first().provider_price != "%.2f" % list_price:
                obj.update(provider_price=list_price)
        else:
            product.save()
        context = {'value': row_index, 'total': sheet.nrows}
        render(request, 'products/display_progress.html', context)
    return context
