#!/usr/bin/env python3
"""
Personal Finance Tracker Setup Script
This script helps users set up the application by checking dependencies and database connectivity.
"""

import subprocess
import sys
import os
import importlib

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - Compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ Error: requirements.txt not found")
        return False
    
    try:
        # Install packages
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Error installing dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n🔍 Checking installed packages...")
    
    required_packages = [
        'mysql.connector',
        'matplotlib',
        'pandas',
        'numpy',
        'tkcalendar',
        'PIL'  # Pillow
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} - Installed")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def check_mysql_connection():
    """Test MySQL database connection"""
    print("\n🗄️ Testing database connection...")
    
    try:
        import database
        db = database.get_db()
        if db:
            print("✅ Database connection successful")
            print("✅ Database and tables created/verified")
            db.close_connection()
            return True
        else:
            print("❌ Database connection failed")
            return False
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def check_tkinter():
    """Check if Tkinter is available"""
    print("\n🖥️ Checking GUI framework...")
    
    try:
        import tkinter as tk
        # Test basic Tkinter functionality
        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.destroy()
        print("✅ Tkinter - Available")
        return True
    except ImportError:
        print("❌ Tkinter not available")
        print("Install tkinter: sudo apt-get install python3-tk (Ubuntu/Debian)")
        return False
    except Exception as e:
        print(f"❌ Tkinter error: {e}")
        return False

def create_sample_data():
    """Ask user if they want to create sample data"""
    print("\n📊 Sample Data Setup")
    response = input("Would you like to add sample data for testing? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        try:
            import database
            from datetime import datetime, timedelta
            
            # Add sample income
            today = datetime.now().date()
            database.add_income(3500.00, "Salary", today, "Monthly salary")
            database.add_income(800.00, "Freelance", today - timedelta(days=5), "Website project")
            database.add_income(150.00, "Investment", today - timedelta(days=10), "Dividend payment")
            
            # Add sample expenses
            categories = database.get_categories()
            if categories:
                # Food & Dining
                food_cat = next((cat for cat in categories if cat['name'] == 'Food & Dining'), None)
                if food_cat:
                    database.add_expense(120.00, food_cat['id'], "Weekly groceries", today - timedelta(days=2))
                    database.add_expense(45.00, food_cat['id'], "Restaurant dinner", today - timedelta(days=5))
                
                # Transportation
                transport_cat = next((cat for cat in categories if cat['name'] == 'Transportation'), None)
                if transport_cat:
                    database.add_expense(60.00, transport_cat['id'], "Gas fill-up", today - timedelta(days=3))
                
                # Bills & Utilities
                bills_cat = next((cat for cat in categories if cat['name'] == 'Bills & Utilities'), None)
                if bills_cat:
                    database.add_expense(85.00, bills_cat['id'], "Electric bill", today - timedelta(days=7))
                    database.add_expense(50.00, bills_cat['id'], "Internet bill", today - timedelta(days=10))
                
                # Entertainment
                entertainment_cat = next((cat for cat in categories if cat['name'] == 'Entertainment'), None)
                if entertainment_cat:
                    database.add_expense(15.00, entertainment_cat['id'], "Netflix subscription", today - timedelta(days=1))
                    database.add_expense(25.00, entertainment_cat['id'], "Movie tickets", today - timedelta(days=8))
            
            print("✅ Sample data added successfully!")
            
        except Exception as e:
            print(f"❌ Error adding sample data: {e}")

def print_mysql_help():
    """Print MySQL installation and setup help"""
    print("\n🗄️ MySQL Setup Help")
    print("=" * 50)
    print("If you don't have MySQL installed:")
    print()
    print("Ubuntu/Debian:")
    print("  sudo apt-get update")
    print("  sudo apt-get install mysql-server")
    print("  sudo systemctl start mysql")
    print()
    print("macOS (with Homebrew):")
    print("  brew install mysql")
    print("  brew services start mysql")
    print()
    print("Windows:")
    print("  Download from: https://dev.mysql.com/downloads/mysql/")
    print()
    print("After installation, you may need to:")
    print("1. Set a root password")
    print("2. Update database.py with your credentials")
    print("3. Ensure MySQL service is running")

def main():
    """Main setup function"""
    print("🚀 Personal Finance Tracker Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check Tkinter
    if not check_tkinter():
        print("\n⚠️ Warning: GUI may not work without Tkinter")
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️ Warning: Some dependencies may be missing")
    
    # Check dependencies
    if not check_dependencies():
        print("\n⚠️ Warning: Some required packages are missing")
        print("Try running: pip install -r requirements.txt")
    
    # Test database connection
    db_success = check_mysql_connection()
    if not db_success:
        print_mysql_help()
        print("\n⚠️ Database setup required before running the application")
    
    # Offer to create sample data
    if db_success:
        create_sample_data()
    
    # Final instructions
    print("\n🎉 Setup Complete!")
    print("=" * 20)
    
    if db_success:
        print("✅ Everything looks good! You can now run:")
        print("   python finance_tracker.py")
    else:
        print("⚠️ Please set up MySQL database first, then run:")
        print("   python setup.py")
        print("   python finance_tracker.py")
    
    print("\n📖 For detailed instructions, see README.md")

if __name__ == "__main__":
    main()