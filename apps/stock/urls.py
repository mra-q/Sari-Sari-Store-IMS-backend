from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockMovementViewSet, CycleCountViewSet, RestockRequestViewSet, analytics_view

router = DefaultRouter()
router.register('movements', StockMovementViewSet, basename='movement')
router.register('cycle-counts', CycleCountViewSet, basename='cycle-count')
router.register('restock-requests', RestockRequestViewSet, basename='restock-request')

urlpatterns = [
    path('analytics/', analytics_view, name='analytics'),
    path('', include(router.urls)),
]
