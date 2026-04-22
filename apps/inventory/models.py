from django.db import models
from apps.products.models import Product

class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'inventory'
        verbose_name_plural = 'Inventory'
    
    def __str__(self):
        return f"{self.product.name}: {self.quantity}"
