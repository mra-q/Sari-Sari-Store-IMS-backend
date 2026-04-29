from django.core.management.base import BaseCommand
from apps.products.models import Product
from apps.inventory.models import Inventory

class Command(BaseCommand):
    help = 'Create missing inventory records for existing products'

    def handle(self, *args, **options):
        products = Product.objects.all()
        created_count = 0
        
        for product in products:
            _, created = Inventory.objects.get_or_create(
                product=product,
                defaults={'quantity': 0}
            )
            if created:
                created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Created {created_count} inventory records')
        )
