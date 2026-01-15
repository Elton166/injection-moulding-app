from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Company(models.Model):
    """Model for companies"""
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    registration_number = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Login credentials
    username = models.CharField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "Companies"
    
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Extended user profile for managers and supervisors"""
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('supervisor', 'Supervisor'),
        ('operator', 'Operator'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='operator')
    employee_id = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='created_employees')
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role} at {self.company}"
    
    class Meta:
        unique_together = ['company', 'employee_id']
