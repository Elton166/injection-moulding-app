# Quick Start Guide

## Installation Steps

### 1. Install Python
Make sure you have Python 3.8 or higher installed:
```bash
python --version
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Load Sample Data
```bash
python setup.py
```

This will create:
- Admin user (username: `admin`, password: `admin123`)
- Sample moulds
- Troubleshooting guides
- Defect types with fix instructions

### 7. Run Development Server
```bash
python manage.py runserver
```

### 8. Access the Application
- Main App: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

## Features Overview

### 1. Dashboard
- View active moulds count
- See pending mould changes
- Monitor open issues
- Quick access to all features

### 2. Mould Changes
- Schedule mould changes
- Track change status (Planned → In Progress → Completed)
- Record start and end times
- Add notes for each change

### 3. Troubleshooting
- Browse common issues and solutions
- Log new issues
- Track resolution status
- View step-by-step fix instructions

### 4. Hourly Checklist
- Submit operator checklists every hour
- Quality checks (visual, dimensional, color, surface)
- Machine checks (temperature, pressure, cycle time)
- Material checks (level, drying)
- Flag issues for follow-up

### 5. Master Sample Management
- Upload master sample images
- Store specifications and tolerances
- Link samples to specific moulds
- Track sample history

### 6. Product Comparison
- Upload product images
- Automatic comparison with master sample
- Similarity score calculation (0-100%)
- Defect detection
- Automatic fix instructions based on defects

### 7. Defect Types Reference
- Browse common defect types
- View causes and symptoms
- Get detailed fix instructions
- Machine adjustment recommendations

## Usage Workflow

### Daily Operations

1. **Start of Shift**
   - Check dashboard for pending changes
   - Review any open issues

2. **Hourly Checks**
   - Submit hourly checklist
   - Perform all quality, machine, and material checks
   - Flag any issues found

3. **Mould Changes**
   - Schedule change in advance
   - Update status when starting
   - Mark as completed when done

4. **Quality Control**
   - Upload master sample for new products
   - Compare production samples regularly
   - Follow fix instructions if defects found

5. **Issue Management**
   - Log issues immediately when found
   - Reference troubleshooting guides
   - Mark as resolved when fixed

## Image Comparison Feature

The system uses computer vision to compare product images with master samples:

1. **Upload Master Sample**
   - Take clear, well-lit photo
   - Upload through Master Samples section
   - Add specifications and tolerances

2. **Compare Product**
   - Take photo of product in same lighting/angle
   - Select master sample to compare against
   - System automatically analyzes

3. **Review Results**
   - Similarity score (95%+ = good match)
   - Defect areas highlighted
   - Automatic fix instructions provided
   - Machine adjustment recommendations

## Tips for Best Results

### Image Comparison
- Use consistent lighting
- Same camera angle for master and product
- Clear, focused images
- Similar background
- Fill frame with product

### Troubleshooting
- Check common issues first
- Follow fix instructions step by step
- Document what worked
- Log all issues for tracking

### Checklists
- Complete every hour
- Be thorough with checks
- Add detailed notes
- Flag issues immediately

## Admin Panel Features

Access at http://localhost:8000/admin with admin credentials:

- Manage moulds
- Add/edit troubleshooting guides
- Create defect types
- View all logs and history
- Manage users and permissions

## Customization

### Adding New Defect Types
1. Go to Admin Panel
2. Click "Defect Types"
3. Add new defect with:
   - Name
   - Description
   - Common causes
   - Fix instructions
   - Machine adjustments

### Adding Troubleshooting Guides
1. Go to Admin Panel
2. Click "Troubleshooting Issues"
3. Add new issue with:
   - Title and category
   - Description
   - Symptoms
   - Solution steps
   - Prevention tips

## Support

For issues or questions:
1. Check troubleshooting guides in the app
2. Review defect types reference
3. Contact system administrator

## Security Notes

- Change default admin password immediately
- Create individual user accounts for operators
- Regular backups of database
- Keep SECRET_KEY secure in production
- Use HTTPS in production environment
