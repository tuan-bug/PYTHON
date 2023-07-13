from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def getHome(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        order = None
        items = []
    context = {'products': products, 'items': items, 'order': order}
    return render(request,'app/home.html', context)



def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        order = None
        items = []
    context = {'items': items, 'order': order}
    return render(request,'app/cart.html', context)



def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        order = None
        items = []
    context = {'items': items, 'order': order}
    return render(request,'app/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
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
    return JsonResponse('added',safe=False)


def register(request):
    from_register = CreateUserForm()

    context = {'from': from_register}

    # khi người dùng ấn nút đăng kí
    if request.method == 'POST':
        from_register = CreateUserForm(request.POST)
        if from_register.is_valid(): # kiểm tra đúng yêu cầu thì lưu cái form đó lại
            from_register.save()
    return render(request, "app/register.html", context)

def login(request):
    context = {}
    return render(request, "app/login.html", context)