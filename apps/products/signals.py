from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product

@receiver(post_save, sender=Product)
def create_inventory(sender, instance, created, **kwargs):
    if created:
        from apps.inventory.models import Inventory
        Inventory.objects.get_or_create(product=instance, defaults={'quantity': 0})
