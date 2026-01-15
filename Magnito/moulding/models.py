from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Mould(models.Model):
    """Model for tracking moulds"""
    mould_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cavity_count = models.IntegerField(default=1)
    material_type = models.CharField(max_length=100)
    cycle_time = models.FloatField(help_text="Cycle time in seconds")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.mould_number} - {self.name}"


class MouldChange(models.Model):
    """Model for tracking mould changes"""
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    mould_from = models.ForeignKey(Mould, on_delete=models.CASCADE, related_name='changes_from', null=True, blank=True)
    mould_to = models.ForeignKey(Mould, on_delete=models.CASCADE, related_name='changes_to')
    machine_number = models.CharField(max_length=50)
    operator = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    scheduled_time = models.DateTimeField()
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Change to {self.mould_to} on {self.scheduled_time}"


class TroubleshootingIssue(models.Model):
    """Model for common troubleshooting issues"""
    CATEGORY_CHOICES = [
        ('quality', 'Quality Issue'),
        ('machine', 'Machine Issue'),
        ('material', 'Material Issue'),
        ('mould', 'Mould Issue'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    symptoms = models.TextField(help_text="Observable symptoms")
    solution = models.TextField(help_text="Step-by-step solution")
    prevention = models.TextField(blank=True, help_text="How to prevent this issue")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TroubleshootingLog(models.Model):
    """Model for logging troubleshooting incidents"""
    issue = models.ForeignKey(TroubleshootingIssue, on_delete=models.CASCADE)
    mould = models.ForeignKey(Mould, on_delete=models.CASCADE)
    machine_number = models.CharField(max_length=50)
    operator = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    resolution = models.TextField(blank=True)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.issue.title} - {self.created_at}"


class HourlyChecklist(models.Model):
    """Model for operator hourly checklist"""
    mould = models.ForeignKey(Mould, on_delete=models.CASCADE)
    machine_number = models.CharField(max_length=50)
    operator = models.ForeignKey(User, on_delete=models.CASCADE)
    check_time = models.DateTimeField(default=timezone.now)
    
    # Quality checks
    visual_inspection = models.BooleanField(default=False)
    dimensional_check = models.BooleanField(default=False)
    color_consistency = models.BooleanField(default=False)
    surface_finish = models.BooleanField(default=False)
    
    # Machine checks
    temperature_ok = models.BooleanField(default=False)
    pressure_ok = models.BooleanField(default=False)
    cycle_time_ok = models.BooleanField(default=False)
    
    # Material checks
    material_level_ok = models.BooleanField(default=False)
    material_drying_ok = models.BooleanField(default=False)
    
    # Additional notes
    notes = models.TextField(blank=True)
    issues_found = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Checklist - {self.machine_number} - {self.check_time}"


class MasterSample(models.Model):
    """Model for master samples"""
    mould = models.ForeignKey(Mould, on_delete=models.CASCADE)
    sample_number = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='master_samples/')
    description = models.TextField(blank=True)
    specifications = models.TextField(help_text="Key specifications and tolerances")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sample_number} - {self.mould}"


class ProductComparison(models.Model):
    """Model for product comparisons against master sample"""
    master_sample = models.ForeignKey(MasterSample, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='product_comparisons/')
    operator = models.ForeignKey(User, on_delete=models.CASCADE)
    machine_number = models.CharField(max_length=50)
    
    # Comparison results
    similarity_score = models.FloatField(null=True, blank=True, help_text="0-100 similarity percentage")
    defects_found = models.BooleanField(default=False)
    defect_description = models.TextField(blank=True)
    fix_instructions = models.TextField(blank=True)
    
    # Status
    approved = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comparison - {self.master_sample} - {self.created_at}"


class DefectType(models.Model):
    """Model for defect types and their fixes"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    common_causes = models.TextField()
    fix_instructions = models.TextField(help_text="Step-by-step instructions to fix")
    machine_adjustments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MouldRun(models.Model):
    """Model for tracking active mould runs with setter information"""
    mould = models.ForeignKey(Mould, on_delete=models.CASCADE)
    machine_number = models.CharField(max_length=50)
    setter_name = models.CharField(max_length=200, help_text="Name of the setter")
    start_time = models.DateTimeField(default=timezone.now)
    setter_completion_time = models.DateTimeField(help_text="When setter completed the setup")
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.mould} on {self.machine_number} - {self.start_time}"
    
    def duration(self):
        """Calculate run duration"""
        if self.end_time:
            delta = self.end_time - self.start_time
        else:
            delta = timezone.now() - self.start_time
        return delta
    
    def duration_display(self):
        """Return formatted duration string"""
        delta = self.duration()
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        if delta.days > 0:
            return f"{delta.days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"


# Import auth models
from .models_auth import Company, UserProfile


# Import order models
from .models_orders import ProductionOrder


# Import issue models
from .models_issues import IssueCategory, Issue, MaintenanceJobCard, IssueComment


# Import housekeeping models
from .models_housekeeping import HousekeepingTask
