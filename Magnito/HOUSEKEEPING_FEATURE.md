# 🧹 Housekeeping Feature

## Overview
Complete housekeeping management system with before/after picture documentation for cleaning tasks.

## Features

### 1. **Housekeeping Dashboard Card**
- Shows active housekeeping tasks count
- Displays pending tasks count
- Quick link to start new task
- Located on main dashboard with gradient styling

### 2. **Task Creation**
- Select area type:
  - Machine
  - Mould
  - Factory Floor
  - Storage Area
  - Workstation
  - Other
- Describe specific area (e.g., "Machine #5", "Mould Storage")
- Upload **before picture** 📸
- Add before notes describing condition
- Automatically starts task and sets status to "In Progress"

### 3. **Task Completion**
- Upload **after picture** ✨
- Add after notes describing cleaned condition
- List cleaning products used
- Document any issues found during cleaning
- Automatically calculates task duration
- Sets status to "Completed"

### 4. **Task Tracking**
- Unique task numbers (HK-00001, HK-00002, etc.)
- Status tracking: Pending → In Progress → Completed
- Time tracking (started, completed, duration)
- Assigned user tracking
- Before/after picture comparison

### 5. **Task List View**
- Summary cards showing:
  - Pending tasks count
  - In Progress tasks count
  - Completed tasks count
- Grid view of all tasks with:
  - Task number and area type
  - Area description
  - Assigned user
  - Status badges
  - Before/after picture indicators
  - Quick action buttons

### 6. **Task Detail View**
- Complete task information
- Side-by-side before/after picture comparison
- Time tracking details
- Cleaning products used
- Issues found during cleaning
- Complete button for in-progress tasks

## URLs

- **List**: `/housekeeping/`
- **Create**: `/housekeeping/create/`
- **Detail**: `/housekeeping/<id>/`
- **Complete**: `/housekeeping/<id>/complete/`

## Navigation

Added to main navigation menu between "Issues" and "Job Cards"

## Database Model

**HousekeepingTask**
- `task_number` - Unique identifier (auto-generated)
- `area_type` - Type of area being cleaned
- `area_description` - Specific area description
- `before_image` - Picture before cleaning
- `before_notes` - Condition notes before
- `after_image` - Picture after cleaning
- `after_notes` - Condition notes after
- `status` - Pending/In Progress/Completed
- `assigned_to` - User assigned to task
- `started_at` - When task started
- `completed_at` - When task completed
- `cleaning_products_used` - Products used
- `issues_found` - Any issues discovered
- `created_at` - Task creation time
- `updated_at` - Last update time

## Workflow

1. **Start Task**
   - Click "Start New Housekeeping Task" from dashboard or list
   - Select area type and describe location
   - Take and upload before picture
   - Add notes about current condition
   - Submit to start task (status: In Progress)

2. **Perform Cleaning**
   - Clean the area using appropriate products
   - Note any issues discovered
   - Take after picture when done

3. **Complete Task**
   - Click "Complete Task" button
   - Upload after picture
   - Add notes about cleaned condition
   - List cleaning products used
   - Document any issues found
   - Submit to complete (status: Completed)

## Benefits

- **Visual Documentation**: Before/after pictures provide clear evidence of work done
- **Accountability**: Track who cleaned what and when
- **Quality Control**: Verify cleaning standards are met
- **Issue Discovery**: Document problems found during cleaning
- **Time Tracking**: Monitor how long cleaning tasks take
- **Product Tracking**: Record which cleaning products are effective
- **Compliance**: Maintain records for audits and inspections

## Styling

- Modern gradient cards with animations
- Green gradient for housekeeping card (🧹)
- Color-coded status badges
- Side-by-side before/after comparison
- Responsive grid layouts
- Emoji icons for visual appeal

## Integration

- Integrated with main dashboard
- Uses same authentication system
- Follows same design patterns as other features
- Admin panel integration for management
