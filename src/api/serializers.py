from rest_framework.serializers import ModelSerializer

from account.models import Customer
from craft.models import Product


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ("first_name", "last_name", "email", "is_staff")


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "discount", "category", "brand", "quantity")
