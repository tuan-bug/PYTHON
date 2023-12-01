from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from app.models import *
from app.python.admin.manage import is_admin
@login_required
@user_passes_test(is_admin)
def manageUser(request):
    users = User.objects.all()  # lay cac damh muc lon
    feedback = Contact.objects.all().count()
    contacts = Contact.objects.all()
    # us = users.staff_status
    print('hahaha: ')

    context = {'users': users,
               'feedback': feedback,
               'contacts': contacts,
               }
    return render(request, 'admin/manageUser.html', context)

def addUser(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid(): # kiểm tra đúng yêu cầu thì lưu cái form đó lại
            form.save()
            messages.success(request, 'Thêm người dùng thành công')
            return redirect('manageUser')
        else:
            messages.error(request, 'Thêm người dùng thất bại')
    else:
        messages.error(request, 'Thêm người dùng thất bại')

    context = {'form': form,
               'messages': messages,
               }
    return render(request, 'admin/addUser.html', context)



def deleteUser(request, id):
    # id = request.GET.get('id', '')  # lấy id khi người dùng vlick vào sản phẩm nào đó
    category = get_object_or_404(User, id=id)
    User.objects.filter(id=id).delete()
    messages.success(request, 'Đã xóa người dùng')
    return redirect('manageCategory')
    context ={'category': category,
              'messages': messages,}
    return render(request, 'admin/deleteCategory.html', context)