from rest_framework import serializers
from .models import StockMovement, CycleCount, RestockRequest
from apps.products.models import Product


def build_user_display_name(user):
    if not user:
        return None

    full_name = ' '.join(
        part for part in [user.first_name, user.middle_name, user.last_name] if part
    ).strip()
    return full_name or user.email

class StockMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    performed_by_name = serializers.SerializerMethodField()

    def get_performed_by_name(self, obj):
        return build_user_display_name(obj.performed_by)
    
    def validate_product(self, value):
        if not value or not Product.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value
    
    class Meta:
        model = StockMovement
        fields = '__all__'

class CycleCountSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    counted_by_name = serializers.SerializerMethodField()

    def get_counted_by_name(self, obj):
        return build_user_display_name(obj.counted_by)
    
    def validate_product(self, value):
        if not value or not Product.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value
    
    def validate_expected_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Expected quantity cannot be negative.")
        return value
    
    class Meta:
        model = CycleCount
        fields = '__all__'

class RestockRequestSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    requested_by_name = serializers.SerializerMethodField()

    def get_requested_by_name(self, obj):
        return build_user_display_name(obj.requested_by)
    
    def validate_product(self, value):
        if not value or not Product.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value
    
    def validate_requested_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Requested quantity must be greater than zero.")
        return value
    
    class Meta:
        model = RestockRequest
        fields = '__all__'
