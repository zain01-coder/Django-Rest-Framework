from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('description','name','price','stock')

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("The price should not be 0")
        return value
    

class OrderitemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.CharField(source='product.price')
    class Meta:
        model = OrderItem
        fields = ['product_name','product_price','quantity']

class OrderSerializer(serializers.ModelSerializer):
    # order_id = serializers.UUIDField(read_only=True)
    items = OrderitemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order.item_subtotal for order in order_items)


    class Meta:
        model = Order
        fields = ['order_id','created_at','user','status','items', 'total_price']


class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()


##########################################################################
##########################################################################
##########################################################################
##########################################################################

class MyProductSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['description','name','price','stock']


class MyOrderItemSerializer(serializers.ModelSerializer):
    product = MyProductSerialzer()
    class Meta:
        model = OrderItem
        fields = ['order', 'product','quantity']


class MyOrderSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ('order_id','created_at','user','status', 'items')


