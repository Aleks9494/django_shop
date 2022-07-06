from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    # инициализация корзины
    def __init__(self, request):
        self.session = request.session  # инициальзация текущей сессии пользователя
        cart = self.session.get(settings.CART_SESSION_ID)  # из сессии пользователя берем по ключу корзину 'cart'
        if not cart:
            # если нет корзины, создаем пустую в сессии пользователя
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart  # инициальзация корзины пользователя

    # добавить продукт в корзину или обновить его количество.
    def add(self, product, quantity=1, update_quantity=False):
        # id продукта преобразуется в строку, так как Джанго использует JSON для сериализации данных сессии,
        # а JSON разрешает только имена строк
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()  # после добавления вызывается метод обновления корзины

    # Обновление сессии cart
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True  # сохраняет все изменения в корзине в сессии и помечает сессию как modified.
        # Это говорит о том, что сессия modified и должна быть сохранена.

    # Удаление товара из корзины
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()  # после удаления вызывается метод обновления корзины

    # Перебор элементов в корзине и получение продуктов из базы данных.
    def __iter__(self):
        product_ids = self.cart.keys()   # id продуктов из ключей в корзине
        products = Product.objects.filter(id__in=product_ids)  # получение продуктов в корзине из БД,
        # id должен входить в id продуктов корзины
        for product in products:
            self.cart[str(product.id)]['product'] = product  # сохранение в корзине продуктов из БД

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])    # преобразование цены обратно в число
            item['total_price'] = item['price'] * item['quantity']  # добавление в товар общей цены товара

            yield item

    # Подсчет всех товаров в корзине.
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    # Подсчет стоимости товаров в корзине.
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    # удаление корзины из сессии
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
