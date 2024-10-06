from rest_framework import serializers
from .models import VideoGame, Cart, CartItem, Order, OrderItem
from django.contrib.auth import get_user_model
from .models import CustomUser

# Serializer for VideoGame
class VideoGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoGame
        fields = '__all__'

# Serializer for Cart and Cart Items


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'videoGame', 'quantity']  # Assurez-vous que 'quantity' est inclus

    def validate_quantity(self, value):
        # Vérifiez que la quantité est supérieure à zéro
        if value is None or value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

# Serializer for Orders and Order Items
class OrderItemSerializer(serializers.ModelSerializer):
    game = VideoGameSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'address', 'phone_number', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])  # Chiffrement du mot de passe
        user.save()
        return user