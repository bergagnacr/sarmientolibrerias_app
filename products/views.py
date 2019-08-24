from django.shortcuts import render
import xlrd

# Create your views here.


def products_import_home(request):
    if request.method == "POST":
        print("POST")
    else:
        print(request.method)
    return render(request, 'products/import_lists.html', {})

