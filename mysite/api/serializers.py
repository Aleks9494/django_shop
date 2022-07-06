from rest_framework import serializers
from shop.models import Product
from orders.models import Order


class ProductsSerializer(serializers.ModelSerializer):
    subcategory_name = serializers.CharField(read_only=True, source="subcategory.name")

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'available', 'subcategory_name', 'subcategory_id')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        return Order.objects.create(**validated_data)


class ProductCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.CharField()
    total_price = serializers.CharField()
