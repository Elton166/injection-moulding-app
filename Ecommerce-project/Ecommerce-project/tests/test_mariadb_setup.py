#!/usr/bin/env python3
"""
MariaDB Setup and Test Script for eCommerce Project.
"""
import os
import sys
import mysql.connector
from mysql.connector import Error

def test_mariadb_connection(password=''):
    """Test MariaDB connection with given password."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ MariaDB Connection Successful!")
            print(f"   Version: {version[0]}")
            return True
            
    except Error as e:
        print(f"❌ MariaDB Connection Failed: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def create_ecommerce_database(password=''):
    """Create the eCommerce database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✅ Database 'ecommerce_db' created successfully!")
            
            # Show databases
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print("\n📋 Available Databases:")
            for db in databases:
                print(f"   - {db[0]}")
            
            return True
            
    except Error as e:
        print(f"❌ Database Creation Failed: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def backup_sqlite_data():
    """Backup SQLite data before migration."""
    print("📦 Backing up SQLite data...")
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    
    import django
    django.setup()
    
    from django.core.management import call_command
    
    try:
        with open('sqlite_backup.json', 'w') as f:
            call_command('dumpdata', 
                        '--natural-foreign', 
                        '--natural-primary',
                        '--exclude=contenttypes',
                        '--exclude=auth.Permission',
                        stdout=f)
        
        print("✅ SQLite data backed up to sqlite_backup.json")
        return True
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

def update_settings_for_mariadb(password):
    """Update settings.py to use MariaDB."""
    print("🔧 Updating settings.py for MariaDB...")
    
    settings_content = f'''# Database Configuration
# MariaDB Configuration
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'root',
        'PASSWORD': '{password}',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {{
            'sql_mode': 'traditional',
        }}
    }}
}}'''
    
    # Read current settings
    with open('ecommerce/settings.py', 'r') as f:
        content = f.read()
    
    # Find and replace database configuration
    import re
    
    # Pattern to match the entire DATABASES section
    pattern = r'DATABASES\s*=\s*\{[^}]*\}[^}]*\}'
    
    if re.search(pattern, content):
        # Replace existing DATABASES configuration
        new_content = re.sub(pattern, settings_content, content, flags=re.DOTALL)
    else:
        # If pattern not found, append at the end
        new_content = content + '\n\n' + settings_content
    
    # Write updated settings
    with open('ecommerce/settings.py', 'w') as f:
        f.write(new_content)
    
    print("✅ Settings updated for MariaDB")
    return True

def run_django_migrations():
    """Run Django migrations for MariaDB."""
    print("🔄 Running Django migrations...")
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    
    import django
    django.setup()
    
    from django.core.management import call_command
    
    try:
        print("   Creating migrations...")
        call_command('makemigrations')
        
        print("   Applying migrations...")
        call_command('migrate')
        
        print("✅ Migrations completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def restore_data_to_mariadb():
    """Restore data to MariaDB."""
    print("📥 Restoring data to MariaDB...")
    
    from django.core.management import call_command
    
    try:
        if os.path.exists('sqlite_backup.json'):
            call_command('loaddata', 'sqlite_backup.json')
            print("✅ Data restored to MariaDB successfully")
            return True
        else:
            print("⚠️ No backup file found")
            return False
            
    except Exception as e:
        print(f"❌ Data restoration failed: {e}")
        return False

def test_django_mariadb():
    """Test Django with MariaDB."""
    print("🧪 Testing Django with MariaDB...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
        
        import django
        django.setup()
        
        from django.db import connection
        from store.models import Product, Store
        from django.contrib.auth.models import User
        
        # Test connection
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE(), VERSION()")
        result = cursor.fetchone()
        
        print(f"✅ Django MariaDB Connection Successful!")
        print(f"   Database: {result[0]}")
        print(f"   Version: {result[1]}")
        
        # Check data
        product_count = Product.objects.count()
        store_count = Store.objects.count()
        user_count = User.objects.count()
        
        print(f"\n📊 Data Summary:")
        print(f"   Users: {user_count}")
        print(f"   Stores: {store_count}")
        print(f"   Products: {product_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Django MariaDB test failed: {e}")
        return False

def main():
    """Main function to set up and test MariaDB."""
    print("🚀 MariaDB Setup and Test for eCommerce Project")
    print("=" * 50)
    
    # Get MariaDB password
    password = input("Enter MariaDB root password (press Enter if no password): ")
    
    print("\n🔍 Step 1: Testing MariaDB Connection...")
    if not test_mariadb_connection(password):
        print("\n💡 Troubleshooting Tips:")
        print("   1. Make sure MariaDB is installed and running")
        print("   2. Check if the password is correct")
        print("   3. Try starting MariaDB service")
        print("   4. For XAMPP users: Start MySQL from XAMPP Control Panel")
        return
    
    print("\n🔍 Step 2: Creating eCommerce Database...")
    if not create_ecommerce_database(password):
        return
    
    print("\n🔍 Step 3: Backing up SQLite Data...")
    backup_sqlite_data()
    
    print("\n🔍 Step 4: Updating Django Settings...")
    update_settings_for_mariadb(password)
    
    print("\n🔍 Step 5: Running Django Migrations...")
    if not run_django_migrations():
        return
    
    print("\n🔍 Step 6: Restoring Data...")
    restore_data_to_mariadb()
    
    print("\n🔍 Step 7: Testing Django with MariaDB...")
    if test_django_mariadb():
        print("\n" + "=" * 50)
        print("🎉 MariaDB Setup Complete!")
        print("\n📝 Your eCommerce project is now running on MariaDB!")
        print("🚀 Start your server with: python manage.py runserver")
    else:
        print("\n⚠️ There were issues with the setup. Check the errors above.")

if __name__ == "__main__":
    main()