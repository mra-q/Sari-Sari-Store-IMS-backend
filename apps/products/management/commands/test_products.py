from django.core.management.base import BaseCommand
from apps.products.models import Product
from apps.products.serializers import ProductSerializer

class Command(BaseCommand):
    help = 'Test product serialization'

    def handle(self, *args, **options):
        products = Product.objects.select_related('category').prefetch_related('inventory').all()
        self.stdout.write(f"Found {products.count()} products")
        
        for product in products:
            try:
                self.stdout.write(f"\nTesting product: {product.name} (ID: {product.id})")
                self.stdout.write(f"  - SKU: {product.sku}")
                self.stdout.write(f"  - Category: {product.category}")
                self.stdout.write(f"  - Has inventory: {hasattr(product, 'inventory')}")
                
                # Test current_stock property
                try:
                    stock = product.current_stock
                    self.stdout.write(f"  - Current stock: {stock}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  - Error getting current_stock: {e}"))
                
                # Test is_low_stock property
                try:
                    low_stock = product.is_low_stock
                    self.stdout.write(f"  - Is low stock: {low_stock}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  - Error getting is_low_stock: {e}"))
                
                # Test serialization
                try:
                    serializer = ProductSerializer(product)
                    data = serializer.data
                    self.stdout.write(self.style.SUCCESS(f"  - Serialization: OK"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  - Serialization error: {e}"))
                    import traceback
                    self.stdout.write(traceback.format_exc())
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing product {product.id}: {e}"))
                import traceback
                self.stdout.write(traceback.format_exc())
        
        self.stdout.write(self.style.SUCCESS('\nTest complete'))
