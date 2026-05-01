from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import StockMovement
from apps.products.models import Product


def get_stock_out_statistics(period='monthly'):
    """Get stock-out movement statistics based on period (weekly, monthly, annual)"""
    now = timezone.now()
    
    def format_weekly(date):
        return date.strftime('%a')
    
    def format_annual(date):
        return date.strftime('%b %Y')
    
    def format_monthly(date):
        return date.strftime('%b')
    
    if period == 'weekly':
        periods = 7
        delta = timedelta(days=1)
        date_format = format_weekly
    elif period == 'annual':
        periods = 12
        delta = timedelta(days=30)
        date_format = format_annual
    else:  # monthly (default)
        periods = 6
        delta = timedelta(days=30)
        date_format = format_monthly
    
    data = []
    for i in range(periods):
        period_end = now - (delta * i)
        period_start = period_end - delta
        
        # Get outgoing stock movements
        stock_out = StockMovement.objects.filter(
            movement_type='out',
            created_at__gte=period_start,
            created_at__lt=period_end
        ).aggregate(total=Sum('quantity'))
        
        data.insert(0, {
            'label': date_format(period_end),
            'value': abs(stock_out['total'] or 0)  # Use absolute value
        })
    
    return data


def get_product_statistics(period='monthly'):
    """Get product category statistics"""
    now = timezone.now()
    
    if period == 'weekly':
        start_date = now - timedelta(days=7)
    elif period == 'annual':
        start_date = now - timedelta(days=365)
    else:  # monthly
        start_date = now - timedelta(days=30)
    
    # Get top 6 categories by stock-out volume (outgoing movements)
    category_stock_out = StockMovement.objects.filter(
        movement_type='out',
        created_at__gte=start_date
    ).values('product__category__name').annotate(
        total=Sum('quantity')
    ).order_by('-total')[:6]
    
    data = []
    for item in category_stock_out:
        if item['product__category__name']:  # Skip null categories
            data.append({
                'category': item['product__category__name'],
                'value': abs(item['total'] or 0)
            })
    
    # If no stock-out data, return product count by category
    if not data:
        category_counts = Product.objects.filter(
            category__isnull=False
        ).values('category__name').annotate(
            count=Count('id')
        ).order_by('-count')[:6]
        
        # Build data list from category counts
        data = []
        for item in category_counts:
            data.append({
                'category': item['category__name'],
                'value': item['count']
            })
    
    return data
