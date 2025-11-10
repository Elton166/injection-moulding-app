# Quick Reference Card

## 🚀 Most Common Commands

### First Time Setup
```bash
# 1. Create virtual environment
python -m venv env

# 2. Activate it
env\Scripts\activate          # Windows
source env/bin/activate       # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
```

### Daily Development
```bash
# Activate virtual environment
env\Scripts\activate          # Windows
source env/bin/activate       # Linux/Mac

# Run server
python manage.py runserver

# Access application
# http://127.0.0.1:8000/
```

### Database Commands
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check database status
python docs/tests/check_db_status.py
```

### User Management
```bash
# Create superuser
python manage.py createsuperuser

# Access admin panel
# http://127.0.0.1:8000/admin/
```

## 📍 Important URLs

| Page | URL | Access |
|------|-----|--------|
| Home | http://127.0.0.1:8000/ | Public |
| Register | http://127.0.0.1:8000/register/ | Public |
| Login | http://127.0.0.1:8000/login/ | Public |
| Vendor Dashboard | http://127.0.0.1:8000/vendor/ | Vendors only |
| Admin Panel | http://127.0.0.1:8000/admin/ | Admin only |
| API Overview | http://127.0.0.1:8000/api/ | Public |
| Cart | http://127.0.0.1:8000/cart/ | All users |

## 👤 User Types

### Buyer
- Browse and search products
- Add items to cart
- Checkout and place orders
- Write product reviews

### Vendor
- Create and manage stores
- Add and edit products
- View sales statistics
- Manage inventory

### Admin
- Full system access
- User management
- Content moderation
- System configuration

## 🛒 Common Workflows

### Vendor: Selling Products
1. Register as Vendor
2. Login
3. Go to Vendor Dashboard
4. Create Store
5. Add Products
6. Products appear on home page

### Buyer: Shopping
1. Register as Buyer (or browse as guest)
2. Browse products on home page
3. Add to cart
4. Checkout
5. Complete purchase

## 🔧 Troubleshooting Quick Fixes

### Server won't start
```bash
# Check if port is in use
python manage.py runserver 8001
```

### Database errors
```bash
# Reset database
del db.sqlite3
python manage.py migrate
```

### Module not found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Virtual environment issues
```bash
# Recreate virtual environment
rmdir /s /q env  # Windows
rm -rf env/      # Linux/Mac
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

## 📁 File Locations

### Templates
```
store/templates/store/
├── base.html              # Base template
├── store.html             # Home page
├── vendor_dashboard.html  # Vendor dashboard
├── add_product.html       # Add product form
└── create_store.html      # Create store form
```

### Static Files
```
static/
├── css/      # Stylesheets
├── js/       # JavaScript
└── images/   # Images
```

### Configuration
```
ecommerce/
├── settings.py  # Main settings
└── urls.py      # URL routing
```

## 🐛 Common Errors & Solutions

| Error | Solution |
|-------|----------|
| "No module named 'django'" | Activate virtual environment |
| "Port 8000 in use" | Use different port: `runserver 8001` |
| "TemplateDoesNotExist" | Check you're in correct directory |
| "Database connection error" | Check MariaDB is running |
| "Empty home page" | Create store and add products |
| "Can't add product" | Create store first |

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Main documentation |
| SETUP_GUIDE.md | Detailed setup instructions |
| PROJECT_STRUCTURE.md | File organization guide |
| API_ENDPOINTS.md | API documentation |
| QUICK_REFERENCE.md | This file |

## 🎯 Testing

```bash
# Test database
python docs/tests/check_db_status.py

# Test API
python docs/tests/test_api.py

# Test MariaDB
python docs/tests/final_mariadb_test.py
```

## 🔑 Default Credentials

After running `createsuperuser`, use your chosen credentials.

**Example:**
- Username: `admin`
- Password: (your chosen password)

## 💡 Pro Tips

1. **Always activate virtual environment** before running commands
2. **Create stores before adding products** (vendors)
3. **Use admin panel** for quick data management
4. **Check terminal output** for error messages
5. **Read error pages** - Django provides helpful debugging info

## 🆘 Need More Help?

1. **Detailed Setup**: See [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. **API Usage**: See [docs/API_ENDPOINTS.md](docs/API_ENDPOINTS.md)
3. **Project Structure**: See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
4. **Twitter Setup**: See [docs/TWITTER_SETUP_GUIDE.md](docs/TWITTER_SETUP_GUIDE.md)

---

**Keep this file handy for quick reference!** 📌