from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q, F
from datetime import datetime, timedelta
from apps.products.models import Product
from apps.inventory.models import Inventory
from apps.stock.models import StockMovement


class InventoryAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        days = int(request.query_params.get('days', 30))
        cutoff_date = datetime.now() - timedelta(days=days)

        # Total inventory value
        inventory_value = Inventory.objects.select_related('product').aggregate(
            total=Sum(F('quantity') * F('product__unit_price'))
        )['total'] or 0

        # Product counts
        total_products = Product.objects.filter(is_active=True).count()
        
        low_stock_count = Inventory.objects.filter(
            product__is_active=True,
            quantity__lte=F('product__reorder_level'),
            quantity__gt=0
        ).count()
        
        out_of_stock_count = Inventory.objects.filter(
            product__is_active=True,
            quantity=0
        ).count()

        # Fast-moving items (based on stock out movements)
        fast_moving = StockMovement.objects.filter(
            movement_type='stock_out',
            created_at__gte=cutoff_date
        ).values(
            'product__id',
            'product__name'
        ).annotate(
            movement_count=Count('id'),
            total_quantity=Sum('quantity')
        ).order_by('-movement_count', '-total_quantity')[:10]

        # Slow-moving items (products with no recent movements)
        slow_moving = Product.objects.filter(
            is_active=True,
            inventory__quantity__gt=0
        ).exclude(
            movements__created_at__gte=cutoff_date
        ).values(
            'id',
            'name',
            'inventory__quantity'
        )[:10]

        # Frequent adjustments
        frequent_adjustments = StockMovement.objects.filter(
            movement_type='adjustment',
            created_at__gte=cutoff_date
        ).values(
            'product__id',
            'product__name'
        ).annotate(
            adjustment_count=Count('id'),
            total_variance=Sum('quantity')
        ).order_by('-adjustment_count')[:10]

        # Stock trends (last 7 days)
        trend_days = 7
        trend_cutoff = datetime.now() - timedelta(days=trend_days)
        
        stock_trends = StockMovement.objects.filter(
            created_at__gte=trend_cutoff
        ).extra(
            select={'date': 'DATE(created_at)'}
        ).values('date').annotate(
            stock_in=Sum('quantity', filter=Q(movement_type='stock_in')),
            stock_out=Sum('quantity', filter=Q(movement_type='stock_out'))
        ).order_by('date')

        return Response({
            'total_inventory_value': float(inventory_value),
            'total_products': total_products,
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count,
            'fast_moving_items': list(fast_moving),
            'slow_moving_items': list(slow_moving),
            'frequent_adjustments': list(frequent_adjustments),
            'stock_trends': list(stock_trends),
        })
