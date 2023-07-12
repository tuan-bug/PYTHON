from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
def getHome(request):
    products = Product.objects.all()
    context = {'products': products}
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
    context = {}
    return render(request,'app/checkout.html', context)