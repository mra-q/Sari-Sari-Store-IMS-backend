from rest_framework import serializers
from .models import StockMovement, CycleCount, RestockRequest


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
    
    class Meta:
        model = StockMovement
        fields = '__all__'

class CycleCountSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    counted_by_name = serializers.SerializerMethodField()

    def get_counted_by_name(self, obj):
        return build_user_display_name(obj.counted_by)
    
    class Meta:
        model = CycleCount
        fields = '__all__'

class RestockRequestSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    requested_by_name = serializers.SerializerMethodField()

    def get_requested_by_name(self, obj):
        return build_user_display_name(obj.requested_by)
    
    class Meta:
        model = RestockRequest
        fields = '__all__'
