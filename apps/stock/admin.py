from django.contrib import admin
from .models import StockMovement, CycleCount, RestockRequest

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'movement_type', 'quantity', 'performed_by', 'created_at']
    list_filter = ['movement_type', 'created_at']

@admin.register(CycleCount)
class CycleCountAdmin(admin.ModelAdmin):
    list_display = ['product', 'expected_quantity', 'actual_quantity', 'variance', 'status', 'created_at']
    list_filter = ['status', 'created_at']

@admin.register(RestockRequest)
class RestockRequestAdmin(admin.ModelAdmin):
    list_display = ['product', 'requested_quantity', 'status', 'requested_by', 'created_at']
    list_filter = ['status', 'created_at']
