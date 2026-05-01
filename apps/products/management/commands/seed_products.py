from django.core.management.base import BaseCommand
from apps.products.models import Category, Product
from apps.inventory.models import Inventory
import random

class Command(BaseCommand):
    help = 'Seed database with 5 categories and 5 products each'

    def handle(self, *args, **kwargs):
        categories_data = [
            {'name': 'Beverages', 'description': 'Soft drinks, water, and beverages'},
            {'name': 'Snacks', 'description': 'Chips, biscuits, and snack items'},
            {'name': 'Canned Goods', 'description': 'Canned and preserved foods'},
            {'name': 'Personal Care', 'description': 'Toiletries and hygiene products'},
            {'name': 'Household Items', 'description': 'Cleaning supplies and household essentials'},
        ]

        products_data = {
            'Beverages': [
                {'name': 'Coca-Cola 1.5L', 'sku': 'BEV-001', 'barcode': '4800888100016', 'unit_price': 65.00, 'cost_price': 55.00},
                {'name': 'C2 Green Tea 1L', 'sku': 'BEV-002', 'barcode': '4800016644429', 'unit_price': 35.00, 'cost_price': 28.00},
                {'name': 'Absolute Distilled Water 500ml', 'sku': 'BEV-003', 'barcode': '4800024621015', 'unit_price': 10.00, 'cost_price': 7.00},
                {'name': 'Zest-O Juice Drink 200ml', 'sku': 'BEV-004', 'barcode': '4800092310014', 'unit_price': 12.00, 'cost_price': 9.00},
                {'name': 'Nescafe 3-in-1 Sachet', 'sku': 'BEV-005', 'barcode': '4800361341516', 'unit_price': 8.00, 'cost_price': 6.00},
            ],
            'Snacks': [
                {'name': 'Chippy BBQ Flavor', 'sku': 'SNK-001', 'barcode': '4800194114028', 'unit_price': 15.00, 'cost_price': 11.00},
                {'name': 'Skyflakes Crackers', 'sku': 'SNK-002', 'barcode': '4800016100017', 'unit_price': 25.00, 'cost_price': 20.00},
                {'name': 'Piattos Cheese', 'sku': 'SNK-003', 'barcode': '4800194114219', 'unit_price': 18.00, 'cost_price': 14.00},
                {'name': 'Boy Bawang Cornick', 'sku': 'SNK-004', 'barcode': '4800092310212', 'unit_price': 12.00, 'cost_price': 9.00},
                {'name': 'Oishi Prawn Crackers', 'sku': 'SNK-005', 'barcode': '4800194114318', 'unit_price': 10.00, 'cost_price': 7.50},
            ],
            'Canned Goods': [
                {'name': 'Century Tuna Flakes 155g', 'sku': 'CAN-001', 'barcode': '4800024620018', 'unit_price': 35.00, 'cost_price': 28.00},
                {'name': 'Argentina Corned Beef 150g', 'sku': 'CAN-002', 'barcode': '4800092310519', 'unit_price': 42.00, 'cost_price': 35.00},
                {'name': 'Ligo Sardines 155g', 'sku': 'CAN-003', 'barcode': '4800092310618', 'unit_price': 22.00, 'cost_price': 18.00},
                {'name': 'Del Monte Spaghetti Sauce 250g', 'sku': 'CAN-004', 'barcode': '4800024621213', 'unit_price': 38.00, 'cost_price': 32.00},
                {'name': 'Mega Sardines Green 155g', 'sku': 'CAN-005', 'barcode': '4800092310717', 'unit_price': 20.00, 'cost_price': 16.00},
            ],
            'Personal Care': [
                {'name': 'Safeguard Bar Soap', 'sku': 'PER-001', 'barcode': '4902430548113', 'unit_price': 35.00, 'cost_price': 28.00},
                {'name': 'Colgate Toothpaste 50g', 'sku': 'PER-002', 'barcode': '8850006328019', 'unit_price': 28.00, 'cost_price': 22.00},
                {'name': 'Palmolive Shampoo Sachet', 'sku': 'PER-003', 'barcode': '8850006329016', 'unit_price': 8.00, 'cost_price': 6.00},
                {'name': 'Close-Up Toothpaste 25g', 'sku': 'PER-004', 'barcode': '8850006328217', 'unit_price': 15.00, 'cost_price': 12.00},
                {'name': 'Tide Detergent Powder 35g', 'sku': 'PER-005', 'barcode': '4902430548311', 'unit_price': 10.00, 'cost_price': 7.50},
            ],
            'Household Items': [
                {'name': 'Joy Dishwashing Liquid 250ml', 'sku': 'HOU-001', 'barcode': '4902430548410', 'unit_price': 32.00, 'cost_price': 26.00},
                {'name': 'Zonrox Bleach 500ml', 'sku': 'HOU-002', 'barcode': '4800092310815', 'unit_price': 28.00, 'cost_price': 22.00},
                {'name': 'Baygon Spray 300ml', 'sku': 'HOU-003', 'barcode': '4902430548519', 'unit_price': 85.00, 'cost_price': 70.00},
                {'name': 'Downy Fabric Conditioner Sachet', 'sku': 'HOU-004', 'barcode': '4902430548618', 'unit_price': 8.00, 'cost_price': 6.00},
                {'name': 'Domex Toilet Bowl Cleaner 500ml', 'sku': 'HOU-005', 'barcode': '8850006329214', 'unit_price': 45.00, 'cost_price': 38.00},
            ],
        }

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            
            for prod_data in products_data[cat_data['name']]:
                product, created = Product.objects.update_or_create(
                    sku=prod_data['sku'],
                    defaults={
                        'name': prod_data['name'],
                        'category': category,
                        'barcode': prod_data['barcode'],
                        'unit_price': prod_data['unit_price'],
                        'cost_price': prod_data['cost_price'],
                        'reorder_level': 10,
                    }
                )
                action = 'Created' if created else 'Updated'
                self.stdout.write(f'  - {action} product: {product.name}')
                
                # Create or update inventory with random stock
                stock_qty = random.randint(20, 100)
                inventory, inv_created = Inventory.objects.update_or_create(
                    product=product,
                    defaults={'quantity': stock_qty}
                )
                self.stdout.write(f'    Stock: {stock_qty} units')

        self.stdout.write(self.style.SUCCESS('\nSeeding completed!'))
