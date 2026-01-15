"""
Comprehensive Injection Moulding Troubleshooting Database
Based on industry-standard troubleshooting charts
Run: python setup_troubleshooting.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'injection_moulding.settings')
django.setup()

from moulding.models import TroubleshootingIssue, DefectType

def create_troubleshooting_data():
    print("Creating comprehensive troubleshooting database...")
    
    # Comprehensive troubleshooting issues
    issues = [
        # QUALITY ISSUES - SHORT SHOTS
        {
            'title': 'Short Shot (Incomplete Fill)',
            'category': 'quality',
            'description': 'Part is not completely filled, missing sections or incomplete features',
            'symptoms': '''- Part is incomplete with missing sections
- Thin or weak areas in the part
- Unfilled cavities or features
- Part weight is less than expected
- Visible flow lines stopping before completion''',
            'solution': '''1. Increase injection pressure (5-10% increments)
2. Increase injection speed
3. Raise melt temperature (10-15°C)
4. Increase mould temperature
5. Extend injection time
6. Check for material blockage in nozzle or gates
7. Verify adequate material supply in hopper
8. Increase gate size if possible
9. Check for air traps and improve venting
10. Reduce clamp tonnage if excessive''',
            'prevention': '''- Regular nozzle and hot runner maintenance
- Proper material drying and handling
- Consistent temperature control
- Adequate venting design
- Proper gate sizing and location'''
        },
        
        # FLASH
        {
            'title': 'Flash (Excess Material)',
            'category': 'quality',
            'description': 'Excess material escaping at parting line or other mould openings',
            'symptoms': '''- Thin material at parting line
- Excess material on part edges
- Rough edges requiring trimming
- Material between mould halves
- Inconsistent part dimensions''',
            'solution': '''1. Reduce injection pressure (5-10%)
2. Reduce injection speed
3. Lower melt temperature (10-15°C)
4. Increase clamp tonnage
5. Reduce cushion size
6. Check and repair mould parting line
7. Verify mould alignment
8. Inspect for worn mould surfaces
9. Reduce packing pressure
10. Check for contamination on parting line''',
            'prevention': '''- Regular mould maintenance and cleaning
- Proper clamp tonnage calculation
- Controlled injection parameters
- Mould surface inspection
- Proper mould alignment procedures'''
        },
        
        # SINK MARKS
        {
            'title': 'Sink Marks',
            'category': 'quality',
            'description': 'Depressions or indentations on part surface, usually opposite thick sections',
            'symptoms': '''- Visible depressions on surface
- Surface irregularities
- Uneven appearance
- Dimples opposite ribs or bosses
- Reduced part aesthetics''',
            'solution': '''1. Increase packing pressure (10-15%)
2. Extend packing time (1-2 seconds)
3. Reduce melt temperature (10-20°C)
4. Increase cooling time
5. Optimize gate location closer to thick sections
6. Reduce wall thickness variations
7. Add ribs or gussets for support
8. Increase injection speed
9. Improve cooling channel design
10. Use gas-assist moulding for thick sections''',
            'prevention': '''- Uniform wall thickness design
- Proper cooling system design
- Adequate packing pressure
- Optimized gate location
- Material selection for low shrinkage'''
        },
        
        # WARPAGE
        {
            'title': 'Warpage (Part Distortion)',
            'category': 'quality',
            'description': 'Part bends, twists, or distorts after ejection',
            'symptoms': '''- Part does not sit flat
- Twisted or bent appearance
- Dimensional instability
- Assembly problems
- Stress marks visible''',
            'solution': '''1. Optimize cooling system for uniform cooling
2. Reduce melt temperature (10-20°C)
3. Adjust packing pressure and time
4. Increase cooling time (20-30%)
5. Check mould temperature uniformity
6. Reduce injection speed
7. Optimize gate location
8. Adjust ejection system
9. Use annealing process
10. Check for uneven wall thickness''',
            'prevention': '''- Balanced cooling design
- Uniform wall thickness
- Proper material selection
- Controlled ejection
- Symmetrical gate placement'''
        },
        
        # FLOW MARKS
        {
            'title': 'Flow Marks (Weld Lines)',
            'category': 'quality',
            'description': 'Wavy lines or patterns on part surface showing flow direction',
            'symptoms': '''- Visible lines on surface
- Wavy patterns
- Color variations
- Dull streaks
- Reduced surface quality''',
            'solution': '''1. Increase injection speed (10-20%)
2. Raise melt temperature (10-15°C)
3. Increase mould temperature (5-10°C)
4. Improve mould venting
5. Optimize gate location
6. Increase injection pressure
7. Reduce wall thickness
8. Polish mould surface
9. Use hot runner system
10. Adjust material drying''',
            'prevention': '''- Proper gate design and location
- Adequate venting
- Controlled injection speed
- Proper mould temperature
- Material drying procedures'''
        },
        
        # BURN MARKS
        {
            'title': 'Burn Marks (Dieseling)',
            'category': 'quality',
            'description': 'Black or brown discoloration on part surface',
            'symptoms': '''- Black or brown marks
- Burnt smell
- Discoloration at end of fill
- Charred material
- Surface degradation''',
            'solution': '''1. Improve mould venting
2. Reduce injection speed
3. Lower melt temperature (10-15°C)
4. Reduce back pressure
5. Clean mould vents
6. Reduce screw speed
7. Check for material degradation
8. Increase gate size
9. Reduce cycle time
10. Use proper material grade''',
            'prevention': '''- Adequate venting design
- Proper temperature control
- Material handling procedures
- Regular vent cleaning
- Controlled injection parameters'''
        },
        
        # WELD LINES
        {
            'title': 'Weld Lines (Knit Lines)',
            'category': 'quality',
            'description': 'Visible lines where two flow fronts meet',
            'symptoms': '''- Visible lines on surface
- Weak spots in part
- Color difference at line
- Reduced strength
- Surface imperfection''',
            'solution': '''1. Increase melt temperature (15-20°C)
2. Increase mould temperature (10-15°C)
3. Increase injection speed
4. Increase injection pressure
5. Relocate gates to minimize weld lines
6. Improve venting at weld line area
7. Use sequential valve gating
8. Increase wall thickness at weld line
9. Add ribs for reinforcement
10. Polish mould surface''',
            'prevention': '''- Optimal gate placement
- Proper venting design
- Adequate temperature control
- Material selection
- Part design optimization'''
        },
        
        # JETTING
        {
            'title': 'Jetting (Worm Tracks)',
            'category': 'quality',
            'description': 'Snake-like flow pattern on part surface',
            'symptoms': '''- Worm-like marks
- Squiggly lines
- Surface imperfections
- Uneven appearance
- Flow disturbance marks''',
            'solution': '''1. Reduce injection speed initially
2. Increase gate size
3. Relocate gate position
4. Increase melt temperature (10-15°C)
5. Increase mould temperature
6. Use fan gate instead of pin gate
7. Implement multi-stage injection
8. Increase wall thickness near gate
9. Add flow leaders
10. Optimize runner design''',
            'prevention': '''- Proper gate design and sizing
- Controlled injection profile
- Adequate wall thickness
- Material temperature control
- Gate location optimization'''
        },
        
        # SPLAY MARKS
        {
            'title': 'Splay Marks (Silver Streaks)',
            'category': 'quality',
            'description': 'Silver or white streaks radiating from gate',
            'symptoms': '''- Silver streaks on surface
- White marks
- Moisture-related defects
- Radiating patterns from gate
- Surface quality issues''',
            'solution': '''1. Dry material properly (check moisture content)
2. Reduce melt temperature (10-15°C)
3. Reduce back pressure
4. Reduce screw speed
5. Check for material contamination
6. Reduce injection speed
7. Increase mould temperature
8. Clean hopper and barrel
9. Use material with lower moisture absorption
10. Check for air entrapment''',
            'prevention': '''- Proper material drying (follow resin specs)
- Material storage in dry conditions
- Regular hopper cleaning
- Moisture content testing
- Proper material handling'''
        },
        
        # BRITTLENESS
        {
            'title': 'Brittleness (Weak Parts)',
            'category': 'quality',
            'description': 'Parts break or crack easily under stress',
            'symptoms': '''- Parts crack easily
- Low impact strength
- Brittle failure
- Reduced toughness
- Stress cracking''',
            'solution': '''1. Reduce melt temperature (material degradation)
2. Reduce residence time in barrel
3. Increase packing pressure
4. Extend packing time
5. Check for material contamination
6. Verify correct material grade
7. Reduce regrind percentage
8. Increase cooling time
9. Check for moisture in material
10. Optimize gate location''',
            'prevention': '''- Proper material selection
- Controlled processing temperatures
- Limited regrind usage
- Material quality control
- Proper drying procedures'''
        },
        
        # DELAMINATION
        {
            'title': 'Delamination (Layer Separation)',
            'category': 'quality',
            'description': 'Layers of material separate or peel apart',
            'symptoms': '''- Layers peeling apart
- Flaking surface
- Weak bonding between layers
- Visible separation
- Reduced strength''',
            'solution': '''1. Increase melt temperature (15-20°C)
2. Increase mould temperature
3. Increase injection pressure
4. Reduce moisture in material
5. Check for contamination
6. Increase packing pressure
7. Extend packing time
8. Verify material compatibility
9. Clean mould surface
10. Check for incompatible regrind''',
            'prevention': '''- Proper material drying
- Material compatibility verification
- Clean processing equipment
- Controlled regrind usage
- Quality material sourcing'''
        },
        
        # VOIDS/BUBBLES
        {
            'title': 'Voids and Air Bubbles',
            'category': 'quality',
            'description': 'Air pockets or voids inside the part',
            'symptoms': '''- Internal voids visible
- Air bubbles in part
- Weak spots
- Reduced density
- Part weight variations''',
            'solution': '''1. Increase packing pressure (15-20%)
2. Extend packing time
3. Reduce melt temperature
4. Increase injection speed
5. Improve venting
6. Reduce moisture in material
7. Optimize gate location
8. Increase cooling time
9. Reduce wall thickness
10. Check for gas generation''',
            'prevention': '''- Adequate packing pressure
- Proper material drying
- Good venting design
- Controlled processing
- Material quality control'''
        },
        
        # COLOR STREAKS
        {
            'title': 'Color Streaks and Variations',
            'category': 'quality',
            'description': 'Uneven color distribution or streaking',
            'symptoms': '''- Color inconsistency
- Streaks in part
- Uneven pigment distribution
- Color variations
- Mottled appearance''',
            'solution': '''1. Increase back pressure for better mixing
2. Increase screw speed
3. Extend residence time
4. Check colorant compatibility
5. Increase melt temperature (5-10°C)
6. Use better dispersion colorant
7. Clean barrel and screw
8. Increase mixing section length
9. Reduce injection speed
10. Check for contamination''',
            'prevention': '''- Proper colorant selection
- Adequate mixing
- Clean equipment
- Consistent material feed
- Quality colorant dispersion'''
        },
        
        # SURFACE DEFECTS
        {
            'title': 'Surface Defects (Blemishes)',
            'category': 'quality',
            'description': 'Various surface imperfections and blemishes',
            'symptoms': '''- Surface roughness
- Scratches or marks
- Dull finish
- Orange peel texture
- Surface contamination''',
            'solution': '''1. Polish mould surface
2. Increase mould temperature (10-15°C)
3. Increase injection speed
4. Raise melt temperature (10°C)
5. Clean mould thoroughly
6. Check for mould damage
7. Improve venting
8. Use mould release agent
9. Reduce ejection force
10. Check material quality''',
            'prevention': '''- Regular mould maintenance
- Proper mould cleaning
- Quality material usage
- Controlled ejection
- Mould surface protection'''
        },
        
        # MACHINE ISSUES
        {
            'title': 'Inconsistent Shot Size',
            'category': 'machine',
            'description': 'Variation in shot weight or volume',
            'symptoms': '''- Weight variations
- Inconsistent fill
- Part-to-part differences
- Cushion variations
- Process instability''',
            'solution': '''1. Check hydraulic system pressure
2. Verify screw check valve operation
3. Inspect barrel and screw wear
4. Check material feed consistency
5. Verify temperature control
6. Calibrate injection unit
7. Check for air in hydraulic system
8. Inspect hopper level sensor
9. Verify material flow
10. Check for contamination''',
            'prevention': '''- Regular machine maintenance
- Screw and barrel inspection
- Hydraulic system checks
- Material handling consistency
- Preventive maintenance schedule'''
        },
        
        # MATERIAL ISSUES
        {
            'title': 'Material Degradation',
            'category': 'material',
            'description': 'Material breaks down due to excessive heat or time',
            'symptoms': '''- Discoloration
- Burnt smell
- Reduced properties
- Brittleness
- Surface defects''',
            'solution': '''1. Reduce barrel temperature (15-20°C)
2. Reduce residence time
3. Purge barrel regularly
4. Check for hot spots
5. Reduce screw speed
6. Lower back pressure
7. Verify material grade
8. Check for contamination
9. Reduce cycle time
10. Use heat stabilizers''',
            'prevention': '''- Proper temperature control
- Minimize residence time
- Regular purging
- Material quality control
- Proper material selection'''
        },
        
        # MOULD ISSUES
        {
            'title': 'Mould Sticking',
            'category': 'mould',
            'description': 'Parts stick to mould and difficult to eject',
            'symptoms': '''- Difficult ejection
- Part damage during ejection
- Ejector pin marks
- Part deformation
- Increased cycle time''',
            'solution': '''1. Reduce mould temperature
2. Increase cooling time
3. Add draft angles
4. Polish mould surface
5. Use mould release agent
6. Check ejection system
7. Increase ejector pin size/number
8. Reduce packing pressure
9. Verify proper venting
10. Check for undercuts''',
            'prevention': '''- Adequate draft angles in design
- Proper mould maintenance
- Controlled mould temperature
- Regular cleaning
- Proper ejection system design'''
        },
    ]
    
    for issue_data in issues:
        TroubleshootingIssue.objects.get_or_create(
            title=issue_data['title'],
            defaults=issue_data
        )
    
    print(f"✓ Created {len(issues)} troubleshooting issues")
    
    # Comprehensive defect types
    defects = [
        {
            'name': 'Short Shot',
            'description': 'Incomplete filling of mould cavity',
            'common_causes': '''- Insufficient injection pressure
- Low material temperature
- Inadequate injection speed
- Material blockage
- Insufficient material supply
- Poor venting
- Gate too small''',
            'fix_instructions': '''1. Increase injection pressure by 5-10%
2. Raise melt temperature by 10-15°C
3. Increase injection speed by 10-20%
4. Check and clear any blockages in nozzle/gates
5. Verify adequate material in hopper
6. Improve mould venting
7. Consider increasing gate size
8. Extend injection time
9. Check for air traps
10. Reduce clamp tonnage if excessive''',
            'machine_adjustments': '''Injection Pressure: +5-10%
Melt Temperature: +10-15°C
Injection Speed: +10-20%
Injection Time: +0.5-1.0 sec
Screw Speed: Maintain or slight increase'''
        },
        {
            'name': 'Flash',
            'description': 'Excess material at parting line',
            'common_causes': '''- Excessive injection pressure
- Worn mould surfaces
- Insufficient clamp tonnage
- High material temperature
- Mould misalignment
- Contamination on parting line''',
            'fix_instructions': '''1. Reduce injection pressure by 5-10%
2. Lower melt temperature by 10-15°C
3. Increase clamp tonnage
4. Inspect and repair mould parting line
5. Check mould alignment
6. Clean parting line surfaces
7. Reduce packing pressure
8. Decrease cushion size
9. Check for mould wear
10. Verify proper mould closure''',
            'machine_adjustments': '''Injection Pressure: -5-10%
Melt Temperature: -10-15°C
Clamp Tonnage: Increase as needed
Packing Pressure: -10-15%
Cushion: Reduce by 2-3mm'''
        },
        {
            'name': 'Sink Marks',
            'description': 'Surface depressions opposite thick sections',
            'common_causes': '''- Insufficient packing pressure
- Inadequate cooling time
- Thick wall sections
- Poor gate location
- Low packing time
- High melt temperature''',
            'fix_instructions': '''1. Increase packing pressure by 10-15%
2. Extend packing time by 1-2 seconds
3. Reduce melt temperature by 10-20°C
4. Increase cooling time by 20-30%
5. Optimize gate location near thick sections
6. Review part design for uniform wall thickness
7. Add ribs or gussets for support
8. Increase injection speed
9. Improve cooling channel design
10. Consider gas-assist moulding''',
            'machine_adjustments': '''Packing Pressure: +10-15%
Packing Time: +1-2 sec
Melt Temperature: -10-20°C
Cooling Time: +20-30%
Mould Temperature: Optimize for uniform cooling'''
        },
        {
            'name': 'Warpage',
            'description': 'Part distortion or bending',
            'common_causes': '''- Uneven cooling
- High melt temperature
- Residual stress
- Uneven wall thickness
- Poor ejection
- Improper packing''',
            'fix_instructions': '''1. Balance cooling channels for uniform cooling
2. Reduce melt temperature by 10-20°C
3. Adjust packing pressure and profile
4. Increase cooling time by 20-30%
5. Check mould temperature uniformity
6. Reduce injection speed
7. Optimize gate location for balanced flow
8. Adjust ejection system
9. Use annealing process post-moulding
10. Review part design for uniform walls''',
            'machine_adjustments': '''Melt Temperature: -10-20°C
Cooling Time: +20-30%
Packing Pressure: Adjust for balance
Mould Temperature: Uniform across cavities
Ejection: Optimize timing and force'''
        },
        {
            'name': 'Flow Marks',
            'description': 'Wavy lines showing flow direction',
            'common_causes': '''- Low injection speed
- Cold material temperature
- Poor venting
- Cold mould temperature
- Small gates
- Long flow length''',
            'fix_instructions': '''1. Increase injection speed by 10-20%
2. Raise melt temperature by 10-15°C
3. Increase mould temperature by 5-10°C
4. Improve mould venting
5. Optimize gate location and size
6. Increase injection pressure
7. Reduce wall thickness if possible
8. Polish mould surface
9. Use hot runner system
10. Check material drying''',
            'machine_adjustments': '''Injection Speed: +10-20%
Melt Temperature: +10-15°C
Mould Temperature: +5-10°C
Injection Pressure: +5-10%
Back Pressure: Slight increase for mixing'''
        },
        {
            'name': 'Burn Marks',
            'description': 'Black or brown discoloration',
            'common_causes': '''- Poor venting
- Excessive injection speed
- High melt temperature
- Air entrapment
- Material degradation
- Dieseling effect''',
            'fix_instructions': '''1. Improve mould venting immediately
2. Reduce injection speed by 10-15%
3. Lower melt temperature by 10-15°C
4. Reduce back pressure
5. Clean all mould vents
6. Reduce screw speed
7. Check for material degradation
8. Increase gate size
9. Reduce cycle time
10. Verify proper material grade''',
            'machine_adjustments': '''Injection Speed: -10-15%
Melt Temperature: -10-15°C
Back Pressure: -20-30%
Screw Speed: -10-15%
Cycle Time: Reduce if possible'''
        },
        {
            'name': 'Weld Lines',
            'description': 'Visible lines where flow fronts meet',
            'common_causes': '''- Multiple gates
- Flow around inserts
- Low melt temperature
- Low mould temperature
- Slow injection speed
- Poor venting at weld line''',
            'fix_instructions': '''1. Increase melt temperature by 15-20°C
2. Increase mould temperature by 10-15°C
3. Increase injection speed significantly
4. Increase injection pressure
5. Relocate gates to minimize weld lines
6. Improve venting at weld line location
7. Use sequential valve gating
8. Increase wall thickness at weld line
9. Add reinforcing ribs
10. Polish mould surface at weld line''',
            'machine_adjustments': '''Melt Temperature: +15-20°C
Mould Temperature: +10-15°C
Injection Speed: +20-30%
Injection Pressure: +10-15%
Venting: Critical at weld line areas'''
        },
        {
            'name': 'Jetting',
            'description': 'Snake-like flow pattern',
            'common_causes': '''- Excessive injection speed
- Small gate size
- Poor gate location
- Low melt temperature
- Direct gate into open cavity''',
            'fix_instructions': '''1. Reduce initial injection speed
2. Increase gate size
3. Relocate gate to side wall
4. Increase melt temperature by 10-15°C
5. Increase mould temperature
6. Use fan gate instead of pin gate
7. Implement multi-stage injection profile
8. Increase wall thickness near gate
9. Add flow leaders or deflectors
10. Optimize runner design''',
            'machine_adjustments': '''Injection Speed: Reduce initially, then ramp up
Melt Temperature: +10-15°C
Mould Temperature: +5-10°C
Injection Profile: Multi-stage
Gate Design: Increase size or change type'''
        },
        {
            'name': 'Splay Marks',
            'description': 'Silver streaks from moisture',
            'common_causes': '''- Moisture in material
- Material degradation
- Excessive melt temperature
- Contamination
- Air entrapment
- Volatile additives''',
            'fix_instructions': '''1. Dry material properly (follow resin specifications)
2. Reduce melt temperature by 10-15°C
3. Reduce back pressure
4. Reduce screw speed
5. Check for material contamination
6. Reduce injection speed
7. Increase mould temperature slightly
8. Clean hopper and barrel thoroughly
9. Use material with lower moisture absorption
10. Check for air entrapment in feed system''',
            'machine_adjustments': '''Material Drying: Critical - follow specs
Melt Temperature: -10-15°C
Back Pressure: -20-30%
Screw Speed: -10-15%
Residence Time: Minimize'''
        },
        {
            'name': 'Brittleness',
            'description': 'Parts break easily',
            'common_causes': '''- Material degradation
- Excessive temperature
- Long residence time
- Contamination
- Excessive regrind
- Moisture''',
            'fix_instructions': '''1. Reduce melt temperature to prevent degradation
2. Reduce residence time in barrel
3. Increase packing pressure
4. Extend packing time
5. Check for material contamination
6. Verify correct material grade
7. Reduce regrind percentage below 25%
8. Increase cooling time
9. Check for moisture in material
10. Optimize gate location for better packing''',
            'machine_adjustments': '''Melt Temperature: Reduce to lower range
Residence Time: Minimize
Packing Pressure: +10-15%
Packing Time: +1-2 sec
Regrind: Limit to 15-25% maximum'''
        },
    ]
    
    for defect_data in defects:
        DefectType.objects.get_or_create(
            name=defect_data['name'],
            defaults=defect_data
        )
    
    print(f"✓ Created {len(defects)} defect types")
    print("\n✅ Comprehensive troubleshooting database created!")
    print("\nDatabase includes:")
    print("- 17 detailed troubleshooting issues")
    print("- 10 comprehensive defect types")
    print("- Industry-standard solutions")
    print("- Machine adjustment parameters")
    print("- Prevention strategies")

if __name__ == '__main__':
    create_troubleshooting_data()
