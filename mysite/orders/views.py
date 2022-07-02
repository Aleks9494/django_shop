from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)  # получаем текущую корзину из сессии
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()  # сохраняем форму в связанную с ней таблицу
            for item in cart:    # для товаров в корзине создаем отделюную строку в таблице товары в заказе (orderitem)
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()  # очистка корзины
            return render(request, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})
