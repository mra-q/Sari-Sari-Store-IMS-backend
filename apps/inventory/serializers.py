from rest_framework import serializers
from .models import Inventory
from apps.products.serializers import ProductSerializer

class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Inventory
        fields = '__all__'
