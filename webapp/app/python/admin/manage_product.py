from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

from app.models import *
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)

def manageProduct(request):
    products = Product.objects.all()
    form = AddProduct()
    feedback = Contact.objects.all().count()
    contacts = Contact.objects.all()
    context = {'products': products,
               'feedback': feedback,
               'contacts': contacts,
               }
    return render(request, 'admin/managementProduct.html', context)

def addProduct(request):
    form = AddProduct()
    if request.method == 'POST':
        form = AddProduct(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()  # Lưu thông tin model vào cơ sở dữ liệu
            print('oke luu thanh cong')
            for image in request.FILES.getlist('images'):
                instance.image.create(image=image)
            messages.success(request, 'Thêm sản phẩm thành công')
            return redirect('manageProduct')
        else:
            messages.error(request, 'Thêm sản phẩm thất bại')
    else:
        messages.error(request, 'Thêm sản phẩm thất bại')

    context = {'form': form,
               'messages': messages,
               }
    return render(request, 'admin/addProduct.html', context)


def editProduct(request):
    id = request.GET.get('id', '')  # lấy id khi người dùng vlick vào sản phẩm nào đó
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = AddProduct(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sửa sản phẩm thành công!!')
            return redirect('manageProduct')
    form = AddProduct(instance=product,
                      initial={'name': product.name,
                               'category': product.category.values_list('id', flat=True),
                               'price': product.price,
                               'describe': product.describe,
                               'image': product.image})

    context = {'product': product,
               'form': form}
    return render(request, 'admin/editProduct.html', context)

def deleteProduct(request, id):
    print('hello')
    print(id)
    print(request.method)
    if request.method == 'GET':
        print('nhảy vào thằng post')
        print(id)
        Product.objects.filter(id=id).delete()
        messages.success(request, 'Sản phẩm đã được xóa thành công.')
        return redirect(reverse('manageProduct'))
    else:
        print('không voo đc rôif')
        return render(request, 'admin/managementProduct.html')

def viewProduct(request):
    id = request.GET.get('id', '')  # lấy id khi người dùng vlick vào sản phẩm nào đó
    user = request.user
    print(user)
    product = get_object_or_404(Product, id=id)
    categories_product = product.category.values_list('id', flat=True)
    # Lấy danh sách tên danh mục từ danh sách ID
    category_names = Category.objects.filter(id__in=categories_product).values_list('name', flat=True)
    print(category_names)
    # Chuyển danh sách tên thành danh sách Python
    category_names_list = list(category_names)
    context = {'product': product,
               'category_names_list': category_names_list,
               }
    return render(request, 'admin/view_product.html', context)