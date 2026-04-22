from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
import logging

logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').prefetch_related('inventory').all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'sku', 'barcode']
    ordering_fields = ['name', 'created_at', 'unit_price']
    
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in ProductViewSet.list: {e}", exc_info=True)
            return Response(
                {'error': 'Failed to retrieve products', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        try:
            products = [p for p in self.get_queryset() if p.is_low_stock]
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error in low_stock: {e}", exc_info=True)
            return Response(
                {'error': 'Failed to retrieve low stock products', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def by_barcode(self, request, pk=None):
        try:
            product = Product.objects.filter(barcode=pk).first()
            if product:
                return Response(self.get_serializer(product).data)
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in by_barcode: {e}", exc_info=True)
            return Response(
                {'error': 'Failed to retrieve product', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
