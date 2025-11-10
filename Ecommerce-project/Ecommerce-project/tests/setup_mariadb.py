#!/usr/bin/env python3
"""
MariaDB Setup Script for eCommerce Project.

This script helps set up MariaDB database for the eCommerce application.
"""
import mysql.connector
from mysql.connector import Error
import os
import sys


def create_database():
    """Create the eCommerce database in MariaDB."""
    try:
        # Connect to MariaDB
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  # Add your MariaDB root password here
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✅ Database 'ecommerce_db' created successfully!")
            
            # Create a dedicated user (optional but recommended)
            try:
                cursor.execute("CREATE USER IF NOT EXISTS 'ecommerce_user'@'localhost' IDENTIFIED BY 'ecommerce_password'")
                cursor.execute("GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost'")
                cursor.execute("FLUSH PRIVILEGES")
                print("✅ Database user 'ecommerce_user' created successfully!")
            except Error as e:
                print(f"⚠️  User creation failed (may already exist): {e}")
            
    except Error as e:
        print(f"❌ Error connecting to MariaDB: {e}")
        print("\n💡 Make sure MariaDB is installed and running:")
        print("   - Windows: Download from https://mariadb.org/download/")
        print("   - Start MariaDB service")
        print("   - Update the password in this script if needed")
        return False
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
    return True


def test_django_connection():
    """Test Django database connection."""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
        import django
        django.setup()
        
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ Django can connect to MariaDB successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Django connection failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Setting up MariaDB for eCommerce Project")
    print("=" * 50)
    
    if create_database():
        print("\n🔄 Testing Django connection...")
        if test_django_connection():
            print("\n✅ MariaDB setup completed successfully!")
            print("\n📝 Next steps:")
            print("   1. Run: python manage.py makemigrations")
            print("   2. Run: python manage.py migrate")
            print("   3. Run: python manage.py createsuperuser")
        else:
            print("\n⚠️  Database created but Django connection failed.")
            print("   Check your settings.py database configuration.")
    else:
        print("\n❌ MariaDB setup failed.")
        print("   Using SQLite fallback. Set USE_SQLITE=1 environment variable.")