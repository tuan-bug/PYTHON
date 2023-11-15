from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
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
