from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import xlrd
import os
import datetime
from .task import my_task

# Create your views here.


def products_import_home(request):
    if request.method == "POST":
        filename = upload_file(request.FILES)
        provider = obtain_provider(filename)
        if provider is not None:
            list_dict = read_workbook(request, filename, provider)
    else:
        print(request.method)
    return render(request, 'products/import_lists.html', {})


def upload_file(price_list_file):
    f = price_list_file['myfile']
    fs = FileSystemStorage()
    f_name = f.name.replace(' ', '')
    filename = fs.save(f_name, f)
    return filename


def obtain_provider(filename):
    if 'ARTEC' in filename:
        return 1
    elif 'MONTENEGRO' in filename:
        return 2
    else:
        return None


def parse_price(price, provider):
    if provider == 1:
        return float(price.split('$ ')[1].replace(',', '.'))
    elif provider == 2:
        return price.replace(",", '.')


def progress_view(request, row, total):
    print('2')
    result = my_task.delay(row, total)
    return render(request, 'products/snippets/display_progress.html', context={'task_id': result.task_id})


def read_workbook(request, excel_file, provider):
    workbook = xlrd.open_workbook(os.path.join(settings.MEDIA_ROOT, excel_file))
    sheet = workbook.sheet_by_index(0)
    dict_list = []
    if provider == 1:  # ARTEC
        for row_index in range(0, sheet.nrows):
            # task
            progress_view(request, row_index, sheet.nrows)
            code = sheet.cell(row_index, 0).value.encode('utf-8')
            description = sheet.cell(row_index, 1).value.encode('utf-8')
            list_price = parse_price(sheet.cell(row_index, 2).value.encode('utf-8'), provider)
            d = {"Code": code,
                 "Description": description,
                 "ProviderPrice": list_price,
                 "Provider": provider,
                 "Updated": str(datetime.datetime.today())}
            dict_list.append(d)
    elif provider == 2:  # MONTENEGRO
        for row_index in range(0, sheet.nrows):
            # task
            progress_view(request, row_index, sheet.nrows)
            if sheet.cell(row_index, 0).value.encode('utf-8') != '' and \
                    sheet.cell(row_index, 1).value.encode('utf-8') != '':
                code = sheet.cell(row_index, 0).value.encode('utf-8')
                description = sheet.cell(row_index, 1).value.encode('utf-8')
                list_price = sheet.cell(row_index, 2).value
                d = {"Code": code,
                     "Description": description,
                     "ProviderPrice": list_price,
                     "Provider": provider,
                     "Updated": str(datetime.datetime.today())}
                dict_list.append(d)
    return dict_list

