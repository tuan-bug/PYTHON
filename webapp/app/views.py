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


    for order in my_orders:
        items = OrderItem.objects.filter(order=order)
        order_items[order] = items
        address = order.address  # Truy cập vào đối tượng Address liên kết với đơn hàng
        order_addresses[order] = address
        print(order_items[order])
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
        'my_orders': my_orders,
        'items': items,

    }
    return render(request, 'app/my_order.html', context)