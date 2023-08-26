import json

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required  # Đảm bảo người dùng đã đăng nhập
from app.models import *
8

@login_required
def updateItem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        productId = data.get('productId')
        action = data.get('action')

        if productId is not None and action in ['add', 'remove']:
            customer = request.user
            product = Product.objects.get(id=productId)

            cart, created = Cart.objects.get_or_create(product=product, user=customer)

            if action == 'add':
                cart.quantity += 1
            elif action == 'remove':
                cart.quantity -= 1

            if cart.quantity > 0:
                cart.save()
            else:
                cart.delete()

            return JsonResponse({'message': 'Cart updated successfully.'})
        else:
            return JsonResponse({'error': 'Invalid request data.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
