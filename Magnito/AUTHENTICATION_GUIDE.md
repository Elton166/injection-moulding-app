# Authentication System Guide

## Overview
Multi-level authentication system with Company and Employee (Manager/Supervisor/Operator) roles.

## System Flow

### 1. Company Registration & Login
**Companies** are the top-level entities that manage all employees.

#### Register a Company
1. Go to: http://localhost:8000/auth/
2. Click "📝 Register Company"
3. Fill in:
   - Company Name
   - Email
   - Phone (optional)
   - Address (optional)
   - Registration Number (optional)
   - Username (for login)
   - Password
   - Confirm Password
4. Click "✅ Register Company"
5. Automatically logged in to Company Dashboard

#### Login as Company
1. Go to: http://localhost:8000/auth/
2. Click "🔐 Company Login"
3. Enter:
   - Username
   - Password
4. Access Company Dashboard

### 2. Company Dashboard
After company login, you can:
- View all employees (Managers, Supervisors, Operators)
- Add new Managers/Supervisors
- View company statistics
- Access main application dashboard

### 3. Add Manager/Supervisor
**Only companies can create Manager/Supervisor accounts**

1. Login as Company
2. Go to Company Dashboard
3. Click "➕ Add Manager/Supervisor"
4. Fill in:
   - **Personal Info**: First Name, Last Name, Email
   - **Employment**: Role (Manager/Supervisor), Employee ID, Department, Phone
   - **Login**: Username, Password, Confirm Password
5. Click "✅ Add Employee"

### 4. Employee Login
Managers, Supervisors, and Operators login here:

1. Go to: http://localhost:8000/auth/
2. Click "🔑 Employee Login"
3. Enter:
   - Username
   - Password
4. Access Main Dashboard

## User Roles

### 🏢 Company
- Top-level account
- Can create Managers and Supervisors
- Manages all employees
- Access to Company Dashboard

### 👔 Manager
- Created by Company
- Full access to operations
- Can manage production

### 👨‍💼 Supervisor
- Created by Company
- Supervises operations
- Can monitor and report

### 👷 Operator
- Basic production access
- Can submit checklists
- Can log issues

## URLs

| Page | URL |
|------|-----|
| Login Home | http://localhost:8000/auth/ |
| Company Register | http://localhost:8000/auth/company/register/ |
| Company Login | http://localhost:8000/auth/company/login/ |
| Company Dashboard | http://localhost:8000/auth/company/dashboard/ |
| Add Employee | http://localhost:8000/auth/employee/register/ |
| Employee Login | http://localhost:8000/auth/user/login/ |
| Logout | http://localhost:8000/auth/logout/ |
| Main Dashboard | http://localhost:8000/ |

## Features

### Company Features
✅ Register and manage company profile
✅ Create Manager and Supervisor accounts
✅ View all employees
✅ Track employee roles and departments
✅ Company-specific dashboard

### Employee Features
✅ Secure login system
✅ Role-based access (Manager/Supervisor/Operator)
✅ Personal profiles with employee ID
✅ Department assignment
✅ Access to main application features

## Database Models

### Company
- name, email, phone, address
- registration_number
- username, password_hash
- is_active, created_at

### UserProfile
- Links to Django User
- company (ForeignKey)
- role (manager/supervisor/operator)
- employee_id, phone, department
- is_active, created_at

## Security Features
- Password hashing for companies
- Django authentication for employees
- Session-based authentication
- Role-based access control
- Company-employee relationship enforcement

## Quick Start

1. **Start Server**: `python manage.py runserver`
2. **Register Company**: http://localhost:8000/auth/ → Register Company
3. **Add Employees**: Company Dashboard → Add Manager/Supervisor
4. **Employee Login**: http://localhost:8000/auth/ → Employee Login
5. **Start Working**: Access all moulding features!

## Notes
- Companies must be registered before employees can be created
- Only companies can create Manager/Supervisor accounts
- Operators can be added later (future feature)
- All employees are linked to their company
- Session data tracks user role and company
