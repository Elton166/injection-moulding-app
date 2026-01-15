"""
Setup script to create issue categories
Run: python setup_issues.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'injection_moulding.settings')
django.setup()

from moulding.models_issues import IssueCategory

def create_issue_categories():
    print("Creating issue categories...")
    
    categories = [
        {
            'name': 'Customer Complaint - Quality',
            'category_type': 'customer_complaint',
            'description': 'Quality issues reported by customers',
            'color': '#dc3545'
        },
        {
            'name': 'Customer Complaint - Delivery',
            'category_type': 'customer_complaint',
            'description': 'Delivery and timing complaints',
            'color': '#fd7e14'
        },
        {
            'name': 'Mould Wear',
            'category_type': 'mould_issue',
            'description': 'Mould wear and tear issues',
            'color': '#ffc107'
        },
        {
            'name': 'Mould Damage',
            'category_type': 'mould_issue',
            'description': 'Physical damage to moulds',
            'color': '#dc3545'
        },
        {
            'name': 'Product Defect - Dimensional',
            'category_type': 'product_defect',
            'description': 'Dimensional defects in products',
            'color': '#fd7e14'
        },
        {
            'name': 'Product Defect - Surface',
            'category_type': 'product_defect',
            'description': 'Surface finish defects',
            'color': '#ffc107'
        },
        {
            'name': 'Machine Breakdown',
            'category_type': 'machine_issue',
            'description': 'Machine breakdowns and failures',
            'color': '#dc3545'
        },
        {
            'name': 'Machine Performance',
            'category_type': 'machine_issue',
            'description': 'Performance and efficiency issues',
            'color': '#fd7e14'
        },
        {
            'name': 'Preventive Maintenance',
            'category_type': 'maintenance',
            'description': 'Scheduled preventive maintenance',
            'color': '#28a745'
        },
        {
            'name': 'Corrective Maintenance',
            'category_type': 'maintenance',
            'description': 'Corrective maintenance tasks',
            'color': '#ffc107'
        },
    ]
    
    for cat_data in categories:
        IssueCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
    
    print(f"✓ Created {len(categories)} issue categories")
    print("\n✅ Issue categories setup complete!")

if __name__ == '__main__':
    create_issue_categories()
