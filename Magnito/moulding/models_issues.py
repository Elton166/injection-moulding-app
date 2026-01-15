from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Mould


class IssueCategory(models.Model):
    """Categories for different types of issues"""
    CATEGORY_TYPES = [
        ('customer_complaint', 'Customer Complaint'),
        ('mould_issue', 'Mould Issue'),
        ('product_defect', 'Product Defect'),
        ('machine_issue', 'Machine Issue'),
        ('maintenance', 'Maintenance'),
    ]
    
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=30, choices=CATEGORY_TYPES)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#667eea', help_text="Hex color code")
    
    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"


class Issue(models.Model):
    """Main issue tracking model"""
    PRIORITY_CHOICES = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    issue_number = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(IssueCategory, on_delete=models.CASCADE)
    description = models.TextField()
    
    # Related entities
    mould = models.ForeignKey(Mould, on_delete=models.SET_NULL, null=True, blank=True)
    machine_number = models.CharField(max_length=50, blank=True)
    customer_name = models.CharField(max_length=200, blank=True, help_text="For customer complaints")
    product_name = models.CharField(max_length=200, blank=True)
    
    # Priority and status
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    # People
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_issues')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    
    # Dates and times
    reported_date = models.DateTimeField(default=timezone.now)
    started_date = models.DateTimeField(null=True, blank=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    
    # Resolution
    resolution = models.TextField(blank=True)
    root_cause = models.TextField(blank=True)
    corrective_action = models.TextField(blank=True)
    preventive_action = models.TextField(blank=True)
    
    # Additional info
    attachments = models.TextField(blank=True, help_text="File paths or URLs")
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', '-reported_date']
    
    def __str__(self):
        return f"{self.issue_number} - {self.title}"
    
    def time_to_resolve(self):
        """Calculate time taken to resolve issue"""
        if self.resolved_date and self.reported_date:
            delta = self.resolved_date - self.reported_date
            hours = delta.total_seconds() / 3600
            if hours < 24:
                return f"{int(hours)}h {int((hours % 1) * 60)}m"
            else:
                days = delta.days
                remaining_hours = int((delta.total_seconds() % 86400) / 3600)
                return f"{days}d {remaining_hours}h"
        return "Not resolved"
    
    def time_open(self):
        """Calculate how long issue has been open"""
        if self.status in ['resolved', 'closed']:
            return self.time_to_resolve()
        
        delta = timezone.now() - self.reported_date
        hours = delta.total_seconds() / 3600
        if hours < 24:
            return f"{int(hours)}h {int((hours % 1) * 60)}m"
        else:
            days = delta.days
            remaining_hours = int((delta.total_seconds() % 86400) / 3600)
            return f"{days}d {remaining_hours}h"
    
    def priority_color(self):
        """Return color for priority badge"""
        colors = {
            'critical': '#dc3545',
            'high': '#fd7e14',
            'medium': '#ffc107',
            'low': '#28a745',
        }
        return colors.get(self.priority, '#6c757d')


class MaintenanceJobCard(models.Model):
    """Job cards for maintenance tasks"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    job_card_number = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Related
    issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, null=True, blank=True, related_name='job_cards')
    machine_number = models.CharField(max_length=50, blank=True)
    mould = models.ForeignKey(Mould, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Status and priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=Issue.PRIORITY_CHOICES, default='medium')
    
    # People
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_job_cards')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_job_cards')
    
    # Dates
    scheduled_date = models.DateField()
    started_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    # Work details
    work_performed = models.TextField(blank=True)
    parts_used = models.TextField(blank=True, help_text="List of parts/materials used")
    labor_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_date', '-created_at']
    
    def __str__(self):
        return f"{self.job_card_number} - {self.title}"
    
    def duration(self):
        """Calculate job duration"""
        if self.completed_date and self.started_date:
            delta = self.completed_date - self.started_date
            hours = delta.total_seconds() / 3600
            return f"{hours:.1f}h"
        return "N/A"


class IssueComment(models.Model):
    """Comments/updates on issues"""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment on {self.issue.issue_number} by {self.user.username}"
