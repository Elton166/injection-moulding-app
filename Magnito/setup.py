"""
Setup script to initialize the database with sample data
Run this after migrations: python setup.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'injection_moulding.settings')
django.setup()

from django.contrib.auth.models import User
from moulding.models import (
    Mould, TroubleshootingIssue, DefectType
)

def create_sample_data():
    print("Creating sample data...")
    
    # Create admin user if not exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✓ Admin user created (username: admin, password: admin123)")
    
    # Create sample moulds
    moulds_data = [
        {
            'mould_number': 'M001',
            'name': 'Bottle Cap Mould',
            'description': 'Standard bottle cap mould',
            'cavity_count': 8,
            'material_type': 'PP',
            'cycle_time': 15.5
        },
        {
            'mould_number': 'M002',
            'name': 'Container Base',
            'description': 'Food container base mould',
            'cavity_count': 4,
            'material_type': 'HDPE',
            'cycle_time': 22.0
        },
        {
            'mould_number': 'M003',
            'name': 'Automotive Part',
            'description': 'Dashboard component',
            'cavity_count': 2,
            'material_type': 'ABS',
            'cycle_time': 35.0
        }
    ]
    
    for data in moulds_data:
        Mould.objects.get_or_create(mould_number=data['mould_number'], defaults=data)
    print(f"✓ Created {len(moulds_data)} sample moulds")
    
    # Create troubleshooting issues
    issues_data = [
        {
            'title': 'Short Shot',
            'category': 'quality',
            'description': 'Incomplete part filling - part is not completely formed',
            'symptoms': '- Part is incomplete\n- Missing sections\n- Thin or weak areas',
            'solution': '1. Increase injection pressure\n2. Increase material temperature\n3. Increase injection speed\n4. Check for material blockage\n5. Verify adequate material supply',
            'prevention': 'Regular maintenance of injection system, proper material drying, consistent temperature control'
        },
        {
            'title': 'Flash (Excess Material)',
            'category': 'quality',
            'description': 'Excess material escaping from mould cavity',
            'symptoms': '- Thin material at parting line\n- Excess material on part edges\n- Rough edges',
            'solution': '1. Reduce injection pressure\n2. Reduce material temperature\n3. Increase clamping force\n4. Inspect and repair mould parting line\n5. Check mould alignment',
            'prevention': 'Regular mould maintenance, proper clamping force, controlled injection parameters'
        },
        {
            'title': 'Sink Marks',
            'category': 'quality',
            'description': 'Depressions on part surface',
            'symptoms': '- Visible depressions\n- Surface irregularities\n- Uneven appearance',
            'solution': '1. Increase packing pressure\n2. Extend packing time\n3. Reduce material temperature\n4. Increase cooling time\n5. Optimize gate location',
            'prevention': 'Proper cooling design, adequate packing pressure, optimized wall thickness'
        },
        {
            'title': 'Warpage',
            'category': 'quality',
            'description': 'Part distortion or bending',
            'symptoms': '- Part does not sit flat\n- Twisted or bent appearance\n- Dimensional issues',
            'solution': '1. Optimize cooling system\n2. Reduce material temperature\n3. Adjust packing pressure\n4. Increase cooling time\n5. Check mould temperature uniformity',
            'prevention': 'Uniform cooling, proper material selection, balanced mould design'
        },
        {
            'title': 'Flow Marks',
            'category': 'quality',
            'description': 'Wavy lines or patterns on part surface',
            'symptoms': '- Visible lines on surface\n- Wavy patterns\n- Color variations',
            'solution': '1. Increase injection speed\n2. Increase material temperature\n3. Improve mould venting\n4. Optimize gate location\n5. Increase mould temperature',
            'prevention': 'Proper gate design, adequate venting, controlled injection speed'
        },
        {
            'title': 'Material Contamination',
            'category': 'material',
            'description': 'Foreign material in product',
            'symptoms': '- Visible specks or particles\n- Color inconsistency\n- Surface defects',
            'solution': '1. Clean hopper and feed system\n2. Purge machine with clean material\n3. Check material storage\n4. Inspect material for contamination\n5. Clean mould cavity',
            'prevention': 'Proper material storage, regular cleaning, material inspection'
        }
    ]
    
    for data in issues_data:
        TroubleshootingIssue.objects.get_or_create(title=data['title'], defaults=data)
    print(f"✓ Created {len(issues_data)} troubleshooting issues")
    
    # Create defect types
    defects_data = [
        {
            'name': 'Short Shot',
            'description': 'Incomplete filling of the mould cavity resulting in missing sections',
            'common_causes': 'Insufficient material, low injection pressure, cold material temperature, blocked gates',
            'fix_instructions': '1. Increase injection pressure by 5-10%\n2. Raise material temperature by 10-15°C\n3. Increase injection speed\n4. Check and clear any blockages\n5. Verify material supply is adequate',
            'machine_adjustments': 'Injection Pressure: +5-10%\nMaterial Temp: +10-15°C\nInjection Speed: Increase'
        },
        {
            'name': 'Flash',
            'description': 'Excess material escaping at the parting line or other mould openings',
            'common_causes': 'Excessive injection pressure, worn mould, insufficient clamping force, high material temperature',
            'fix_instructions': '1. Reduce injection pressure by 5-10%\n2. Lower material temperature by 10-15°C\n3. Increase clamping force\n4. Inspect mould for wear\n5. Check mould alignment',
            'machine_adjustments': 'Injection Pressure: -5-10%\nMaterial Temp: -10-15°C\nClamping Force: Increase'
        },
        {
            'name': 'Sink Marks',
            'description': 'Depressions on the surface caused by shrinkage',
            'common_causes': 'Insufficient packing pressure, inadequate cooling time, thick wall sections',
            'fix_instructions': '1. Increase packing pressure by 10-15%\n2. Extend packing time by 1-2 seconds\n3. Reduce material temperature\n4. Increase cooling time\n5. Review part design for thick sections',
            'machine_adjustments': 'Packing Pressure: +10-15%\nPacking Time: +1-2 sec\nCooling Time: +2-3 sec'
        },
        {
            'name': 'Warpage',
            'description': 'Distortion or bending of the part after ejection',
            'common_causes': 'Uneven cooling, high material temperature, residual stress, improper ejection',
            'fix_instructions': '1. Balance cooling channels\n2. Reduce material temperature by 10-20°C\n3. Adjust packing pressure\n4. Increase cooling time by 20-30%\n5. Check ejection system',
            'machine_adjustments': 'Material Temp: -10-20°C\nCooling Time: +20-30%\nPacking Pressure: Adjust'
        },
        {
            'name': 'Flow Marks',
            'description': 'Wavy lines or patterns on the surface',
            'common_causes': 'Low injection speed, cold material, poor venting, cold mould',
            'fix_instructions': '1. Increase injection speed by 10-20%\n2. Raise material temperature by 10-15°C\n3. Improve mould venting\n4. Increase mould temperature by 5-10°C\n5. Check gate location',
            'machine_adjustments': 'Injection Speed: +10-20%\nMaterial Temp: +10-15°C\nMould Temp: +5-10°C'
        }
    ]
    
    for data in defects_data:
        DefectType.objects.get_or_create(name=data['name'], defaults=data)
    print(f"✓ Created {len(defects_data)} defect types")
    
    print("\n✅ Sample data created successfully!")
    print("\nYou can now:")
    print("1. Run the server: python manage.py runserver")
    print("2. Access admin panel: http://localhost:8000/admin")
    print("3. Login with: admin / admin123")

if __name__ == '__main__':
    create_sample_data()
