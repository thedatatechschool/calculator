import mysql.connector
from mysql.connector import Error
import logging
from datetime import datetime

class DatabaseManager:
    def __init__(self, host='localhost', database='finance_tracker', user='finance_user', password='finance_pass'):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Successfully connected to MySQL database")
                return True
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            # Try to create database if it doesn't exist
            try:
                temp_connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password
                )
                cursor = temp_connection.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
                temp_connection.commit()
                cursor.close()
                temp_connection.close()
                
                # Now connect to the created database
                self.connection = mysql.connector.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
                )
                if self.connection.is_connected():
                    print("Database created and connected successfully")
                    return True
            except Error as create_error:
                print(f"Error creating database: {create_error}")
                return False
        return False
    
    def create_tables(self):
        """Create necessary tables for the finance tracker"""
        if not self.connection or not self.connection.is_connected():
            return False
            
        try:
            cursor = self.connection.cursor()
            
            # Users table
            users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # Income table
            income_table = """
            CREATE TABLE IF NOT EXISTS income (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT DEFAULT 1,
                amount DECIMAL(10, 2) NOT NULL,
                source VARCHAR(100) NOT NULL,
                date DATE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
            
            # Categories table
            categories_table = """
            CREATE TABLE IF NOT EXISTS categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL,
                color VARCHAR(7) DEFAULT '#3498db',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # Expenses table
            expenses_table = """
            CREATE TABLE IF NOT EXISTS expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT DEFAULT 1,
                category_id INT,
                amount DECIMAL(10, 2) NOT NULL,
                description TEXT NOT NULL,
                date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
            )
            """
            
            # Budgets table
            budgets_table = """
            CREATE TABLE IF NOT EXISTS budgets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT DEFAULT 1,
                category_id INT,
                amount DECIMAL(10, 2) NOT NULL,
                month INT NOT NULL,
                year INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
                UNIQUE KEY unique_budget (user_id, category_id, month, year)
            )
            """
            
            # Execute table creation
            cursor.execute(users_table)
            cursor.execute(categories_table)
            cursor.execute(income_table)
            cursor.execute(expenses_table)
            cursor.execute(budgets_table)
            
            # Insert default user and categories
            cursor.execute("INSERT IGNORE INTO users (username, email) VALUES ('default', 'user@example.com')")
            
            default_categories = [
                ('Food & Dining', '#e74c3c'),
                ('Transportation', '#f39c12'),
                ('Shopping', '#9b59b6'),
                ('Entertainment', '#e67e22'),
                ('Bills & Utilities', '#34495e'),
                ('Healthcare', '#1abc9c'),
                ('Education', '#3498db'),
                ('Travel', '#2ecc71'),
                ('Personal Care', '#f1c40f'),
                ('Other', '#95a5a6')
            ]
            
            for category, color in default_categories:
                cursor.execute("INSERT IGNORE INTO categories (name, color) VALUES (%s, %s)", (category, color))
            
            self.connection.commit()
            cursor.close()
            print("Tables created successfully")
            return True
            
        except Error as e:
            print(f"Error creating tables: {e}")
            return False
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        if not self.connection or not self.connection.is_connected():
            return None
            
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = cursor.rowcount
                
            cursor.close()
            return result
            
        except Error as e:
            print(f"Error executing query: {e}")
            return None
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

# Convenience functions for common operations
def get_db():
    """Get database instance"""
    db = DatabaseManager()
    if db.connect():
        db.create_tables()
        return db
    return None

def add_income(amount, source, date, description=""):
    """Add income record"""
    db = get_db()
    if db:
        query = "INSERT INTO income (amount, source, date, description) VALUES (%s, %s, %s, %s)"
        result = db.execute_query(query, (amount, source, date, description))
        db.close_connection()
        return result
    return None

def add_expense(amount, category_id, description, date):
    """Add expense record"""
    db = get_db()
    if db:
        query = "INSERT INTO expenses (amount, category_id, description, date) VALUES (%s, %s, %s, %s)"
        result = db.execute_query(query, (amount, category_id, description, date))
        db.close_connection()
        return result
    return None

def get_categories():
    """Get all categories"""
    db = get_db()
    if db:
        query = "SELECT * FROM categories ORDER BY name"
        result = db.execute_query(query)
        db.close_connection()
        return result
    return []

def get_expenses_by_date_range(start_date, end_date):
    """Get expenses within date range"""
    db = get_db()
    if db:
        query = """
        SELECT e.*, c.name as category_name, c.color as category_color 
        FROM expenses e 
        LEFT JOIN categories c ON e.category_id = c.id 
        WHERE e.date BETWEEN %s AND %s 
        ORDER BY e.date DESC
        """
        result = db.execute_query(query, (start_date, end_date))
        db.close_connection()
        return result
    return []

def get_income_by_date_range(start_date, end_date):
    """Get income within date range"""
    db = get_db()
    if db:
        query = "SELECT * FROM income WHERE date BETWEEN %s AND %s ORDER BY date DESC"
        result = db.execute_query(query, (start_date, end_date))
        db.close_connection()
        return result
    return []