from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *


urlpatterns = [
    path('base/', views.base, name="base"),
    path('', views.getHome, name="home"),
    path('shop/', views.shop, name="shop"),
    path('blog/', views.blog, name="blog"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logoutPage, name="logout"),
    path('search/', views.searchProduct, name="search"),
    path('category/', views.category, name="category"),
    path('detail/', views.detail, name="detail"),
    path('address/', views.Continue1, name="address"),
    path('information/', views.Information, name="information"),
    path('contact/', views.contact, name="contact"),
    path('information_address/', views.information_address, name="information_address"),
    path('deleteAddress/', views.deleteAddress, name="deleteAddress"),
    path('addAddress/', views.addAddress, name="addAddress"),
    path('editAddress/', views.editAddress, name="editAddress"),
    path('my_order/', views.myOrder, name="myOrder"),
    path('delete_my_order/', views.deletemyOrder, name="delete_myOrder"),

    # ADMIN
    path('manage/', views.Manage, name="manage"),
    path('home_manage/', views.homeManage, name="home_manage"),
    path('manageSlide/', views.manageSlide, name="manageSlide"),
    #PRODUCTS
    path('manageProduct/', views.manageProduct, name="manageProduct"),
    path('addProduct/', views.addProduct, name="addProduct"),
    path('editProduct/', views.editProduct, name="editProduct"),
    path('deleteProduct/<int:id>', views.deleteProduct, name="deleteProduct"),
    path('viewProduct/', views.viewProduct, name="viewProduct"),

    #CATEGORY
    path('manageCategory/', views.manageCategory, name="manageCategory"),
    path('addCategory/', views.addCategory, name="addCategory"),
    path('editCategory/', views.editCategory, name="editCategory"),
    path('deleteCategory/<int:id>', views.deleteCategory, name="deleteCategory"),

    #ORDER
    path('manageUser/', views.manageUser, name="manageUser"),
    path('manageOrder/', views.manageOrder, name="manageOrder"),
    path('viewOrder/', views.viewOrder, name="viewOrder"),
    path('delOrder/', views.delOrder, name="delOrder"),

    path('abcpaypal/',views.view_money, name="viewmoney" ),
    path('paypal_ipn/',views.paypal_ipn, name="paypal_ipn" ),
    path('your_return_view/',views.your_return_view, name="your_return_view" ),
    path('your_cancel_view/',views.view_money, name="your_cancel_view" ),

    #API
    path('api/products/', CreateProductAPI.as_view(), name='create-product-api'),
    path('api/productsl/<int:pk>/', UpdateProductAPI.as_view(), name='update-product-api'),
    path('api/category/', CreateCategoryAPI.as_view(), name='create-category-ap'),
    path('api/categorysl/<int:pk>/', UpdateCategoryAPI.as_view(), name='update-category-api'),



    path('pay/', views.index, name='index'),
    path('payment/',views.payment, name='payment'),
    path('payment_ipn/', views.payment_ipn, name='payment_ipn'),
    path('payment_return/', views.payment_return, name='payment_return'),
    path('query/', views.query, name='query'),
    path('refund/', views.refund, name='refund'),
    # path('admin/', admin.site.urls),

]
