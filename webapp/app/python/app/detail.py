from django.shortcuts import get_object_or_404, render

from app.models import *


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
