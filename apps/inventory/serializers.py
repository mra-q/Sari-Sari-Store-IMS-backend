from rest_framework import serializers
from .models import Inventory
from apps.products.serializers import ProductSerializer
from apps.products.models import Product

class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value
    
    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value
    
    class Meta:
        model = Inventory
        fields = '__all__'
