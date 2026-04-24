from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models import Product
import uuid

User = get_user_model()

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('stock_in', 'Stock In'),
        ('stock_out', 'Stock Out'),
        ('adjustment', 'Adjustment'),
    ]
    
    REASON_CHOICES = [
        ('sale', 'Sale'),
        ('restock', 'Restock'),
        ('damage', 'Damage'),
        ('expired', 'Expired'),
        ('return', 'Return'),
        ('theft', 'Theft'),
        ('adjustment', 'Adjustment'),
        ('cycle_count', 'Cycle Count'),
        ('misc', 'Miscellaneous'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=20, choices=REASON_CHOICES, blank=True)
    notes = models.TextField(blank=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'stock_movements'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', 'movement_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.product.name} - {self.movement_type}: {self.quantity}"

class CycleCount(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cycle_counts')
    expected_quantity = models.IntegerField()
    actual_quantity = models.IntegerField(null=True, blank=True)
    variance = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    counted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'cycle_counts'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if self.actual_quantity is not None:
            self.variance = self.actual_quantity - self.expected_quantity
        super().save(*args, **kwargs)

class RestockRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='restock_requests')
    requested_quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='restock_requests')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_restocks')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'restock_requests'
        ordering = ['-created_at']
