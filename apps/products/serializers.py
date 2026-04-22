from rest_framework import serializers
from .models import Product, Category
import logging

logger = logging.getLogger(__name__)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    current_stock = serializers.SerializerMethodField(read_only=True)
    is_low_stock = serializers.SerializerMethodField(read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)

    def get_current_stock(self, obj):
        try:
            return obj.current_stock
        except Exception as e:
            logger.error(f"Error getting current_stock for product {obj.id}: {e}")
            return 0

    def get_is_low_stock(self, obj):
        try:
            return obj.is_low_stock
        except Exception as e:
            logger.error(f"Error getting is_low_stock for product {obj.id}: {e}")
            return False

    def get_image_url(self, obj):
        try:
            if not obj.image:
                return None

            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        except Exception as e:
            logger.error(f"Error getting image_url for product {obj.id}: {e}")
            return None
    
    class Meta:
        model = Product
        fields = '__all__'
