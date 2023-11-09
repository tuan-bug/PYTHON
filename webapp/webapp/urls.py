"""
URL configuration for webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.conf.urls import url
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

import app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('paypal/', include("paypal.standard.ipn.urls")),

    # url(r'^$', app.views.index, name='index'),
    # url(r'^payment$', app.views.payment, name='payment'),
    # url(r'^payment_ipn$', app.views.payment_ipn, name='payment_ipn'),
    # url(r'^payment_return$', app.views.payment_return, name='payment_return'),
    # url(r'^query$', app.views.query, name='query'),
    # url(r'^refund$', app.views.refund, name='refund'),
    # url(r'^admin/', admin.site.urls),
]
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

