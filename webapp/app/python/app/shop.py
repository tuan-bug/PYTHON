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
    product_price = {}
    for item in products:
        product_price[item.id] = '{:,.0f}'.format(item.price)

    products_sale = Product.objects.exclude(price_sale=0)

    product_sale_price = {}
    pr_sale = {}
    for item in products_sale:
        product_sale_price[item.id] = '{:,.0f}'.format(item.price_sale)
        pr_sale[item.id] = '{:,.0f}'.format(item.price)
    first_product_sale = products_sale[0]
    print(categories)

    for product in products_sale:
        product.price = float(product.price)
        product.price_sale = float(product.price_sale)
        product.sale = ((product.price - product.price_sale) / product.price) * 100

    total_all = 0
    count = 0
    if request.user.is_authenticated:
        customer = request.user
        items = Cart.objects.filter(user=customer)
        user_not_login = "none"
        user_login = "show"
        for item in items:
            print(item)
            item.total = item.product.price * item.quantity
            total_all += item.product.price * item.quantity
            count += item.quantity
    else:
        items = []
        user_not_login = "show"
        user_login = "none"

    total_all = '{:,.0f}'.format(total_all)
    context = {'categories': categories,
               'products': products,
               'product_price': product_price,
               'products_sale': products_sale,
               'pr_sale': pr_sale,
               'product_sale_price': product_sale_price,
               'first_product_sale': first_product_sale,
               'show_manage': show_manage,
               'user_not_login': user_not_login,
               'user_login': user_login,
               'slide_hidden': slide_hidden,
               'fixed_height': fixed_height,
               'items': items,
               'total_all': total_all,
               'count': count,

               }
    return render(request, 'app/shop.html', context)