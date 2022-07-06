from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView
from cart.cart import Cart
from orders.models import Order, OrderItem
from .serializers import ProductsSerializer, ProductCartSerializer, OrderSerializer
from shop.models import Product, SubCategory


class ProductsApiView(generics.ListAPIView):   # вью для представления списка объектов
    serializer_class = ProductsSerializer

    def get_queryset(self):  # возвращает набор запросов
        return Product.objects.filter(available=True)


class CatApiView(generics.ListAPIView):
    serializer_class = ProductsSerializer

    def get_queryset(self):  # возвращает набор запросов
        subcategories = SubCategory.objects.filter(category__id=self.kwargs['cat_id'])
        products = Product.objects.filter(subcategory__id__in=subcategories, available=True)
        if not products:
            raise ParseError(detail=f'Category with id {self.kwargs["cat_id"]} does not exists', code=404)

        return products


class SubCatApiView(generics.ListAPIView):
    serializer_class = ProductsSerializer

    def get_queryset(self):
        products = Product.objects.filter(subcategory__id=self.kwargs['subcat_id'],
                                          subcategory__category__id=self.kwargs['cat_id'], available=True)
        if not products:
            raise ParseError(detail=f'Subcategory with id {self.kwargs["subcat_id"]} '
                                    f'in category with id {self.kwargs["cat_id"]} does not exists', code=404)

        return products


class ProductApiView(generics.RetrieveAPIView):  # вью для представления 1 объекта
    serializer_class = ProductsSerializer

    def get_object(self):   # возвращает 1 объект
        try:
            product = Product.objects.get(pk=self.kwargs['pr_id'], subcategory__id=self.kwargs['subcat_id'])
        except ObjectDoesNotExist as e:
            raise ParseError(detail=e)

        return product


class CartApiView(APIView):   # Вью корзины

    def get(self, request):   # GET запрос
        cart = Cart(request)  # корзина из сессии
        products = list()
        for item in cart:     # для товара в корзине меняем цену из Decimal на str и объект БД,
            # т.к Json не сериализует Decimal и объекты БД
            item['price'] = str(item['price'])
            item['total_price'] = str(item['total_price'])
            item['product_id'] = item['product'].id
            item['product'] = item['product'].name
            products.append(item)

        serializer = ProductCartSerializer(data=products, many=True)    # создаем объект сериализатора
        serializer.is_valid(raise_exception=True)   # проверяем данные. если ошибка, то исключение ValidationError

        return Response({'cart': serializer.data,   # данные из объекта
                         'total_price': str(cart.get_total_price())})


class ProductAddApiView(APIView):

    def get(self, request, **kwargs):  # добавление товара в корзину
        cart = Cart(request)                # корзина из сессии
        try:
            product = Product.objects.get(pk=self.kwargs['pr_id'], subcategory__id=self.kwargs['subcat_id'])
        except ObjectDoesNotExist as e:     # ошибка, если объекта с такими id нет в БД
            raise ParseError(detail=e)      # исключение 400
        cart.add(product=product)           # добавляем продукт в корзину

        return redirect('api:cart')


class ProductDelApiView(APIView):

    def delete(self, request, **kwargs):  # удаление товара из корзины
        cart = Cart(request)                   # корзина из сессии
        try:
            product = Product.objects.get(pk=self.kwargs['pr_id'], subcategory__id=self.kwargs['subcat_id'])
        except ObjectDoesNotExist as e:
            raise ParseError(detail=e)

        cart.remove(product=product)           # удаляем продукт из корзины

        return Response({'message': f'Product {product.name} was deleted from your cart!!'})


class AddOrderToCart(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def post(self, request):
        cart = Cart(request)    # объект корзины
        data = request.data     # данные из запроса
        serializer = self.serializer_class(data=data)  # объект сериализатора
        serializer.is_valid(raise_exception=True)      # проверка на корректность данных, если нет, то исключение
        serializer.save()                              # сохраняем данные в БД
        order = Order.objects.order_by('pk').last()    # берем сохраненную запись для создания дочерней таблицы
        for item in cart:
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
        cart.clear()            # очистка корзины

        return Response({'order': serializer.data})
