from django.core.management.base import BaseCommand
from apps.products.models import Category, Product
from apps.inventory.models import Inventory

class Command(BaseCommand):
    help = 'Populate database with Sari-Sari Store categories and products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating categories and products...')
        
        data = {
            'Beverages': [
                {'name': 'Coca-Cola 1.5L', 'sku': 'BEV001', 'barcode': '4800888100016', 'price': 65.00, 'cost': 55.00, 'stock': 24},
                {'name': 'Royal Tru-Orange 1L', 'sku': 'BEV002', 'barcode': '4800888100023', 'price': 45.00, 'cost': 38.00, 'stock': 30},
                {'name': 'C2 Green Tea 1L', 'sku': 'BEV003', 'barcode': '4800888100030', 'price': 35.00, 'cost': 28.00, 'stock': 36},
                {'name': 'Zest-O Orange 200ml', 'sku': 'BEV004', 'barcode': '4800888100047', 'price': 12.00, 'cost': 9.00, 'stock': 48},
                {'name': 'Bottled Water 500ml', 'sku': 'BEV005', 'barcode': '4800888100054', 'price': 15.00, 'cost': 11.00, 'stock': 60},
            ],
            'Snacks': [
                {'name': 'Chippy BBQ', 'sku': 'SNK001', 'barcode': '4800016100017', 'price': 8.00, 'cost': 6.00, 'stock': 50},
                {'name': 'Piattos Cheese', 'sku': 'SNK002', 'barcode': '4800016100024', 'price': 25.00, 'cost': 20.00, 'stock': 40},
                {'name': 'Nova Barbecue', 'sku': 'SNK003', 'barcode': '4800016100031', 'price': 7.50, 'cost': 5.50, 'stock': 45},
                {'name': 'Oishi Prawn Crackers', 'sku': 'SNK004', 'barcode': '4800016100048', 'price': 6.50, 'cost': 5.00, 'stock': 55},
                {'name': 'Clover Chips', 'sku': 'SNK005', 'barcode': '4800016100055', 'price': 7.00, 'cost': 5.50, 'stock': 48},
            ],
            'Instant Noodles': [
                {'name': 'Lucky Me Pancit Canton Original', 'sku': 'NOD001', 'barcode': '4800194100014', 'price': 13.00, 'cost': 10.00, 'stock': 60},
                {'name': 'Lucky Me Beef Mami', 'sku': 'NOD002', 'barcode': '4800194100021', 'price': 12.00, 'cost': 9.50, 'stock': 55},
                {'name': 'Nissin Cup Noodles Seafood', 'sku': 'NOD003', 'barcode': '4800194100038', 'price': 28.00, 'cost': 23.00, 'stock': 30},
                {'name': 'Payless Pancit Canton', 'sku': 'NOD004', 'barcode': '4800194100045', 'price': 10.00, 'cost': 7.50, 'stock': 50},
                {'name': 'Quickchow Chicken', 'sku': 'NOD005', 'barcode': '4800194100052', 'price': 9.00, 'cost': 7.00, 'stock': 45},
            ],
            'Canned Goods': [
                {'name': 'Century Tuna Flakes in Oil 155g', 'sku': 'CAN001', 'barcode': '4800024100011', 'price': 35.00, 'cost': 28.00, 'stock': 40},
                {'name': 'Argentina Corned Beef 150g', 'sku': 'CAN002', 'barcode': '4800024100028', 'price': 42.00, 'cost': 35.00, 'stock': 35},
                {'name': 'Ligo Sardines Red 155g', 'sku': 'CAN003', 'barcode': '4800024100035', 'price': 22.00, 'cost': 18.00, 'stock': 45},
                {'name': 'CDO Liver Spread 85g', 'sku': 'CAN004', 'barcode': '4800024100042', 'price': 28.00, 'cost': 23.00, 'stock': 38},
                {'name': 'Del Monte Spaghetti Sauce 250g', 'sku': 'CAN005', 'barcode': '4800024100059', 'price': 38.00, 'cost': 31.00, 'stock': 30},
            ],
            'Rice & Grains': [
                {'name': 'Sinandomeng Rice 1kg', 'sku': 'RIC001', 'barcode': '4800123100018', 'price': 55.00, 'cost': 48.00, 'stock': 50},
                {'name': 'Jasmine Rice 1kg', 'sku': 'RIC002', 'barcode': '4800123100025', 'price': 65.00, 'cost': 56.00, 'stock': 40},
                {'name': 'Dinorado Rice 1kg', 'sku': 'RIC003', 'barcode': '4800123100032', 'price': 75.00, 'cost': 65.00, 'stock': 35},
                {'name': 'Brown Rice 1kg', 'sku': 'RIC004', 'barcode': '4800123100049', 'price': 70.00, 'cost': 60.00, 'stock': 25},
                {'name': 'Malagkit Rice 1kg', 'sku': 'RIC005', 'barcode': '4800123100056', 'price': 68.00, 'cost': 58.00, 'stock': 30},
            ],
            'Condiments': [
                {'name': 'Datu Puti Soy Sauce 385ml', 'sku': 'CON001', 'barcode': '4800092100015', 'price': 22.00, 'cost': 18.00, 'stock': 45},
                {'name': 'Silver Swan Vinegar 385ml', 'sku': 'CON002', 'barcode': '4800092100022', 'price': 18.00, 'cost': 14.00, 'stock': 50},
                {'name': 'UFC Banana Catsup 320g', 'sku': 'CON003', 'barcode': '4800092100039', 'price': 32.00, 'cost': 26.00, 'stock': 40},
                {'name': 'Mama Sita Oyster Sauce 405g', 'sku': 'CON004', 'barcode': '4800092100046', 'price': 45.00, 'cost': 37.00, 'stock': 35},
                {'name': 'Lorins Fish Sauce 350ml', 'sku': 'CON005', 'barcode': '4800092100053', 'price': 25.00, 'cost': 20.00, 'stock': 42},
            ],
            'Cooking Essentials': [
                {'name': 'Minola Cooking Oil 1L', 'sku': 'COK001', 'barcode': '4800067100012', 'price': 85.00, 'cost': 72.00, 'stock': 30},
                {'name': 'Baguio Oil 1L', 'sku': 'COK002', 'barcode': '4800067100029', 'price': 78.00, 'cost': 66.00, 'stock': 35},
                {'name': 'Ajinomoto Umami Seasoning 100g', 'sku': 'COK003', 'barcode': '4800067100036', 'price': 28.00, 'cost': 23.00, 'stock': 48},
                {'name': 'Knorr Chicken Cube 60g', 'sku': 'COK004', 'barcode': '4800067100043', 'price': 32.00, 'cost': 26.00, 'stock': 45},
                {'name': 'Iodized Salt 1kg', 'sku': 'COK005', 'barcode': '4800067100050', 'price': 18.00, 'cost': 14.00, 'stock': 40},
            ],
            'Personal Care': [
                {'name': 'Safeguard Bar Soap 135g', 'sku': 'PER001', 'barcode': '4800034100019', 'price': 38.00, 'cost': 31.00, 'stock': 50},
                {'name': 'Palmolive Shampoo 180ml', 'sku': 'PER002', 'barcode': '4800034100026', 'price': 55.00, 'cost': 45.00, 'stock': 40},
                {'name': 'Colgate Toothpaste 150g', 'sku': 'PER003', 'barcode': '4800034100033', 'price': 68.00, 'cost': 56.00, 'stock': 35},
                {'name': 'Close Up Toothpaste 100g', 'sku': 'PER004', 'barcode': '4800034100040', 'price': 52.00, 'cost': 43.00, 'stock': 38},
                {'name': 'Rejoice Shampoo Sachet 12ml', 'sku': 'PER005', 'barcode': '4800034100057', 'price': 8.00, 'cost': 6.00, 'stock': 100},
            ],
            'Household Items': [
                {'name': 'Tide Detergent Powder 120g', 'sku': 'HOU001', 'barcode': '4800056100013', 'price': 28.00, 'cost': 23.00, 'stock': 45},
                {'name': 'Surf Powder 120g', 'sku': 'HOU002', 'barcode': '4800056100020', 'price': 25.00, 'cost': 20.00, 'stock': 50},
                {'name': 'Zonrox Bleach 500ml', 'sku': 'HOU003', 'barcode': '4800056100037', 'price': 32.00, 'cost': 26.00, 'stock': 35},
                {'name': 'Domex Toilet Bowl Cleaner 500ml', 'sku': 'HOU004', 'barcode': '4800056100044', 'price': 45.00, 'cost': 37.00, 'stock': 30},
                {'name': 'Joy Dishwashing Liquid 250ml', 'sku': 'HOU005', 'barcode': '4800056100051', 'price': 38.00, 'cost': 31.00, 'stock': 40},
            ],
            'Dairy & Eggs': [
                {'name': 'Alaska Evaporated Milk 370ml', 'sku': 'DAI001', 'barcode': '4800078100010', 'price': 48.00, 'cost': 40.00, 'stock': 35},
                {'name': 'Bear Brand Powdered Milk 150g', 'sku': 'DAI002', 'barcode': '4800078100027', 'price': 85.00, 'cost': 72.00, 'stock': 30},
                {'name': 'Nestle Fresh Milk 1L', 'sku': 'DAI003', 'barcode': '4800078100034', 'price': 95.00, 'cost': 82.00, 'stock': 20},
                {'name': 'Eden Cheese 165g', 'sku': 'DAI004', 'barcode': '4800078100041', 'price': 68.00, 'cost': 56.00, 'stock': 25},
                {'name': 'Fresh Eggs (per piece)', 'sku': 'DAI005', 'barcode': '4800078100058', 'price': 8.00, 'cost': 6.50, 'stock': 120},
            ],
        }

        for category_name, products in data.items():
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'description': f'{category_name} products for Sari-Sari Store'}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category_name}'))
            
            for product_data in products:
                product, created = Product.objects.get_or_create(
                    sku=product_data['sku'],
                    defaults={
                        'name': product_data['name'],
                        'barcode': product_data['barcode'],
                        'category': category,
                        'unit_price': product_data['price'],
                        'cost_price': product_data['cost'],
                        'reorder_level': 10,
                        'is_active': True,
                    }
                )
                
                if created:
                    Inventory.objects.get_or_create(
                        product=product,
                        defaults={'quantity': product_data['stock']}
                    )
                    self.stdout.write(f'  - Created: {product.name}')
        
        self.stdout.write(self.style.SUCCESS('\nSuccessfully populated database!'))
        self.stdout.write(f'Total categories: {Category.objects.count()}')
        self.stdout.write(f'Total products: {Product.objects.count()}')
