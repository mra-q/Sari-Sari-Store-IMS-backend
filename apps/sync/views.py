from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils.dateparse import parse_datetime
from datetime import datetime
import logging
from .serializers import SyncRequestSerializer
from apps.products.models import Product
from apps.inventory.models import Inventory
from apps.stock.models import StockMovement, CycleCount, RestockRequest

logger = logging.getLogger(__name__)


class SyncView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        try:
            serializer = SyncRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            creates = serializer.validated_data.get('creates', [])
            updates = serializer.validated_data.get('updates', [])
            deletes = serializer.validated_data.get('deletes', [])

            created_count = 0
            updated_count = 0
            deleted_count = 0
            errors = []

            # Process creates
            for item in creates:
                entity_type = item.get('type')
                data = item.get('data')
                
                try:
                    if entity_type == 'product':
                        Product.objects.update_or_create(
                            id=data['id'],
                            defaults={
                                'name': data['name'],
                                'description': data.get('description', ''),
                                'barcode': data.get('barcode'),
                                'category': data.get('category'),
                                'unit': data.get('unit', ''),
                                'reorder_level': data.get('reorder_level', 0),
                                'price': data.get('price', 0),
                                'updated_at': parse_datetime(data.get('updated_at')) or datetime.now()
                            }
                        )
                        created_count += 1
                    elif entity_type == 'inventory':
                        Inventory.objects.update_or_create(
                            id=data['id'],
                            defaults={
                                'product_id': data['product_id'],
                                'quantity': data['quantity'],
                                'location': data.get('location', ''),
                                'updated_at': parse_datetime(data.get('updated_at')) or datetime.now()
                            }
                        )
                        created_count += 1
                    elif entity_type == 'stock_movement':
                        StockMovement.objects.get_or_create(
                            id=data['id'],
                            defaults={
                                'product_id': data['product_id'],
                                'movement_type': data['movement_type'],
                                'quantity': data['quantity'],
                                'reason': data.get('reason', ''),
                                'notes': data.get('notes', ''),
                                'performed_by_id': request.user.id,
                                'created_at': parse_datetime(data.get('created_at')) or datetime.now(),
                                'updated_at': parse_datetime(data.get('updated_at')) or datetime.now()
                            }
                        )
                        created_count += 1
                    elif entity_type == 'cycle_count':
                        CycleCount.objects.get_or_create(
                            id=data['id'],
                            defaults={
                                'product_id': data['product_id'],
                                'expected_quantity': data['expected_quantity'],
                                'actual_quantity': data['actual_quantity'],
                                'variance': data['variance'],
                                'counted_by_id': request.user.id,
                                'created_at': parse_datetime(data.get('created_at')) or datetime.now(),
                                'updated_at': parse_datetime(data.get('updated_at')) or datetime.now()
                            }
                        )
                        created_count += 1
                    elif entity_type == 'restock_request':
                        RestockRequest.objects.get_or_create(
                            id=data['id'],
                            defaults={
                                'product_id': data['product_id'],
                                'requested_quantity': data['requested_quantity'],
                                'status': data.get('status', 'pending'),
                                'notes': data.get('notes', ''),
                                'requested_by_id': request.user.id,
                                'created_at': parse_datetime(data.get('created_at')) or datetime.now(),
                                'updated_at': parse_datetime(data.get('updated_at')) or datetime.now()
                            }
                        )
                        created_count += 1
                except Exception as e:
                    error_msg = f"Error creating {entity_type}: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)

            # Process updates (with conflict resolution)
            for item in updates:
                entity_type = item.get('type')
                data = item.get('data')
                
                try:
                    if entity_type == 'product':
                        obj = Product.objects.filter(id=data['id']).first()
                        if obj:
                            client_updated = parse_datetime(data.get('updated_at'))
                            if client_updated and client_updated > obj.updated_at:
                                for key, value in data.items():
                                    if key not in ['id', 'created_at']:
                                        setattr(obj, key, value)
                                obj.save()
                                updated_count += 1
                    elif entity_type == 'inventory':
                        obj = Inventory.objects.filter(id=data['id']).first()
                        if obj:
                            client_updated = parse_datetime(data.get('updated_at'))
                            if client_updated and client_updated > obj.updated_at:
                                for key, value in data.items():
                                    if key not in ['id', 'created_at']:
                                        setattr(obj, key, value)
                                obj.save()
                                updated_count += 1
                    elif entity_type == 'restock_request':
                        obj = RestockRequest.objects.filter(id=data['id']).first()
                        if obj:
                            client_updated = parse_datetime(data.get('updated_at'))
                            if client_updated and client_updated > obj.updated_at:
                                for key, value in data.items():
                                    if key not in ['id', 'created_at']:
                                        setattr(obj, key, value)
                                obj.save()
                                updated_count += 1
                except Exception as e:
                    error_msg = f"Error updating {entity_type}: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)

            # Process deletes
            for item in deletes:
                entity_type = item.get('type')
                entity_id = item.get('id')
                
                try:
                    if entity_type == 'product':
                        Product.objects.filter(id=entity_id).delete()
                        deleted_count += 1
                    elif entity_type == 'inventory':
                        Inventory.objects.filter(id=entity_id).delete()
                        deleted_count += 1
                except Exception as e:
                    error_msg = f"Error deleting {entity_type}: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)

            response_data = {
                'success': True,
                'message': 'Sync completed',
                'created_count': created_count,
                'updated_count': updated_count,
                'deleted_count': deleted_count
            }
            
            if errors:
                response_data['errors'] = errors
                response_data['message'] = 'Sync completed with errors'
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Sync failed: {str(e)}", exc_info=True)
            return Response({
                'success': False,
                'message': 'Sync failed',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SyncPullView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get timestamp filter if provided
            since = request.query_params.get('since')
            
            # Build queries
            products_qs = Product.objects.all()
            inventory_qs = Inventory.objects.all()
            stock_movements_qs = StockMovement.objects.all()
            cycle_counts_qs = CycleCount.objects.all()
            restock_requests_qs = RestockRequest.objects.all()
            
            if since:
                try:
                    since_dt = parse_datetime(since)
                    if since_dt:
                        products_qs = products_qs.filter(updated_at__gte=since_dt)
                        inventory_qs = inventory_qs.filter(last_updated__gte=since_dt)
                        stock_movements_qs = stock_movements_qs.filter(updated_at__gte=since_dt)
                        cycle_counts_qs = cycle_counts_qs.filter(updated_at__gte=since_dt)
                        restock_requests_qs = restock_requests_qs.filter(updated_at__gte=since_dt)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Invalid since parameter: {since}, error: {e}")

            return Response({
                'products': list(products_qs.values()),
                'inventory': list(inventory_qs.values()),
                'stock_movements': list(stock_movements_qs.values()),
                'cycle_counts': list(cycle_counts_qs.values()),
                'restock_requests': list(restock_requests_qs.values()),
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Sync pull failed: {str(e)}", exc_info=True)
            return Response({
                'error': 'Failed to pull sync data',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
