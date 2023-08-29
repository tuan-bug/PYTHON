# from itertools import product
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import *


# app
from .python.app.base import *
from .python.app.information_address import information_address
from .python.app.cart import cart
from .python.app.blog import blog
from .python.app.shop import shop
from .python.app.category import category
from .python.app.check_address import Continue1
from .python.app.checkout import checkout
from .python.app.detail import detail
from .python.app.information import Information
from .python.app.login import loginPage, logoutPage
from .python.app.register import register
from .python.app.search import searchProduct
from .python.app.updateItem import updateItem
from .python.app.contact import contact
from .python.app.manage_address import addAddress, editAddress, deleteAddress


# admin
from .python.admin.manage import Manage
from .python.admin.manage_slide import manageSlide
from .python.admin.manage_user import manageUser
from .python.admin.manage_category import manageCategory, addCategory, editCategory, deleteCategory
from .python.admin.manage_product import manageProduct, addProduct, editProduct, deleteProduct, viewProduct


#API

from .API.products_api import *
from .API.category_api import *


def myOrder(request):
    check_staff = request.user
    if check_staff.is_staff:
        print('admin')
        show_manage = 'show'
    else:
        print('not admin')
        show_manage = 'none'
    slide_hidden = "hidden"
    fixed_height = "20px"
    total_all = 0
    count = 0
    if request.user.is_authenticated:
        customer = request.user
        items = Cart.objects.filter(user=customer)
        user_not_login = "none"
        user_login = "show"
        for item in items:
            item.total = item.product.price * item.quantity
            total_all += item.product.price * item.quantity
            count += item.quantity
    else:
        items = []
        user_not_login = "show"
        user_login = "none"
    categories = Category.objects.filter(is_sub=False)  # lay cac damh muc lon

    my_orders = Order.objects.filter(customer=request.user)
    order_items = {}  # Tạo một từ điển để lưu trữ các đơn hàng và mặt hàng tương ứng
    order_addresses = {}  # Tạo một từ điển để lưu trữ đơn hàng và thông tin địa chỉ tương ứng
    order_total_amounts = {}

    for order in my_orders:
        items = OrderItem.objects.filter(order=order)
        order_items[order] = items
        total_order_amount = 0
        for item in items:
            total_order_amount += item.total
            print("tong gia order : ")
            print(total_order_amount)
        order_total_amounts[order.id] = total_order_amount
        order_total_amounts_list = [(order.id, total_amount) for order.id, total_amount in order_total_amounts.items()]

        address = order.address  # Truy cập vào đối tượng Address liên kết với đơn hàng
        order_addresses[order] = address
        if order in order_total_amounts:
            print(f"Giá trị đã được lưu cho đơn hàng '{order}': {order_total_amounts[order]}")
        else:
            print(f"Không tìm thấy giá trị cho đơn hàng '{order}' trong order_total_amounts.")


    context = {
        'order_addresses': order_addresses,
        'categories': categories,
        'order_items': order_items,
        'total_all': total_all,
        'count': count,
        'user_login': user_login,
        'user_not_login': user_not_login,
        'slide_hidden': slide_hidden,
        'fixed_height': fixed_height,
        'show_manage': show_manage,
        'my_order': my_orders,
        'items': items,
        'order_total_amounts': order_total_amounts,
        'total_order_amount': total_order_amount,
        'order_total_amounts_list': order_total_amounts_list,

    }
    return render(request, 'app/my_order.html', context)


def deletemyOrder(request):
    id = request.GET.get('id', '')  # lấy id khi người dùng vlick vào sản phẩm nào đó
    order = get_object_or_404(Order, id=id)
    print(order)
    items = OrderItem.objects.filter(order=order)
    print(items)
    if request.method == 'POST':
        items.delete()
        order.delete()
        messages.success(request, 'Xóa đơn hàng thành công')
        return redirect('myOrder')
    context = {'product': order}

    return render(request, 'app/delete_my_order.html', context)


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


def manageOrder(request):

    orders = Order.objects.all()

    context = {
        'orders': orders,

    }
    return render(request, 'admin/manageOrders.html', context)