from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import StockMovement, CycleCount, RestockRequest
from .serializers import StockMovementSerializer, CycleCountSerializer, RestockRequestSerializer
from apps.inventory.models import Inventory
from .analytics import get_sales_statistics, get_product_statistics

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.select_related('product', 'performed_by').all()
    serializer_class = StockMovementSerializer
    
    def perform_create(self, serializer):
        movement = serializer.save(performed_by=self.request.user)
        inventory, _ = Inventory.objects.get_or_create(product=movement.product)
        
        if movement.movement_type == 'in':
            inventory.quantity += movement.quantity
        elif movement.movement_type in ['out', 'adjustment']:
            inventory.quantity -= movement.quantity
        
        inventory.save()

class CycleCountViewSet(viewsets.ModelViewSet):
    queryset = CycleCount.objects.select_related('product', 'counted_by').all()
    serializer_class = CycleCountSerializer
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        cycle_count = self.get_object()
        actual_quantity = request.data.get('actual_quantity')
        
        if actual_quantity is None:
            return Response({'error': 'actual_quantity required'}, status=status.HTTP_400_BAD_REQUEST)
        
        cycle_count.actual_quantity = int(actual_quantity)
        cycle_count.status = 'completed'
        cycle_count.counted_by = request.user
        cycle_count.completed_at = timezone.now()
        cycle_count.save()
        
        return Response(self.get_serializer(cycle_count).data)

class RestockRequestViewSet(viewsets.ModelViewSet):
    queryset = RestockRequest.objects.select_related('product', 'requested_by', 'approved_by').all()
    serializer_class = RestockRequestSerializer
    
    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        restock = self.get_object()
        restock.status = 'approved'
        restock.approved_by = request.user
        restock.save()
        return Response(self.get_serializer(restock).data)


@api_view(['GET'])
def analytics_view(request):
    period = request.query_params.get('period', 'monthly')
    
    if period not in ['weekly', 'monthly', 'annual']:
        return Response({'error': 'Invalid period'}, status=status.HTTP_400_BAD_REQUEST)
    
    sales_data = get_sales_statistics(period)
    product_data = get_product_statistics(period)
    
    return Response({
        'sales': sales_data,
        'products': product_data
    })
