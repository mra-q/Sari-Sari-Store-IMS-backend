from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import StockMovement
from apps.products.models import Product


def get_sales_statistics(period='monthly'):
    """Get sales statistics based on period (weekly, monthly, annual)"""
    now = timezone.now()
    
    if period == 'weekly':
        periods = 7
        delta = timedelta(days=1)
        date_format = lambda d: d.strftime('%a')
    elif period == 'annual':
        periods = 12
        delta = timedelta(days=30)
        date_format = lambda d: d.strftime('%b %Y')
    else:  # monthly (default)
        periods = 6
        delta = timedelta(days=30)
        date_format = lambda d: d.strftime('%b')
    
    data = []
    for i in range(periods):
        period_end = now - (delta * i)
        period_start = period_end - delta
        
        # Get outgoing stock movements (sales)
        sales = StockMovement.objects.filter(
            movement_type='out',
            created_at__gte=period_start,
            created_at__lt=period_end
        ).aggregate(total=Sum('quantity'))
        
        data.insert(0, {
            'label': date_format(period_end),
            'value': abs(sales['total'] or 0)  # Use absolute value
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
    
    # Get top 6 categories by sales volume (outgoing movements)
    category_sales = StockMovement.objects.filter(
        movement_type='out',
        created_at__gte=start_date
    ).values('product__category__name').annotate(
        total=Sum('quantity')
    ).order_by('-total')[:6]
    
    data = []
    for item in category_sales:
        if item['product__category__name']:  # Skip null categories
            data.append({
                'category': item['product__category__name'],
                'value': abs(item['total'] or 0)
            })
    
    # If no sales data, return product count by category
    if not data:
        category_counts = Product.objects.filter(
            category__isnull=False
        ).values('category__name').annotate(
            count=Count('id')
        ).order_by('-count')[:6]
        
        data = [{
            'category': item['category__name'],
            'value': item['count']
        } for item in category_counts]
    
    return data
