from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm





class Slide(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    detail = models.TextField(null=True)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.name

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    slug = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    category = models.ManyToManyField(Category, related_name='product_category')
    price = models.FloatField()
    describe = models.CharField(max_length=300, null=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True) 
    
    def __str__(self):
        return str(self.id)
    @property
    def get_cart_item(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        # lấy hết tất cả tiền của các mặt hàng
        total = sum([item.get_total for item in orderitems])
        return total
    
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    # lấy tiền của mỗi sản phẩm
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
class ShippingAdress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(OrderItem, on_delete=models.SET_NULL, null=True, blank=True)
    adress = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.adress


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.TextField(null=True, blank=False)
    def __str__(self):
        return self.user.last_name
# Create your models here.
