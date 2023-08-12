# from itertools import product
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import *

from .python.app.base import *
from .python.app.information_address import information_address
from .python.app.cart import cart
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
from .python.admin.manage import Manage
from .python.admin.manage_slide import manageSlide
from .python.admin.manage_user import manageUser
from .python.admin.manage_category import manageCategory, addCategory, editCategory, deleteCategory
from .python.admin.manage_product import manageProduct, addProduct, editProduct, deleteProduct, viewProduct


