#!/usr/bin/env python3
"""
Simple test script to verify database connectivity
"""

import database

def test_database():
    print("Testing database connection...")
    
    try:
        # Test database connection
        db = database.get_db()
        if db:
            print("✅ Database connection successful!")
            print("✅ Database and tables created/verified")
            
            # Test adding sample data
            print("\nTesting data operations...")
            
            # Add sample income
            result = database.add_income(3000.00, "Salary", "2025-01-31", "Monthly salary")
            if result:
                print("✅ Sample income added successfully")
            
            # Get categories
            categories = database.get_categories()
            print(f"✅ Found {len(categories)} categories")
            
            if categories:
                # Add sample expense
                food_category = categories[0]  # Use first category
                result = database.add_expense(50.00, food_category['id'], "Lunch", "2025-01-31")
                if result:
                    print("✅ Sample expense added successfully")
            
            # Test data retrieval
            from datetime import datetime, timedelta
            today = datetime.now().date()
            start_date = today - timedelta(days=7)
            
            income_data = database.get_income_by_date_range(start_date, today)
            expense_data = database.get_expenses_by_date_range(start_date, today)
            
            print(f"✅ Retrieved {len(income_data)} income records")
            print(f"✅ Retrieved {len(expense_data)} expense records")
            
            # Calculate totals
            total_income = sum(item['amount'] for item in income_data)
            total_expenses = sum(item['amount'] for item in expense_data)
            
            print(f"\n📊 Financial Summary:")
            print(f"   Total Income: ${total_income:.2f}")
            print(f"   Total Expenses: ${total_expenses:.2f}")
            print(f"   Net Balance: ${total_income - total_expenses:.2f}")
            
            db.close_connection()
            print("\n🎉 All database tests passed!")
            return True
            
        else:
            print("❌ Database connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    test_database()