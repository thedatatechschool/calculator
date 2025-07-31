#!/usr/bin/env python3
"""
Quick start script for Personal Finance Tracker
This script performs basic checks and launches the application.
"""

import sys
import os

def main():
    """Quick start the finance tracker"""
    print("🚀 Starting Personal Finance Tracker...")
    
    # Check if main application exists
    if not os.path.exists('finance_tracker.py'):
        print("❌ Error: finance_tracker.py not found")
        print("Please ensure you're in the correct directory")
        sys.exit(1)
    
    # Check if database module exists
    if not os.path.exists('database.py'):
        print("❌ Error: database.py not found")
        print("Please run setup.py first")
        sys.exit(1)
    
    try:
        # Import and run the application
        print("Loading application...")
        import finance_tracker
        finance_tracker.main()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Some dependencies may be missing. Please run:")
        print("  python setup.py")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("For troubleshooting help, see README.md")
        sys.exit(1)

if __name__ == "__main__":
    main()