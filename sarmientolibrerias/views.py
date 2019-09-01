from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse, reverse
from django.contrib.auth import authenticate, login, get_user_model, logout
from .forms import LoginForm
from django.utils.http import is_safe_url


def home_page(request):
    context = {
        'title': "Sarmiento Librerias",
        'content': "Welcome",
    }
    return render(request, 'home_page.html', context)


def login_page(request):
    form = LoginForm(request.POST, None)
    context = {'form': form}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            print("Error")
    return render(request, "login.html", context)


def logout_page(request):
    logout(request)
    url = reverse("login")
    return redirect(url, args=(), kwargs={})
