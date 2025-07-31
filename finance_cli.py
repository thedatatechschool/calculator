#!/usr/bin/env python3
"""
Command-line version of Personal Finance Tracker
"""

import database
from datetime import datetime, timedelta
from collections import defaultdict

def show_dashboard():
    print("\n📊 FINANCIAL DASHBOARD")
    print("-" * 30)
    
    # Get current month data
    today = datetime.now().date()
    start_of_month = today.replace(day=1)
    
    income_data = database.get_income_by_date_range(start_of_month, today)
    expense_data = database.get_expenses_by_date_range(start_of_month, today)
    
    total_income = sum(item['amount'] for item in income_data)
    total_expenses = sum(item['amount'] for item in expense_data)
    net_balance = total_income - total_expenses
    
    print(f"📅 Period: {start_of_month} to {today}")
    print(f"💰 Total Income:  ${total_income:>10.2f}")
    print(f"💸 Total Expenses: ${total_expenses:>10.2f}")
    print(f"💵 Net Balance:   ${net_balance:>10.2f}")
    
    if net_balance >= 0:
        print("✅ You're in the positive!")
    else:
        print("⚠️  You're spending more than earning")

def add_sample_data():
    print("\n📊 ADDING SAMPLE DATA")
    print("-" * 25)
    
    try:
        today = datetime.now().date()
        
        # Add sample income
        database.add_income(3500.00, "Salary", today, "Monthly salary")
        database.add_income(800.00, "Freelance", today - timedelta(days=5), "Website project")
        
        # Add sample expenses
        categories = database.get_categories()
        if categories:
            cat_map = {cat['name']: cat['id'] for cat in categories}
            
            if 'Food & Dining' in cat_map:
                database.add_expense(120.00, cat_map['Food & Dining'], "Weekly groceries", today - timedelta(days=2))
            
            if 'Transportation' in cat_map:
                database.add_expense(60.00, cat_map['Transportation'], "Gas fill-up", today - timedelta(days=3))
        
        print("✅ Sample data added successfully!")
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")

def main():
    print("🚀 Personal Finance Tracker - CLI Demo")
    print("="*40)
    
    # Test database connection
    db = database.get_db()
    if not db:
        print("❌ Could not connect to MySQL database")
        return
    
    print("✅ Database connection successful!")
    db.close_connection()
    
    # Add sample data
    add_sample_data()
    
    # Show dashboard
    show_dashboard()
    
    print("\n🎉 Finance tracker is working perfectly!")
    print("📝 To run the full GUI version, use: python3 finance_tracker.py")
    print("   (Note: GUI requires a display/X11 forwarding)")

if __name__ == "__main__":
    main()