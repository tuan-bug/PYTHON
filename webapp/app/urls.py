from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('base/', views.base, name="base"),
    path('', views.getHome, name="home"),
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

    # phan admin
    path('manage/', views.Manage, name="manage"),
    path('manageSlide/', views.manageSlide, name="manageSlide"),

    path('manageProduct/', views.manageProduct, name="manageProduct"),
    path('addProduct/', views.addProduct, name="addProduct"),
    path('editProduct/', views.editProduct, name="editProduct"),
    path('deleteProduct/', views.deleteProduct, name="deleteProduct"),

    path('manageCategory/', views.manageCategory, name="manageCategory"),
    path('addCategory/', views.addCategory, name="addCategory"),
    path('editCategory/', views.editCategory, name="editCategory"),
    path('deleteCategory/', views.deleteCategory, name="deleteCategory"),

    path('manageUser/', views.manageUser, name="manageUser"),
]
