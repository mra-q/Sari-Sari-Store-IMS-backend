from decimal import Decimal

from django.db.models import Count, DecimalField, ExpressionWrapper, F, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Inventory
from .serializers import InventorySerializer
from apps.products.models import Product
from apps.stock.models import StockMovement

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.select_related('product', 'product__category').all()
    serializer_class = InventorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['product__name', 'product__sku']
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        inventory_qs = self.get_queryset()
        products_qs = Product.objects.select_related('category').prefetch_related('inventory').all()

        total_products = products_qs.count()
        total_stock_units = sum(p.current_stock for p in products_qs)

        estimated_inventory_value = sum(
            Decimal(str(p.current_stock)) * p.unit_price for p in products_qs
        )

        low_stock_count = sum(1 for product in products_qs if product.is_low_stock)
        out_of_stock_count = sum(1 for product in products_qs if product.current_stock <= 0)

        today = timezone.localdate()
        stock_added_today = (
            StockMovement.objects.filter(
                created_at__date=today,
                movement_type__in=['in', 'stock_in'],
            ).aggregate(total=Coalesce(Sum('quantity'), 0))['total']
            or 0
        )

        raw_category_summary = (
            products_qs.values('category__name')
            .annotate(count=Count('id'))
            .order_by('category__name')
        )
        category_summary = [
            {
                'category': item['category__name'] or 'Uncategorized',
                'count': item['count'],
            }
            for item in raw_category_summary
        ]

        return Response({
            'totalProducts': total_products,
            'lowStockCount': low_stock_count,
            'outOfStockCount': out_of_stock_count,
            'stockAddedToday': stock_added_today,
            'totalStockUnits': total_stock_units,
            'estimatedInventoryValue': float(estimated_inventory_value),
            'categorySummary': category_summary,
        })
