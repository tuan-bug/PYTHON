from rest_framework import generics

from app.models import *
from app.serializers import ProductsAPI


class CreateProductAPI(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsAPI

class UpdateProductAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsAPI