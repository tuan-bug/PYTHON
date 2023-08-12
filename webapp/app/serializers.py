from rest_framework import serializers
from .models import *

class ProductsAPI(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'price_sale', 'describe', 'digital', 'image', 'unit', 'count']


class CategoryAPI(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['sub_category', 'is_sub', 'name', 'slug', 'image']