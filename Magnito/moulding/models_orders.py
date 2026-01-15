from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Mould


class ProductionOrder(models.Model):
    """Model for production orders"""
    PRIORITY_CHOICES = [
        ('urgent', 'Urgent'),
        ('high', 'High'),
        ('normal', 'Normal'),
        ('low', 'Low'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_number = models.CharField(max_length=100, unique=True)
    mould = models.ForeignKey(Mould, on_delete=models.CASCADE, related_name='production_orders')
    product_name = models.CharField(max_length=200)
    customer_name = models.CharField(max_length=200)
    customer_contact = models.CharField(max_length=100, blank=True)
    
    # Order details
    quantity_ordered = models.IntegerField(help_text="Total quantity to produce")
    quantity_produced = models.IntegerField(default=0, help_text="Quantity already produced")
    unit = models.CharField(max_length=50, default='pieces', help_text="Unit of measurement")
    
    # Priority and status
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Dates
    order_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    start_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    
    # Additional info
    notes = models.TextField(blank=True)
    special_requirements = models.TextField(blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', 'due_date', '-created_at']
    
    def __str__(self):
        return f"{self.order_number} - {self.product_name} for {self.customer_name}"
    
    def quantity_remaining(self):
        """Calculate remaining quantity to produce"""
        return self.quantity_ordered - self.quantity_produced
    
    def progress_percentage(self):
        """Calculate production progress percentage"""
        if self.quantity_ordered == 0:
            return 0
        return round((self.quantity_produced / self.quantity_ordered) * 100, 1)
    
    def is_overdue(self):
        """Check if order is overdue"""
        if self.status in ['completed', 'cancelled']:
            return False
        return timezone.now().date() > self.due_date
    
    def days_until_due(self):
        """Calculate days until due date"""
        delta = self.due_date - timezone.now().date()
        return delta.days
    
    def priority_display_color(self):
        """Return color for priority badge"""
        colors = {
            'urgent': '#dc3545',
            'high': '#fd7e14',
            'normal': '#28a745',
            'low': '#6c757d',
        }
        return colors.get(self.priority, '#6c757d')
