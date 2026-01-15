from django import forms
from .models import (
    MouldChange, TroubleshootingLog, HourlyChecklist,
    MasterSample, ProductComparison, MouldRun, HousekeepingTask
)


class MouldChangeForm(forms.ModelForm):
    class Meta:
        model = MouldChange
        fields = ['mould_from', 'mould_to', 'machine_number', 'scheduled_time', 'notes']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }


class TroubleshootingLogForm(forms.ModelForm):
    class Meta:
        model = TroubleshootingLog
        fields = ['issue', 'mould', 'machine_number', 'description', 'resolution', 'resolved']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'resolution': forms.Textarea(attrs={'rows': 4}),
        }


class HourlyChecklistForm(forms.ModelForm):
    class Meta:
        model = HourlyChecklist
        fields = [
            'mould', 'machine_number', 'check_time',
            'visual_inspection', 'dimensional_check', 'color_consistency', 'surface_finish',
            'temperature_ok', 'pressure_ok', 'cycle_time_ok',
            'material_level_ok', 'material_drying_ok',
            'notes', 'issues_found'
        ]
        widgets = {
            'check_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class MasterSampleForm(forms.ModelForm):
    class Meta:
        model = MasterSample
        fields = ['mould', 'sample_number', 'image', 'description', 'specifications']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'specifications': forms.Textarea(attrs={'rows': 4}),
        }


class ProductComparisonForm(forms.ModelForm):
    class Meta:
        model = ProductComparison
        fields = ['master_sample', 'product_image', 'machine_number', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class MouldRunForm(forms.ModelForm):
    class Meta:
        model = MouldRun
        fields = ['mould', 'machine_number', 'setter_name', 'start_time', 'setter_completion_time', 'notes']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'setter_completion_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


from .models_orders import ProductionOrder

class ProductionOrderForm(forms.ModelForm):
    class Meta:
        model = ProductionOrder
        fields = [
            'order_number', 'mould', 'product_name', 'customer_name', 'customer_contact',
            'quantity_ordered', 'unit', 'priority', 'order_date', 'due_date',
            'notes', 'special_requirements'
        ]
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'special_requirements': forms.Textarea(attrs={'rows': 3}),
        }


from .models_issues import Issue, MaintenanceJobCard, IssueComment

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            'issue_number', 'title', 'category', 'description', 'mould', 'machine_number',
            'customer_name', 'product_name', 'priority', 'assigned_to', 'notes'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class IssueResolveForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['resolution', 'root_cause', 'corrective_action', 'preventive_action']
        widgets = {
            'resolution': forms.Textarea(attrs={'rows': 3}),
            'root_cause': forms.Textarea(attrs={'rows': 3}),
            'corrective_action': forms.Textarea(attrs={'rows': 3}),
            'preventive_action': forms.Textarea(attrs={'rows': 3}),
        }


class MaintenanceJobCardForm(forms.ModelForm):
    class Meta:
        model = MaintenanceJobCard
        fields = [
            'job_card_number', 'title', 'description', 'issue', 'machine_number', 'mould',
            'priority', 'assigned_to', 'scheduled_date', 'notes'
        ]
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class IssueCommentForm(forms.ModelForm):
    class Meta:
        model = IssueComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        }



class HousekeepingTaskForm(forms.ModelForm):
    class Meta:
        model = HousekeepingTask
        fields = ['area_type', 'area_description', 'before_image', 'before_notes']
        widgets = {
            'before_notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the condition before cleaning...'}),
            'area_description': forms.TextInput(attrs={'placeholder': 'e.g., Machine #5, Mould Storage, Production Floor'}),
        }


class HousekeepingCompleteForm(forms.ModelForm):
    class Meta:
        model = HousekeepingTask
        fields = ['after_image', 'after_notes', 'cleaning_products_used', 'issues_found']
        widgets = {
            'after_notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the condition after cleaning...'}),
            'cleaning_products_used': forms.Textarea(attrs={'rows': 2, 'placeholder': 'List cleaning products used...'}),
            'issues_found': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any issues discovered during cleaning...'}),
        }
