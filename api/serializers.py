from rest_framework import serializers
from .models import Menu, Table, Bill, Order,CustomUser
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class BillSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)
    class Meta:
        model = Bill
        fields = ['id', 'table', 'castumer_name',"total_sum","is_paid","is_active", 'orders']