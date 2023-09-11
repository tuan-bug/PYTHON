from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from app.models import *

from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def manageCategory(request):
    categories = Category.objects.all()  # lay cac damh muc lon
    feedback = Contact.objects.all().count()
    contacts = Contact.objects.all()
    context ={'categories': categories,
              'feedback': feedback,
              'contacts': contacts,
              }
    return render(request, 'admin/managementCategory.html', context)
def addCategory(request):
    form = AddCategory()
    if request.method == 'POST':
        form = AddCategory(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category saved successfully!')
            return redirect('manageCategory')

    context = {'form': form,
               'messages': messages,
               }
    return render(request, 'admin/addCategory.html', context)

def editCategory(request):
    id = request.GET.get('id', '')  # lấy id khi người dùng vlick vào sản phẩm nào đó
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = AddCategory(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('manageCategory')
    form = AddCategory(instance=category,
                       initial={'sub_category': category.sub_category,
                                'is_sub': category.is_sub,
                                'name': category.name,
                                'slug': category.slug,
                                'image': category.image
                                })

    context = {'category': category,
               'form': form}
    return render(request, 'admin/editCategory.html', context)

def deleteCategory(request):
    id = request.GET.get('id', '')  # lấy id khi người dùng vlick vào sản phẩm nào đó
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('manageCategory')
    context ={'category': category}
    return render(request, 'admin/deleteCategory.html', context)