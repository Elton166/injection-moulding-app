# Comprehensive Injection Moulding Troubleshooting Database

## Overview
Complete troubleshooting database based on industry-standard injection moulding troubleshooting charts and best practices.

## Database Contents

### 17 Detailed Troubleshooting Issues

#### Quality Issues (11)
1. **Short Shot (Incomplete Fill)**
   - Symptoms, causes, and 10-step solution
   - Machine parameter adjustments
   - Prevention strategies

2. **Flash (Excess Material)**
   - Parting line issues
   - Clamp tonnage solutions
   - Mould maintenance

3. **Sink Marks**
   - Packing pressure optimization
   - Cooling time adjustments
   - Design recommendations

4. **Warpage (Part Distortion)**
   - Cooling balance
   - Temperature control
   - Stress reduction

5. **Flow Marks (Weld Lines)**
   - Injection speed optimization
   - Temperature adjustments
   - Venting improvements

6. **Burn Marks (Dieseling)**
   - Venting solutions
   - Speed and temperature reduction
   - Material handling

7. **Weld Lines (Knit Lines)**
   - Gate optimization
   - Temperature increases
   - Venting at weld lines

8. **Jetting (Worm Tracks)**
   - Gate design changes
   - Speed profile optimization
   - Flow control

9. **Splay Marks (Silver Streaks)**
   - Material drying procedures
   - Moisture control
   - Temperature reduction

10. **Brittleness (Weak Parts)**
    - Material degradation prevention
    - Processing optimization
    - Quality control

11. **Delamination (Layer Separation)**
    - Material compatibility
    - Temperature control
    - Contamination prevention

12. **Voids and Air Bubbles**
    - Packing optimization
    - Venting improvements
    - Material drying

13. **Color Streaks and Variations**
    - Mixing optimization
    - Colorant selection
    - Equipment cleaning

14. **Surface Defects (Blemishes)**
    - Mould maintenance
    - Temperature control
    - Surface finish optimization

#### Machine Issues (1)
15. **Inconsistent Shot Size**
    - Hydraulic system checks
    - Screw and barrel inspection
    - Calibration procedures

#### Material Issues (1)
16. **Material Degradation**
    - Temperature control
    - Residence time management
    - Material quality

#### Mould Issues (1)
17. **Mould Sticking**
    - Ejection system optimization
    - Draft angle requirements
    - Release agent usage

### 10 Comprehensive Defect Types

Each defect type includes:
- **Description**: Clear explanation of the defect
- **Common Causes**: List of typical root causes
- **Fix Instructions**: 10-step detailed solution
- **Machine Adjustments**: Specific parameter changes with values
- **Prevention**: Long-term prevention strategies

1. Short Shot
2. Flash
3. Sink Marks
4. Warpage
5. Flow Marks
6. Burn Marks
7. Weld Lines
8. Jetting
9. Splay Marks
10. Brittleness

## Features

### Troubleshooting Chart View
- **Comprehensive Display**: All issues in one scrollable page
- **Category Filtering**: Filter by Quality, Machine, Material, or Mould
- **Print-Friendly**: Optimized for printing as reference guide
- **Color-Coded Sections**: 
  - Blue: Description
  - Yellow: Symptoms
  - Green: Solutions
  - Cyan: Prevention

### Information Included

#### For Each Issue:
1. **Title**: Clear defect name
2. **Category**: Quality/Machine/Material/Mould
3. **Description**: What the defect is
4. **Symptoms**: Observable signs (bullet points)
5. **Solution**: 10-step detailed fix procedure
6. **Prevention**: Long-term prevention strategies

#### Machine Parameter Adjustments:
- Injection Pressure (% changes)
- Melt Temperature (°C changes)
- Injection Speed (% changes)
- Cooling Time (% or time changes)
- Packing Pressure (% changes)
- Mould Temperature (°C changes)
- Screw Speed (% changes)
- Back Pressure (% changes)

## Access Points

### URLs
- **Troubleshooting List**: http://localhost:8000/troubleshooting/
- **Troubleshooting Chart**: http://localhost:8000/troubleshooting/chart/
- **Individual Issue**: http://localhost:8000/troubleshooting/{id}/
- **Defect Types**: http://localhost:8000/defect-types/

### Navigation
- Main menu → Troubleshooting
- Click "📊 View Troubleshooting Chart" for comprehensive view
- Click individual issues for detailed solutions

## Usage

### Quick Reference
1. Navigate to Troubleshooting Chart
2. Use category filters to narrow down
3. Find your defect
4. Follow step-by-step solutions
5. Apply machine adjustments
6. Implement prevention strategies

### Logging Issues
1. Click "➕ Log New Issue"
2. Select troubleshooting issue type
3. Enter mould and machine details
4. Add description
5. Track resolution

### Printing
- Click "🖨️ Print Troubleshooting Chart"
- Optimized layout for printing
- Use as shop floor reference

## Industry Standards

Based on:
- ASTM injection moulding standards
- SPE (Society of Plastics Engineers) guidelines
- Industry best practices
- Manufacturer troubleshooting guides
- Quality control standards

## Parameter Ranges

### Typical Adjustments:
- **Injection Pressure**: ±5-15%
- **Melt Temperature**: ±10-20°C
- **Injection Speed**: ±10-30%
- **Cooling Time**: ±20-30%
- **Packing Pressure**: ±10-20%
- **Mould Temperature**: ±5-15°C

### Safety Notes:
- Make adjustments incrementally
- Document all changes
- Monitor part quality after each adjustment
- Stay within material specifications
- Consult material data sheets

## Benefits

✅ **Comprehensive**: 17 issues + 10 defect types
✅ **Detailed**: 10-step solutions for each
✅ **Practical**: Specific parameter adjustments
✅ **Preventive**: Long-term prevention strategies
✅ **Accessible**: Easy-to-use interface
✅ **Printable**: Shop floor reference
✅ **Searchable**: Quick issue lookup
✅ **Professional**: Industry-standard solutions

## Setup

Database created with:
```bash
python setup_troubleshooting.py
```

This populates:
- TroubleshootingIssue model (17 issues)
- DefectType model (10 defects)

## Future Enhancements

Potential additions:
- Images/diagrams for each defect
- Video tutorials
- Interactive parameter calculator
- Material-specific troubleshooting
- Machine-specific guides
- Multi-language support
- Mobile app version
- QR codes for quick access

## Support

For additional troubleshooting:
1. Consult material data sheets
2. Contact material supplier
3. Review machine manual
4. Consult mould designer
5. Contact technical support
