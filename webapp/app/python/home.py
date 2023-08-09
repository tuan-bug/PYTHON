
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django import forms

from ..models import *


def base(request):
    slide = Slide.objects.all()
    categories = Category.objects.filter(is_sub=False)  # lay cac damh muc lon
    context = {
        'slide': slide,
        'categories': categories,
    }
    return render(request, 'app/base.html', context)

def getHome(request):
    products = Product.objects.all()
    slide = Slide.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        user_not_login = "none"
        user_login = "show"
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        order = None
        items = []
        user_not_login = "show"
        user_login = "none"

    categories = Category.objects.filter(is_sub=False)  # lay cac damh muc lon
    active_category = request.GET.get('category', '')
    context = {'products': products,
               'slide': slide,
               'items': items,
               'order': order,
               'user_login': user_login,
               'user_not_login': user_not_login,
               'categories': categories,
               'active_category': active_category}
    return render(request, 'app/home.html', context)
