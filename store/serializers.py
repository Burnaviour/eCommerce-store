from decimal import Decimal
from rest_framework import serializers
from django.db import transaction
from store.models import Product, Collection, Review, Cart, OrderItem, CartItem, Customer, Order


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']
    product_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = ['id', 'title', 'description', 'slug', 'inventory',
                  'unit_price', 'price_with_tax', 'collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(
    #     max_digits=6, decimal_places=2, source='unit_price')
    # collection = CollectionSerializer()
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'date', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'unit_price', 'collection']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    def get_total_price(self, cartitem):
        return cartitem.product.unit_price*cartitem.quantity

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)

    def get_total_price(self, cart):
        print(cart.items.all)
        return sum(
            item.product.unit_price * item.quantity for item in cart.items.all()
        )

    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('product not found')
        return value

    def save(self, **kwargs):
        product_Id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        cart_id = self.context['cart_id']
        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_Id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'birth_date', 'phone', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']


class OrderSerializers(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'payment_status', 'customer_id', 'items']


class CreateOrderSerializers(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('cart not found')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('cart is empty')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            (customer, created) = Customer.objects.get_or_create(
                user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)
            cart_item = CartItem.objects.\
                select_related('product')\
                .filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity

                )
                for item in cart_item
            ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()
            return order


class UpdateOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']
