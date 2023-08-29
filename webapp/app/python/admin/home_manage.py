from django.shortcuts import render

from app.models import *
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def homeManage(request):
    orders = Order.objects.all();
    count = 0;
    for order in orders:
        if order:
            count += 1

    items = OrderItem.objects.all()

    total = 0
    for item in items:
        if item:
            total += item.total

    users = User.objects.all()
    member = 0
    for user in users:
        if user:
            member += 1
    context = {
        'count': count,
        'total': total,
        'member': member - 1,
    }
    return render(request, 'admin/home_manage.html', context)