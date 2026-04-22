from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Inventory
from .serializers import InventorySerializer

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.select_related('product', 'product__category').all()
    serializer_class = InventorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['product__name', 'product__sku']
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        total_products = self.get_queryset().count()
        total_value = sum(inv.quantity * inv.product.unit_price for inv in self.get_queryset())
        low_stock = sum(1 for inv in self.get_queryset() if inv.product.is_low_stock)
        
        return Response({
            'total_products': total_products,
            'total_value': float(total_value),
            'low_stock_count': low_stock,
        })
