# from itertools import product

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django import forms
# Create your views here.
def base(request):
    categories = Category.objects.filter(is_sub=False)  # lay cac damh muc lon
    return render(request, 'app/base.html', categories)

def getHome(request):
    products = Product.objects.all()
    slide = Slide.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        order = None
        items = []
        user_not_login = "show"
        user_login = "hidden"

    categories = Category.objects.filter(is_sub=False)  # lay cac damh muc lon
    active_category = request.GET.get('category', '')
    context = {'products': products, 'slide': slide, 'items': items, 'order': order, 'user_login': user_login,
               'user_not_login': user_not_login, 'categories': categories, 'active_category': active_category}
    return render(request, 'app/home.html', context)


# def getSlide(request):
#     slide = Slide.objects.all()
#     return register(request, 'app/base.html', slide)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        order = None
        items = []
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub=False)  # lay cac damh muc lon
    context = {'items': items, 'order': order, 'user_login': user_login, 'user_not_login': user_not_login, 'categories':categories}
    return render(request, 'app/cart.html', context)



def checkout(request):
    categories = Category.objects.filter(is_sub=False)  # lấy các danh mục lớn
    form = AddressForm()
    if request.user.is_authenticated:
        customer = request.user
        allAddress = Adress.objects.filter(customer=customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        allAddress = None
        order = None
        items = []
        user_not_login = "show"
        user_login = "hidden"

    if allAddress is not None and allAddress.exists():
        # Ẩn form thêm địa chỉ
        form_hidden = "hidden"
        form_show = "show"
    else:
        # Hiển thị form thêm địa chỉ
        form_hidden = "show"
        form_show = "hidden"
    context = {'categories':categories , 'items': items, 'order': order, 'user_login': user_login,
               'user_not_login': user_not_login, 'form': form, 'allAddress': allAddress,
               'form_hidden': form_hidden, 'form_show': form_show}
    return render(request, 'app/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remote':
        orderItem.quantity -= 1
        
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added', safe=False)


def register(request):
    from_register = CreateUserForm()
    user_not_login = "show"
    user_login = "hidden"
    context = {'from': from_register, 'user_login': user_login, 'user_not_login': user_not_login}

    # khi người dùng ấn nút đăng kí
    if request.method == 'POST':
        from_register = CreateUserForm(request.POST)
        if from_register.is_valid(): # kiểm tra đúng yêu cầu thì lưu cái form đó lại
            from_register.save()
            return redirect('login')
    return render(request, "app/register.html", context)

def loginPage(request):
    user_not_login = "show"
    user_login = "hidden"
    if request.user.is_authenticated: # neu da xac thuc
        return redirect('home')
    if request.method == 'POST':
        userName = request.POST.get('username')
        passWord = request.POST.get('password')
        user = authenticate(request, username=userName, password=passWord)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'UserName or PassWord not ddungs')
    context = {'user_login': user_login, 'user_not_login': user_not_login}
    return render(request, "app/login.html", context)

def logoutPage(request):
    logout(request)
    return redirect('login')


def searchProduct(request):
    categories = Category.objects.filter(is_sub=False)  # lay cac damh muc lon
    if request.user.is_authenticated: # neu da xac thuc
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"

    if request.method == "POST":
        search = request.POST["searched"]
        keys = Product.objects.filter(name__contains=search)
        if request.user.is_authenticated:
            customer = request.user
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            for item in items:
                item.total = item.product.price * item.quantity
        else:
            order = None
            items = []
    return render(request, "app/search.html", {'categories': categories, 'user_login': user_login, 'user_not_login': user_not_login,"search": search, "keys": keys, 'items': items, 'order': order})

def category(request):
    # user_not_login = "hidden"
    # user_login = "show"
    categories = Category.objects.filter(is_sub=False) #lay cac damh muc lon
    active_category = request.GET.get('category', '')
    if active_category:
        products = Product.objects.filter(category__slug=active_category) # lay theo duong dan

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        order = None
        items = []
        user_not_login = "show"
        user_login = "hidden"

    context ={'items': items, 'order': order, 'categories': categories, 'products': products,
              'active_category': active_category, 'user_login': user_login, 'user_not_login': user_not_login}
    return render(request, "app/category.html", context)

def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        order = None
        items = []
        user_not_login = "show"
        user_login = "hidden"

    id = request.GET.get('id', '') # lấy id khi người dùng vlick vào sản phẩm nào đó
    user = request.user
    print(user)
    products = get_object_or_404(Product, id=id)
    comment = Comment.objects.filter(product=products) # lấy đúng cái cmt của cái sp đó
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            comments = Comment(user=user, product=products, title=content)
            comments.save()
    else:
        form = CommentForm()
    categories = Category.objects.filter(is_sub=False)  # lay cac damh muc lon
    context = {'form': form, 'comments': comment, 'products': products, 'items': items, 'order': order, 'user_login': user_login,
               'user_not_login': user_not_login, 'categories':categories}
    return render(request, 'app/detail.html', context)


def Continue1(request):
    # lấy các sản phẩm
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        user_not_login = "hidden"
        user_login = "show"
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        order = None
        items = []
        user_not_login = "show"
        user_login = "hidden"

    # lấy địa chỉ
    form = AddressForm()
    allAddress = Adress.objects.all()
    if request.user.is_authenticated:
        user = request.user
        shipping = Adress.objects.filter(customer=user)

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            mobile = form.cleaned_data['mobile']
            shipping = Adress(customer=request.user, address=address, city=city, state=state, mobile=mobile)
            shipping.save()
            messages.success(request, 'Address saved successfully!')
        else:
            messages.error(request, 'Failed to save address.')
    else:
        form = AddressForm()

    context = {'shipping': shipping, 'items': items, 'order': order, 'user_login': user_login,
               'user_not_login': user_not_login, 'allAddress': allAddress, 'messages': messages}
    return render(request, 'app/address.html', context)


def Information(request):
    if request.user.is_authenticated:
        user = request.user

    user_address = None
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            mobile = form.cleaned_data['mobile']
            user_address = Adress(customer=request.user, adress=address, city=city, state=state, mobile=mobile)
            user_address.save()
    else:
        form = AddressForm()
    context = {'user': user, 'form': form, 'user_address': user_address}
    return render(request, 'app/information.html', context)


def Manage(request):
    context ={}
    return render(request, 'admin/manage.html', context)

def manageSlide(request):
    context ={}
    return render(request, 'admin/managementSlide.html', context)


def manageProduct(request):
    context ={}
    return render(request, 'admin/managementProduct.html', context)

def manageCategory(request):
    context ={}
    return render(request, 'admin/managementCategory.html', context)
class CommentForm(forms.Form):
    # author = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

class AddressForm(forms.Form):
    address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Adress.....', 'class': 'form-control'}) )
    city = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'City.....', 'class': 'form-control'}))
    state = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'State.....', 'class': 'form-control'}))
    mobile = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Mobile.....', 'class': 'form-control'}))


class CreateUserForm(forms.Form):
        username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Username.....', 'class': 'form-control'}) )
        email = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Email.....', 'class': 'form-control'}) )
        first_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Fist name.....', 'class': 'form-control'}) )
        last_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Last name.....', 'class': 'form-control'}) )
        password1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Password.....', 'class': 'form-control'}) )
        password2 = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'placeholder': 'Confix pasword.....', 'class': 'form-control'}))

