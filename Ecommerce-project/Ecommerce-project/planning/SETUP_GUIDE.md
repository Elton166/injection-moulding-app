# Complete Setup Guide

## 🚀 Quick Start (5 Minutes)

Follow these exact steps to get the application running:

### Step 1: Check Python Installation

```bash
python --version
```

You should see Python 3.8 or higher. If not, install Python from https://www.python.org/

### Step 2: Navigate to Project Directory

```bash
cd Ecommerce-project
```

### Step 3: Create Virtual Environment

**IMPORTANT**: If you see an `env/` folder already in the project, DELETE IT first!

```bash
# Windows
python -m venv env
env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

You should see `(env)` at the start of your command prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

Wait for all packages to install (this may take 2-3 minutes).

### Step 5: Setup Database

For quick start, we'll use SQLite (no installation needed):

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Admin User (Optional but Recommended)

```bash
python manage.py createsuperuser
```

Follow the prompts:
- Username: `admin`
- Email: `admin@example.com`
- Password: (choose a password)

### Step 7: Run the Server

```bash
python manage.py runserver
```

### Step 8: Open Your Browser

Visit: http://127.0.0.1:8000/

You should see the welcome page!

---

## 📝 First Time User Guide

### Creating Your First Account

1. **Click "Register"** on the home page
2. **Fill in the form**:
   ```
   Username: testvendor
   Email: vendor@test.com
   Password: test123456
   Account Type: Vendor (to sell) or Buyer (to shop)
   ```
3. **Click "Create Account"**
4. **Login** with your credentials

### For Vendors - Creating Your First Store

1. After login, click **"Vendor Dashboard"** in the navigation
2. Click **"Create Store"** button
3. Fill in store details:
   ```
   Store Name: My Test Store
   Description: A great store for testing
   Address: 123 Test Street, Cape Town
   Phone: +27-123-456-7890
   Email: store@test.com
   ```
4. Click **"Create Store"**

### For Vendors - Adding Your First Product

1. In Vendor Dashboard, click **"Add Product"**
2. Fill in product details:
   ```
   Product Name: Test Laptop
   Store: My Test Store (select from dropdown)
   Description: A great laptop for testing
   Price: 18999.99
   Stock Quantity: 10
   ```
3. Upload an image (optional)
4. Click **"Add Product"**

Your product will now appear on the home page!

### For Buyers - Making Your First Purchase

1. Browse products on the home page
2. Click **"Add to Cart"** on a product
3. Click the **Cart icon** in navigation
4. Click **"Checkout"**
5. Fill in shipping information
6. Complete purchase

---

## 🗄️ Database Options

### Option A: SQLite (Default - Easiest)

Already configured! No additional setup needed.

**Pros:**
- No installation required
- Works immediately
- Perfect for development

**Cons:**
- Not suitable for production
- Limited concurrent users

### Option B: MariaDB (Production Ready)

#### 1. Install MariaDB

**Windows:**
- Download from https://mariadb.org/download/
- Run installer
- Set root password during installation

**Linux:**
```bash
sudo apt-get update
sudo apt-get install mariadb-server
sudo mysql_secure_installation
```

**Mac:**
```bash
brew install mariadb
brew services start mariadb
```

#### 2. Create Database

```bash
mysql -u root -p
```

Then in MySQL prompt:
```sql
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

#### 3. Update Settings

Edit `ecommerce/settings.py` and update the password:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'root',
        'PASSWORD': 'your_actual_password',  # Change this!
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

#### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🐦 Twitter Integration (Optional)

### Step 1: Create Twitter Developer Account

1. Go to https://developer.twitter.com/
2. Apply for developer account (free tier)
3. Create an app with "Read and Write" permissions

### Step 2: Get API Keys

Generate these 4 credentials:
- API Key
- API Secret
- Access Token
- Access Token Secret

### Step 3: Set Environment Variables

**Windows:**
```cmd
set TWITTER_API_KEY=your_api_key
set TWITTER_API_SECRET=your_api_secret
set TWITTER_ACCESS_TOKEN=your_access_token
set TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

**Linux/Mac:**
```bash
export TWITTER_API_KEY=your_api_key
export TWITTER_API_SECRET=your_api_secret
export TWITTER_ACCESS_TOKEN=your_access_token
export TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

### Step 4: Test Integration

```bash
python docs/tests/test_twitter_free_tier.py
```

---

## 🧪 Testing the Application

### Manual Testing Checklist

- [ ] Home page loads
- [ ] Registration works (both buyer and vendor)
- [ ] Login works
- [ ] Logout works
- [ ] Vendor can create store
- [ ] Vendor can add product
- [ ] Products appear on home page
- [ ] Buyer can add to cart
- [ ] Checkout process works

### Automated Tests

```bash
# Test database
python docs/tests/check_db_status.py

# Test API
python docs/tests/test_api.py

# Test MariaDB (if using MariaDB)
python docs/tests/final_mariadb_test.py
```

---

## 🔧 Troubleshooting

### Problem: "No module named 'django'"

**Solution:**
```bash
# Make sure virtual environment is activated
# You should see (env) in your prompt

# Windows
env\Scripts\activate

# Linux/Mac
source env/bin/activate

# Then install dependencies
pip install -r requirements.txt
```

### Problem: "Port 8000 is already in use"

**Solution:**
```bash
# Use a different port
python manage.py runserver 8001

# Or find and kill the process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Problem: "TemplateDoesNotExist"

**Solution:**
Make sure you're in the correct directory:
```bash
# You should be in Ecommerce-project/
# Not in the parent directory

cd Ecommerce-project
python manage.py runserver
```

### Problem: "Database connection error"

**Solution for MariaDB:**
1. Check if MariaDB is running
2. Verify password in `ecommerce/settings.py`
3. Make sure database `ecommerce_db` exists

**Solution for SQLite:**
```bash
# Delete old database and recreate
del db.sqlite3  # Windows
rm db.sqlite3   # Linux/Mac

python manage.py migrate
```

### Problem: "Empty home page / No products"

**Solution:**
1. Register as a vendor
2. Create a store
3. Add products
4. Products will appear on home page

### Problem: "Can't add product - no stores"

**Solution:**
You must create a store first:
1. Go to Vendor Dashboard
2. Click "Create Store"
3. Fill in store details
4. Then you can add products

---

## 📞 Getting Help

If you're still stuck:

1. **Check the logs** - Look at the terminal where `runserver` is running
2. **Check Django admin** - Visit http://127.0.0.1:8000/admin/
3. **Read the error message** - Django provides detailed error pages
4. **Check the documentation** - See README.md and other docs

---

## ✅ Success Checklist

You've successfully set up the application when:

- [ ] Server runs without errors
- [ ] Home page displays welcome message
- [ ] You can register a new account
- [ ] You can login
- [ ] Vendors can create stores
- [ ] Vendors can add products
- [ ] Products appear on home page
- [ ] Buyers can add to cart
- [ ] Admin panel is accessible

---

## 🎉 Next Steps

Once everything is working:

1. **Explore the API** - See `docs/API_ENDPOINTS.md`
2. **Set up Twitter** - See `docs/TWITTER_SETUP_GUIDE.md`
3. **Deploy to production** - Consider Heroku, AWS, or DigitalOcean
4. **Customize the design** - Edit templates in `store/templates/`
5. **Add more features** - The codebase is well-structured for expansion

---

**Congratulations! Your eCommerce platform is now running!** 🎊