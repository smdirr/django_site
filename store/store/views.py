from django.contrib import messages
from users.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from products.models import Product
from django.http import HttpResponseRedirect


def index(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'index.html', {
        'message': "Listado de Productos",
        'title': "Productos",
        'products': products
    })


def login_site(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        user = request.POST.get('username')
        pwd = request.POST.get('password')

        user = authenticate(username=user, password=pwd)
        if user:
            login(request, user)
            messages.success(request, "Welcome {}".format(user.username))
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'])
            return redirect('index')
        else:
            messages.error(request, "Error: invalid user or pass")

    return render(request, 'users/login.html', {})


def logout_site(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user_created = form.save()
            if user_created:
                login(request, user_created)
                messages.success(request, 'User created successfully')
                return redirect('login')

    return render(request, 'users/register.html', {
        'form': form
    })
