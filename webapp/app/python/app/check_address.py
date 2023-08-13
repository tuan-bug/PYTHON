from django.contrib import messages
from django.shortcuts import render

from app.models import *


def Continue1(request):

    slide_hidden = "hidden"
    fixed_height = "20px"
    check_staff = request.user
    if check_staff.is_staff:
        print('admin')
        show_manage = 'show'
    else:
        print('not admin')
        show_manage = 'none'
    # lấy các sản phẩm
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

# Xử lý chính
    id = request.GET.get('id', '')
    print("lấy id của address: " + id)
    address = Adress.objects.filter(id=id)
    address_data = address.values()
    try:
        single_address = address.get()
        # Lấy các trường cụ thể, ví dụ lấy tên người dùng và địa chỉ
        city = single_address.city
        address_sate = single_address.adress
        name = single_address.name_user
        mobile = single_address.mobile
        district = single_address.district
        commune = single_address.commune
    except Adress.DoesNotExist:
        # Xử lý trường hợp không tìm thấy bản ghi
        pass

    print(name, city, address_sate, mobile, district, commune)
    for item in items:
        print(item)
    context = {
               'items': items,
               'order': order,
               'user_login': user_login,
               'user_not_login': user_not_login,
               'messages': messages,
               'slide_hidden': slide_hidden,
               'fixed_height': fixed_height,
               'show_manage': show_manage
               }
    return render(request, 'app/address.html', context)
