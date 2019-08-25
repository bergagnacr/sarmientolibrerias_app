from django.shortcuts import render, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import xlrd
import os
import datetime

# Create your views here.


def products_import_home(request):
    if request.method == "POST":
        filename = upload_file(request.FILES)
        provider = obtain_provider(filename)
        if provider is not None:
            context, dic_list = read_workbook(request, filename, provider)
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
        return float(price.split('$ ')[1].replace(',', '.'))
    elif provider == 2:
        return float(price.replace(",", '.'))


def obtain_provider(filename):
    if 'ARTEC' in filename:
        return 1
    elif 'MONTENEGRO' in filename:
        return 2
    else:
        return None


def read_workbook(request, excel_file, provider):
    workbook = xlrd.open_workbook(os.path.join(settings.MEDIA_ROOT, excel_file))
    sheet = workbook.sheet_by_index(0)
    dict_list = return_dict_from_list(request, sheet, provider)
    return dict_list


def return_dict_from_list(request, sheet, provider):
    dict_list = []
    context = {}
    code = 0
    description = ''
    list_price = 0.00
    for row_index in range(0, sheet.nrows):
        if provider == 1:  # ARTEC
            code = sheet.cell(row_index, 0).value.encode('utf-8')
            description = sheet.cell(row_index, 1).value.encode('utf-8')
            list_price = parse_price(sheet.cell(row_index, 2).value.encode('utf-8'), provider)
        elif provider == 2:  # MONTENEGRO
            code = sheet.cell(row_index, 0).value.encode('utf-8')
            description = sheet.cell(row_index, 1).value.encode('utf-8')
            list_price = sheet.cell(row_index, 2).value
        d = {"Code": code,
             "Description": description,
             "ProviderPrice": list_price,
             "Provider": provider,
             "Updated": str(datetime.datetime.today())}
        dict_list.append(d)
        context = {'value': row_index, 'total': sheet.nrows}
        render(request, 'products/display_progress.html', context)
    return context, dict_list
