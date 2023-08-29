from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from app.models import *
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)

def manageOrder(request):

    orders = Order.objects.all()
    feedback = Contact.objects.all().count()
    contacts = Contact.objects.all()

    context = {
        'orders': orders,
        'feedback': feedback,
        'contacts': contacts,

    }
    return render(request, 'admin/manageOrders.html', context)

def viewOrder(request):
    id = request.GET.get('id', '')
    order =  get_object_or_404(Order, id=id)
    print('id order: ')
    print(id)
    order_items = {}
    total = 0
    items = OrderItem.objects.filter(order=order)
    order_items[order] = items
    total_order_amount = 0
    for item in items:
        total += item.total

    context={'order': order,
             'order_items': order_items,
             'items': items,
             'total': total,
             }
    return render(request, 'admin/view_order.html', context)

def delOrder(request):
    id = request.GET.get('id', '')  # lấy id khi người dùng vlick vào sản phẩm nào đó
    order = get_object_or_404(Order, id=id)
    print(order)
    items = OrderItem.objects.filter(order=order)
    print(items)
    if request.method == 'POST':
        items.delete()
        order.delete()
        messages.success(request, 'Xóa đơn hàng thành công')
        return redirect('manageOrder')
    context = {'product': order}

    return render(request, 'admin/delete_order.html', context)