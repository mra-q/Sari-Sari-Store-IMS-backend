from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta, datetime
from .models import StockMovement
from apps.products.models import Product


def get_stock_out_statistics(period='monthly', year=None, month=None, week=None):
    """Get stock-out movement statistics based on period (weekly, monthly, annual)"""
    now = timezone.now()
    
    # Specific filtering
    if year and month:
        # Specific month in a year
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        end_date = timezone.make_aware(end_date)
        start_date = timezone.make_aware(start_date)
        
        # Get days in month
        days_in_month = (end_date - start_date).days
        data = []
        for day in range(1, min(days_in_month + 1, 31)):
            day_start = start_date + timedelta(days=day - 1)
            day_end = day_start + timedelta(days=1)
            
            stock_out = StockMovement.objects.filter(
                movement_type__in=['out', 'stock_out'],
                created_at__gte=day_start,
                created_at__lt=day_end
            ).aggregate(total=Sum('quantity'))
            
            data.append({
                'label': str(day),
                'value': abs(stock_out['total'] or 0)
            })
        return data
    
    elif year and week:
        # Specific week in a year
        jan_1 = datetime(year, 1, 1)
        start_date = jan_1 + timedelta(weeks=week - 1)
        end_date = start_date + timedelta(days=7)
        start_date = timezone.make_aware(start_date)
        end_date = timezone.make_aware(end_date)
        
        data = []
        for day in range(7):
            day_start = start_date + timedelta(days=day)
            day_end = day_start + timedelta(days=1)
            
            stock_out = StockMovement.objects.filter(
                movement_type__in=['out', 'stock_out'],
                created_at__gte=day_start,
                created_at__lt=day_end
            ).aggregate(total=Sum('quantity'))
            
            data.append({
                'label': day_start.strftime('%a'),
                'value': abs(stock_out['total'] or 0)
            })
        return data
    
    elif year:
        # Specific year - show all 12 months
        data = []
        for month_num in range(1, 13):
            month_start = timezone.make_aware(datetime(year, month_num, 1))
            if month_num == 12:
                month_end = timezone.make_aware(datetime(year + 1, 1, 1))
            else:
                month_end = timezone.make_aware(datetime(year, month_num + 1, 1))
            
            stock_out = StockMovement.objects.filter(
                movement_type__in=['out', 'stock_out'],
                created_at__gte=month_start,
                created_at__lt=month_end
            ).aggregate(total=Sum('quantity'))
            
            data.append({
                'label': month_start.strftime('%b'),
                'value': abs(stock_out['total'] or 0)
            })
        return data
    
    # Default period-based filtering
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
        
        stock_out = StockMovement.objects.filter(
            movement_type__in=['out', 'stock_out'],
            created_at__gte=period_start,
            created_at__lt=period_end
        ).aggregate(total=Sum('quantity'))
        
        data.insert(0, {
            'label': date_format(period_end),
            'value': abs(stock_out['total'] or 0)
        })
    
    return data


def get_product_statistics(period='monthly', year=None, month=None, week=None):
    """Get product category statistics"""
    now = timezone.now()
    
    # Specific filtering
    if year and month:
        start_date = timezone.make_aware(datetime(year, month, 1))
        if month == 12:
            end_date = timezone.make_aware(datetime(year + 1, 1, 1))
        else:
            end_date = timezone.make_aware(datetime(year, month + 1, 1))
    elif year and week:
        jan_1 = datetime(year, 1, 1)
        start_date = timezone.make_aware(jan_1 + timedelta(weeks=week - 1))
        end_date = start_date + timedelta(days=7)
    elif year:
        start_date = timezone.make_aware(datetime(year, 1, 1))
        end_date = timezone.make_aware(datetime(year + 1, 1, 1))
    else:
        # Default period-based filtering
        if period == 'weekly':
            start_date = now - timedelta(days=7)
        elif period == 'annual':
            start_date = now - timedelta(days=365)
        else:  # monthly
            start_date = now - timedelta(days=30)
        end_date = now
    
    # Get top 6 categories by stock-out volume
    category_stock_out = StockMovement.objects.filter(
        movement_type__in=['out', 'stock_out'],
        created_at__gte=start_date,
        created_at__lt=end_date
    ).values('product__category__name').annotate(
        total=Sum('quantity')
    ).order_by('-total')[:6]
    
    data = []
    for item in category_stock_out:
        if item['product__category__name']:
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
        
        data = [{
            'category': item['category__name'],
            'value': item['count']
        } for item in category_counts]
    
    return data
