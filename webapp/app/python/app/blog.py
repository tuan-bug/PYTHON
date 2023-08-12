from django.shortcuts import render

from app.models import Order


def blog(request):
    slide_hidden = "hidden"
    fixed_height = "5px"
    user = request.user
    if user.is_staff:
        print('admin')
        show_manage = 'show'
    else:
        print('not admin')
        show_manage = 'none'
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
    context = {'show_manage': show_manage,
               'user_not_login': user_not_login,
               'user_login': user_login,
               'slide_hidden': slide_hidden,
               'fixed_height': fixed_height,
               'order': order,
               'items': items,
               }
    return render(request, 'app/blog.html', context)