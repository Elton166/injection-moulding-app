# Injection Moulding Management System

A Django-based application for managing injection moulding operations.

## Features

- Mould change tracking and management
- Troubleshooting system with common issues and solutions
- Operator hourly checklist
- Master sample upload and comparison
- Defect detection with fix instructions
- Image comparison for quality control

## Installation

1. Install Python 3.8 or higher
2. Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage

Access the application at http://localhost:8000
