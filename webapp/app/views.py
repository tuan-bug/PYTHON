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
    slide = Slide.objects.all()
    categories = Category.objects.filter(is_sub=False)  # lay cac damh muc lon
    context = {
        'slide': slide,
        'categories': categories,
    }
    return render(request, 'app/base.html', context)

def getHome(request):
    products = Product.objects.all()
    slide = Slide.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        user_not_login = "none"
        user_login = "show"
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        order = None
        items = []
        user_not_login = "show"
        user_login = "none"

    categories = Category.objects.filter(is_sub=False)  # lay cac damh muc lon
    active_category = request.GET.get('category', '')
    context = {'products': products,
               'slide': slide,
               'items': items,
               'order': order,
               'user_login': user_login,
               'user_not_login': user_not_login,
               'categories': categories,
               'active_category': active_category}
    return render(request, 'app/home.html', context)


def cart(request):
    slide_hidden = "hidden"
    fixed_height = "20px"
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        user_not_login = "none"
        user_login = "show"
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        order = None
        items = []
        user_not_login = "show"
        user_login = "none"
    categories = Category.objects.filter(is_sub=False)  # lay cac damh muc lon
    context = {'items': items,
               'order': order,
               'user_login': user_login,
               'user_not_login': user_not_login,
               'categories':categories,
               'slide_hidden': slide_hidden,
               'fixed_height': fixed_height}
    return render(request, 'app/cart.html', context)



