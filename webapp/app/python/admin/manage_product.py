from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
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
            for image in request.FILES.getlist('images'):
                instance.image.create(image=image)
            messages.success(request, 'Product saved successfully!')
            return redirect('manageProduct')

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
            messages.success(request, 'Category updated successfully!')
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
    product_del = Product.objects.filter(id=id).delete()

    context = {'product_del': product_del}
    return redirect(request,'admin/managementProduct.html', context)

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