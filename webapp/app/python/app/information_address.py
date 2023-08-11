from django.shortcuts import render

from app.models import *


def information_address(request):
    slide_hidden = "hidden"
    fixed_height = "20px"
    address_infor = Adress.objects.filter(customer=request.user)
    if request.user.is_authenticated:
        user = request.user

    form = AddressForm()
    context = {'address_infor': address_infor,
               'fixed_height': fixed_height,
               'slide_hidden': slide_hidden,
               'form': form}
    return render(request, 'app/information_address.html', context)
