from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from app.models import *
from app.python.admin.manage import is_admin
@login_required
@user_passes_test(is_admin)
def manageSlide(request):
    feedback = Contact.objects.all().count()
    contacts = Contact.objects.all()
    slides = Slide.objects.all()

    context ={'feedback': feedback,
              'contacts': contacts,
              'slides': slides,
              }
    return render(request, 'admin/managementSlide.html', context)
