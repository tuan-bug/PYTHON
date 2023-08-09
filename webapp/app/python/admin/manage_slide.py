from django.shortcuts import render


def manageSlide(request):
    context ={}
    return render(request, 'admin/managementSlide.html', context)
