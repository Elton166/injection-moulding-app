from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class HousekeepingTask(models.Model):
    """Model for housekeeping tasks with before/after pictures"""
    AREA_CHOICES = [
        ('machine', 'Machine'),
        ('mould', 'Mould'),
        ('factory_floor', 'Factory Floor'),
        ('storage', 'Storage Area'),
        ('workstation', 'Workstation'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    task_number = models.CharField(max_length=50, unique=True, blank=True)
    area_type = models.CharField(max_length=20, choices=AREA_CHOICES)
    area_description = models.CharField(max_length=200, help_text="e.g., Machine #5, Mould Storage, Production Floor")
    
    # Before cleaning
    before_image = models.ImageField(upload_to='housekeeping/before/', blank=True, null=True)
    before_notes = models.TextField(blank=True, help_text="Condition before cleaning")
    
    # After cleaning
    after_image = models.ImageField(upload_to='housekeeping/after/', blank=True, null=True)
    after_notes = models.TextField(blank=True, help_text="Condition after cleaning")
    
    # Task details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='housekeeping_tasks')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Additional info
    cleaning_products_used = models.TextField(blank=True, help_text="List of cleaning products used")
    issues_found = models.TextField(blank=True, help_text="Any issues discovered during cleaning")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.task_number:
            # Generate task number
            last_task = HousekeepingTask.objects.order_by('-id').first()
            if last_task and last_task.task_number:
                try:
                    last_num = int(last_task.task_number.split('-')[1])
                    self.task_number = f'HK-{last_num + 1:05d}'
                except:
                    self.task_number = f'HK-{self.id or 1:05d}'
            else:
                self.task_number = 'HK-00001'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.task_number} - {self.get_area_type_display()} - {self.area_description}"
    
    def duration(self):
        """Calculate task duration"""
        if self.completed_at and self.started_at:
            delta = self.completed_at - self.started_at
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            if delta.days > 0:
                return f"{delta.days}d {hours}h {minutes}m"
            elif hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
        return "N/A"
