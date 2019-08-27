from django.shortcuts import render


def home_page(request):
    context = {
        'title': "Sarmiento Librerias",
        'content': "Welcome",
    }
    return render(request, 'home_page.html', context)
