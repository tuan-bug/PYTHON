from django.shortcuts import render

from app.models import *


def cart(request):
    slide_hidden = "hidden"
    fixed_height = "20px"
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
    context = {'items': items,
               'order': order,
               'user_login': user_login,
               'user_not_login': user_not_login,
               'categories':categories,
               'slide_hidden': slide_hidden,
               'fixed_height': fixed_height}
    return render(request, 'app/cart.html', context)

