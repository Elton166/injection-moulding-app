# Production Orders Feature

## Overview
Complete production order management system integrated into the "Pending Changes" card on the dashboard.

## What's New

### Production Order Model
Tracks:
- Order number and product name
- Customer name and contact
- Mould to be used
- Quantity ordered vs produced
- Priority levels (Urgent, High, Normal, Low)
- Status (Pending, In Progress, Completed, Cancelled)
- Due dates with overdue tracking
- Special requirements and notes

### Dashboard Integration
The "Pending Orders" card now shows:
- Total pending orders count
- Number of urgent orders (🔥 badge)
- Link to create new orders
- Detailed cards for each pending order showing:
  - Product name and order number
  - Customer name
  - Mould required
  - Quantity needed
  - Priority badge with color coding
  - Due date with overdue warnings
  - Days until due for urgent items
  - Special requirements preview
  - Quick action buttons (View/Start)

### Priority System
**🔥 Urgent** - Red badge, highest priority
**⚡ High** - Orange badge
**✓ Normal** - Green badge
**📌 Low** - Gray badge

### Features

#### Create Production Order
- Order number (unique)
- Product name
- Select mould
- Customer information
- Quantity and unit
- Priority level
- Order and due dates
- Special requirements
- Notes

#### Order Management
- View all orders with status
- Filter by status (Pending/In Progress/Completed)
- Progress tracking (% complete)
- Update status (Start/Complete)
- Overdue detection
- Days until due calculation

#### Dashboard Display
- Shows only pending orders
- Sorted by priority then due date
- Color-coded priority badges
- Overdue warnings
- Urgent order count
- Quick actions

## URLs

| Page | URL |
|------|-----|
| Production Orders List | http://localhost:8000/production-orders/ |
| Create Order | http://localhost:8000/production-orders/create/ |
| Order Detail | http://localhost:8000/production-orders/{id}/ |
| Update Status | http://localhost:8000/production-orders/{id}/status/{status}/ |

## Usage

### Creating an Order
1. Dashboard → Click "➕ New Order" on Pending Orders card
2. Or Navigation → Production Orders → ➕ New Order
3. Fill in:
   - Order number (e.g., "PO-2026-001")
   - Product name
   - Select mould
   - Customer name and contact
   - Quantity and unit (pieces, kg, etc.)
   - Priority (Urgent/High/Normal/Low)
   - Order date and due date
   - Special requirements (optional)
   - Notes (optional)
4. Click "✅ Create Order"

### Managing Orders
1. **View All**: Navigation → Production Orders
2. **Start Production**: Click "▶️ Start" button
3. **Complete Order**: Click "✅ Complete" when done
4. **View Details**: Click "View" for full information

### Dashboard View
- Pending orders shown in colorful cards
- Urgent orders highlighted with 🔥 badge
- Overdue orders marked with red "OVERDUE" badge
- Orders due soon show countdown (e.g., "3 days")
- Click "View All Orders →" to see complete list

## Priority Colors
- **Urgent**: #dc3545 (Red)
- **High**: #fd7e14 (Orange)
- **Normal**: #28a745 (Green)
- **Low**: #6c757d (Gray)

## Status Flow
1. **Pending** → Order created, waiting to start
2. **In Progress** → Production started
3. **Completed** → Order finished
4. **Cancelled** → Order cancelled

## Features
✅ Priority-based sorting
✅ Overdue detection
✅ Progress tracking
✅ Customer management
✅ Mould assignment
✅ Special requirements tracking
✅ Due date warnings
✅ Funky gradient design
✅ Mobile responsive cards
✅ Quick action buttons

## Integration
- Replaces "Pending Changes" card
- Shows in main navigation
- Integrated with mould system
- Links to mould runs
- Admin panel support

## Database
New table: `moulding_productionorder`
- Tracks all production orders
- Linked to Mould model
- Progress calculation
- Automatic date tracking
