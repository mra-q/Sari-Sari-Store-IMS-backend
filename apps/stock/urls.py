from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockMovementViewSet, CycleCountViewSet, RestockRequestViewSet, stock_insights_view

router = DefaultRouter()
router.register('movements', StockMovementViewSet, basename='movement')
router.register('cycle-counts', CycleCountViewSet, basename='cycle-count')
router.register('restock-requests', RestockRequestViewSet, basename='restock-request')

urlpatterns = [
    path('insights/', stock_insights_view, name='stock-insights'),
    path('analytics/', stock_insights_view, name='analytics'),  # Keep for backward compatibility
    path('', include(router.urls)),
]
