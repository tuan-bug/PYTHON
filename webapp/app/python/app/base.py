from django.shortcuts import render

from app.models import *


def base(request):
    user = request.user
    if user.is_staff:
        print('admin')
        show_manage = 'show'
    else:
        print('not admin')
        show_manage = 'none'
    slide = Slide.objects.all()
    test = slide.category_slide
    categories = Category.objects.filter(is_sub=False)  # lay cac damh muc lon
    context = {
        'slide': slide,
        'categories': categories,
        'show_manage': show_manage,
    }
    return render(request, 'app/base.html', context)

def getHome(request):
    user = request.user
    if user.is_staff:
        print('admin')
        show_manage = 'show'
    else:
        print('not admin')
        show_manage = 'none'
    products = Product.objects.all()
    product_price = {}
    for product in products:
        product_price[product.id] = '{:,.0f}'.format(product.price)
    # format_price =  '{:,.0f}'.format(products.)
    slide = Slide.objects.all()
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
    print('tong: ....')
    print(total_all)

    categories = Category.objects.filter(is_sub=False)  # lay cac damh muc lon
    active_category = request.GET.get('category', '')
    context = {'products': products,
               'product_price': product_price,
               'slide': slide,
               'items': items,
               'total_all': total_all,
               'count': count,
               'user_login': user_login,
               'user_not_login': user_not_login,
               'categories': categories,
               'active_category': active_category,
               'show_manage': show_manage}
    return render(request, 'app/home.html', context)


def show_manage(request):
    check_staff = request.user
    if check_staff.is_staff:
        print('admin')
        show_manage = 'show'
    else:
        print('not admin')
        show_manage = 'none'

    return show_manage