from django.shortcuts import render

from app.models import *


def shop(request):
    slide_hidden = "hidden"
    fixed_height = "5px"
    user = request.user
    if user.is_staff:
        print('admin')
        show_manage = 'show'
    else:
        print('not admin')
        show_manage = 'none'
    categories = Category.objects.all()
    products = Product.objects.filter(price_sale=0)
    products_sale = Product.objects.exclude(price_sale=0)
    first_product_sale = products_sale[0]
    print(categories)

    for product in products_sale:
        product.price = float(product.price)
        product.price_sale = float(product.price_sale)
        product.sale = ((product.price - product.price_sale) / product.price) * 100

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
    context = {'categories': categories,
               'products': products,
               'products_sale': products_sale,
               'first_product_sale': first_product_sale,
               'show_manage': show_manage,
               'user_not_login': user_not_login,
               'user_login': user_login,
               'slide_hidden': slide_hidden,
               'fixed_height': fixed_height,
               'order': order,
               'items': items,

               }
    return render(request, 'app/shop.html', context)