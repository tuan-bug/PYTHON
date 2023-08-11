from django.shortcuts import render

from app.models import *


def category(request):
    slide_hidden = "hidden"
    fixed_height = "20px"
    # user_not_login = "hidden"
    # user_login = "show"
    categories = Category.objects.filter(is_sub=False) #lay cac damh muc lon
    active_category = request.GET.get('category', '')
    if active_category:
        products = Product.objects.filter(category__slug=active_category) # lay theo duong dan

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
        user_login = "none"

    context ={'items': items,
              'order': order,
              'categories': categories,
              'products': products,
              'active_category': active_category,
              'user_login': user_login,
              'user_not_login': user_not_login,
              'slide_hidden': slide_hidden,
              'fixed_height': fixed_height,
              }
    return render(request, "app/category.html", context)