def checkout(request):
    slide_hidden = "hidden"
    fixed_height = "20px"
    categories = Category.objects.filter(is_sub=False)  # lấy các danh mục lớn
    form = AddressForm()
    if request.user.is_authenticated:
        customer = request.user
        allAddress = Adress.objects.filter(customer=customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        user_not_login = "none"
        user_login = "show"
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        allAddress = None
        order = None
        items = []
        user_not_login = "show"
        user_login = "none"

    if allAddress is not None and allAddress.exists():
        # Ẩn form thêm địa chỉ
        form_hidden = "hidden"
        form_show = "show"
    else:
        # Hiển thị form thêm địa chỉ
        form_hidden = "show"
        form_show = "hidden"
    context = {'categories':categories,
               'items': items,
               'order': order,
               'user_login': user_login,
               'user_not_login': user_not_login,
               'form': form, 'allAddress': allAddress,
               'form_hidden': form_hidden,
               'form_show': form_show,
               'slide_hidden': slide_hidden,
               'fixed_height': fixed_height,
               }
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
    slide_hidden = "hidden"
    fixed_height = "20px"
    from_register = CreateUserForm()
    user_not_login = "show"
    user_login = "none"
    context = {'from': from_register,
               'user_login': user_login,
               'user_not_login': user_not_login,
               'slide_hidden': slide_hidden,
               'fixed_height': fixed_height}

    # khi người dùng ấn nút đăng kí
    if request.method == 'POST':
        from_register = CreateUserForm(request.POST)
        if from_register.is_valid(): # kiểm tra đúng yêu cầu thì lưu cái form đó lại
            from_register.save()
            return redirect('login')
    return render(request, "app/register.html", context)

def loginPage(request):
    slide_hidden = "hidden"
    fixed_height = "20px"
    user_not_login = "show"
    user_login = "none"
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
    context = {'user_login': user_login,
               'user_not_login': user_not_login,
               'slide_hidden': slide_hidden,
               'fixed_height': fixed_height,}
    return render(request, "app/login.html", context)

def logoutPage(request):
    logout(request)
    return redirect('login')


def searchProduct(request):
    categories = Category.objects.filter(is_sub=False)  # lay cac damh muc lon
    slide_hidden = "hidden"
    fixed_height = "20px"
    if request.user.is_authenticated: # neu da xac thuc
        user_not_login = "none"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "none"

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
    return render(request, "app/search.html",
                  {'categories': categories,
                   'user_login': user_login,
                   'user_not_login': user_not_login,
                   "search": search,
                   "keys": keys,
                   'items': items,
                   'order': order,
                   'slide_hidden': slide_hidden,
                   'fixed_height': fixed_height,
                   })

def category(request):
    slide_hidden = "hidden"
    fixed_height = "20px"
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
        user_login = "none"

    context ={'items': items,
              'order': order,
              'categories': categories,
              'products': products,
              'active_category': active_category,
              'user_login': user_login,
              'user_not_login': user_not_login,
              'slide_hidden': slide_hidden,
              'fixed_height': fixed_height,
              }
    return render(request, "app/category.html", context)

def detail(request):
    slide_hidden = "hidden"
    fixed_height = "20px"
    fixed_comment = "100px"
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        user_not_login = "none"
        user_login = "show"
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        order = None
        items = []
        user_not_login = "show"
        user_login = "none"

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
    context = {'form': form,
               'comments': comment,
               'products': products,
               'items': items,
               'order': order,
               'user_login': user_login,
               'user_not_login': user_not_login,
               'categories':categories,
               'slide_hidden': slide_hidden,
               'fixed_height': fixed_height,
               'fixed_comment': fixed_comment,
               }
    return render(request, 'app/detail.html', context)


def Continue1(request):
    slide_hidden = "hidden"
    fixed_height = "20px"
    # lấy các sản phẩm
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        user_not_login = "none"
        user_login = "show"
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        order = None
        items = []
        user_not_login = "show"
        user_login = "none"

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

    context = {'shipping': shipping,
               'items': items,
               'order': order,
               'user_login': user_login,
               'user_not_login': user_not_login,
               'allAddress': allAddress,
               'messages': messages,
               'slide_hidden': slide_hidden,
               'fixed_height': fixed_height,
               }
    return render(request, 'app/address.html', context)


def Information(request):
    slide_hidden = "hidden"
    fixed_height = "20px"
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
    context = {'user': user,
               'form': form,
               'user_address': user_address,
               'slide_hidden': slide_hidden,
               'fixed_height': fixed_height,
               }
    return render(request, 'app/information.html', context)


def Manage(request):
    context ={}
    return render(request, 'admin/manage.html', context)

def manageSlide(request):
    context ={}
    return render(request, 'admin/managementSlide.html', context)


def manageProduct(request):
    products = Product.objects.all()
    form = AddCategory()
    context = {'products': products}
    return render(request, 'admin/managementProduct.html', context)

def addProduct(request):
    form = AddProduct()
    if request.method == 'POST':
        form = AddProduct(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product saved successfully!')
            return redirect('manageProduct')

    context = {'form': form,
               'messages': messages,
               }
    return render(request, 'admin/addProduct.html', context)

def contact(request):

    slide_hidden = "hidden"
    fixed_height = "20px"
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        user_not_login = "none"
        user_login = "show"
        for item in items:
            item.total = item.product.price * item.quantity
    else:
        order = None
        items = []
        user_not_login = "show"
        user_login = "none"
    categories = Category.objects.filter(is_sub=False)  # lay cac damh muc lon
    active_category = request.GET.get('category', '')

    context ={
        'categories': categories,
        'order': order,
        'items': items,
        'user_login': user_login,
        'user_not_login': user_not_login,
        'slide_hidden': slide_hidden,
        'fixed_height': fixed_height,
        }
    return render(request, 'app/contact.html', context)

def manageCategory(request):
    categories = Category.objects.all()  # lay cac damh muc lon
    context ={'categories': categories}
    return render(request, 'admin/managementCategory.html', context)
def addCategory(request):
    form = AddCategory()
    if request.method == 'POST':
        form = AddCategory(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category saved successfully!')
            return redirect('manageCategory')

    context = {'form': form,
               'messages': messages,
               }
    return render(request, 'admin/addCategory.html', context)

def editCategory(request):
    id = request.GET.get('id', '')  # lấy id khi người dùng vlick vào sản phẩm nào đó
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = AddCategory(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('manageCategory')
    form = AddCategory(instance=category, initial={'sub_category': category.sub_category, 'is_sub': category.is_sub,
                                                   'name': category.name, 'slug': category.slug, 'image': category.image})

    context = {'category': category,
               'form': form}
    return render(request, 'admin/editCategory.html', context)

def deleteCategory(request):
    id = request.GET.get('id', '')  # lấy id khi người dùng vlick vào sản phẩm nào đó
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('manageCategory')
    context ={'category': category}
    return render(request, 'admin/deleteCategory.html', context)
def test(request):
    context ={}
    return render(request, 'app/test.html', context)
class CommentForm(forms.Form):
    # author = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'height:100px', 'placeholder': 'Nhập nội dung comment.....'}))

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


