#!/usr/bin/env python3
"""
Quick Database Status Checker for eCommerce Project.
"""
import os
import sys

def check_database_status():
    """Check current database configuration and status."""
    print("🔍 Database Status Check")
    print("=" * 30)
    
    # Check environment variables
    use_mariadb = os.environ.get('USE_MARIADB')
    mariadb_password = os.environ.get('MARIADB_PASSWORD')
    
    print(f"Environment Variables:")
    print(f"   USE_MARIADB: {use_mariadb or 'Not set (using SQLite)'}")
    print(f"   MARIADB_PASSWORD: {'Set' if mariadb_password else 'Not set'}")
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    
    try:
        import django
        django.setup()
        
        from django.conf import settings
        from django.db import connection
        
        # Get database configuration
        db_config = settings.DATABASES['default']
        
        print(f"\nDjango Database Configuration:")
        print(f"   Engine: {db_config['ENGINE']}")
        print(f"   Name: {db_config['NAME']}")
        
        if 'mysql' in db_config['ENGINE']:
            print(f"   Host: {db_config.get('HOST', 'localhost')}")
            print(f"   Port: {db_config.get('PORT', '3306')}")
            print(f"   User: {db_config.get('USER', 'root')}")
        
        # Test connection
        try:
            cursor = connection.cursor()
            
            if 'mysql' in db_config['ENGINE']:
                cursor.execute("SELECT DATABASE(), VERSION()")
                result = cursor.fetchone()
                print(f"\n✅ MariaDB Connection Successful:")
                print(f"   Database: {result[0]}")
                print(f"   Version: {result[1]}")
                
                # Check tables
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f"   Tables: {len(tables)} found")
                
            else:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                print(f"\n✅ SQLite Connection Successful:")
                print(f"   Database file: {db_config['NAME']}")
                print(f"   Tables: {len(tables)} found")
            
            # Check data
            from store.models import Product, Store
            from django.contrib.auth.models import User
            
            product_count = Product.objects.count()
            store_count = Store.objects.count()
            user_count = User.objects.count()
            
            print(f"\n📊 Data Summary:")
            print(f"   Users: {user_count}")
            print(f"   Stores: {store_count}")
            print(f"   Products: {product_count}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Database Connection Failed: {e}")
            return False
            
    except Exception as e:
        print(f"\n❌ Django Setup Failed: {e}")
        return False

if __name__ == "__main__":
    check_database_status()