from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
def getHome(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        order = None
        items = []
        user_not_login = "show"
        user_login = "hidden"
    context = {'products': products, 'items': items, 'order': order, 'user_login': user_login, 'user_not_login': user_not_login}
    return render(request, 'app/home.html', context)



def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        order = None
        items = []
        user_not_login = "show"
        user_login = "hidden"
    context = {'items': items, 'order': order, 'user_login': user_login, 'user_not_login': user_not_login}
    return render(request,'app/cart.html', context)



def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        order = None
        items = []
        user_not_login = "show"
        user_login = "hidden"
    context = {'items': items, 'order': order, 'user_login': user_login, 'user_not_login': user_not_login}
    return render(request,'app/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remote':
        orderItem.quantity -= 1
        
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added', safe=False)


def register(request):
    from_register = CreateUserForm()
    user_not_login = "show"
    user_login = "hidden"
    context = {'from': from_register, 'user_login': user_login, 'user_not_login': user_not_login}

    # khi người dùng ấn nút đăng kí
    if request.method == 'POST':
        from_register = CreateUserForm(request.POST)
        if from_register.is_valid(): # kiểm tra đúng yêu cầu thì lưu cái form đó lại
            from_register.save()
            return redirect('login')
    return render(request, "app/register.html", context)

def loginPage(request):
    user_not_login = "show"
    user_login = "hidden"
    if request.user.is_authenticated: # neu da xac thuc
        return redirect('home')
    if request.method == 'POST':
        userName = request.POST.get('username')
        passWord = request.POST.get('password')
        user = authenticate(request, username=userName, password=passWord)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'UserName or PassWord not ddungs')
    context = {'user_login': user_login, 'user_not_login': user_not_login}
    return render(request, "app/login.html", context)

def logoutPage(request):
    logout(request)
    return redirect('login')


def searchProduct(request):
    if request.method == "POST":
        search = request.POST["searched"]
        keys = Product.objects.filter(name__contains=search)
        if request.user.is_authenticated:
            customer = request.user
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            for item in items:
                item.total = item.product.price * item.quantity
        else:
            order = None
            items = []
    return render(request, "app/search.html", {"search": search, "keys": keys, 'items': items, 'order': order})