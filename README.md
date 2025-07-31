# Personal Finance Tracker

A comprehensive personal finance management application built with Python, Tkinter, and MySQL. Track your income, expenses, visualize spending trends, and manage budgets with an intuitive graphical user interface.

![Finance Tracker Dashboard](https://via.placeholder.com/800x500/2c3e50/ffffff?text=Personal+Finance+Tracker+Dashboard)

## 🌟 Features

### Core Functionality
- **Income Tracking**: Record salary, freelance income, and other revenue sources
- **Expense Management**: Categorize and track all your expenses
- **Real-time Dashboard**: View financial overview with quick statistics
- **Visual Analytics**: Interactive charts showing expense trends over time
- **Transaction History**: Complete log of all financial activities

### Advanced Features
- **Budget Management**: Set monthly budgets for different categories and track progress
- **Financial Reports**: Generate detailed reports for different time periods
- **Category Management**: Organize expenses with customizable categories
- **Data Persistence**: All data stored securely in MySQL database
- **Modern UI**: Clean, intuitive interface built with Tkinter

### Dashboard Components
- **Quick Stats**: Current month income, expenses, and net balance
- **Recent Transactions**: Latest 10 financial activities
- **Expense Trends**: 30-day spending visualization
- **Monthly Summary**: Key metrics and top spending category

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd personal-finance-tracker
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup MySQL Database
1. **Install MySQL** (if not already installed):
   - **Ubuntu/Debian**: `sudo apt-get install mysql-server`
   - **macOS**: `brew install mysql`
   - **Windows**: Download from [MySQL website](https://dev.mysql.com/downloads/mysql/)

2. **Start MySQL service**:
   - **Ubuntu/Debian**: `sudo systemctl start mysql`
   - **macOS**: `brew services start mysql`
   - **Windows**: Use MySQL Workbench or Services panel

3. **Configure Database Connection**:
   Edit `database.py` if needed to match your MySQL configuration:
   ```python
   # Default settings (line 8-12)
   def __init__(self, host='localhost', database='finance_tracker', user='root', password=''):
   ```

### Step 4: Run the Application
```bash
python finance_tracker.py
```

The application will automatically:
- Create the database if it doesn't exist
- Set up all required tables
- Insert default expense categories

## 📖 Usage Guide

### Getting Started
1. **Launch the Application**: Run `python finance_tracker.py`
2. **Navigate the Interface**: Use the sidebar buttons to access different features
3. **Add Your First Income**: Click "Add Income" and enter your salary or other income
4. **Record Expenses**: Use "Add Expense" to track your spending
5. **View Dashboard**: Monitor your financial health on the main dashboard

### Adding Income
1. Click **"Add Income"** in the sidebar
2. Fill in the form:
   - **Amount**: Enter the income amount (e.g., 3000.00)
   - **Source**: Specify the income source (e.g., "Salary", "Freelance")
   - **Date**: Select the date (defaults to today)
   - **Description**: Optional details about the income
3. Click **"Add Income"** to save

### Recording Expenses
1. Click **"Add Expense"** in the sidebar
2. Complete the expense form:
   - **Amount**: Enter the expense amount
   - **Category**: Select from predefined categories (Food, Transportation, etc.)
   - **Date**: Choose the expense date
   - **Description**: Describe the expense (required)
3. Click **"Add Expense"** to save

### Managing Budgets
1. Navigate to **"Budget Manager"**
2. Click **"Set New Budget"** to create a budget
3. Select a category and set monthly budget amount
4. View budget status with progress bars and spending percentages
5. Monitor budget health with color-coded indicators:
   - 🟢 Green: Under 80% of budget
   - 🟡 Yellow: 80-100% of budget
   - 🔴 Red: Over budget

### Generating Reports
1. Go to **"View Reports"**
2. Select time period:
   - Last 7 days
   - Last 30 days
   - Last 3 months
   - Last year
3. Click **"Generate Report"** for detailed financial analysis
4. Review income sources, expense breakdowns, and spending percentages

## 🗂️ Database Schema

The application uses five main tables:

### Users Table
- `id`: Primary key
- `username`: User identifier
- `email`: User email
- `created_at`: Account creation timestamp

### Categories Table
- `id`: Primary key
- `name`: Category name (e.g., "Food & Dining")
- `color`: Category color for visualization
- `created_at`: Creation timestamp

### Income Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `amount`: Income amount
- `source`: Income source description
- `date`: Income date
- `description`: Optional details
- `created_at`: Record creation timestamp

### Expenses Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `category_id`: Foreign key to categories
- `amount`: Expense amount
- `description`: Expense description
- `date`: Expense date
- `created_at`: Record creation timestamp

### Budgets Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `category_id`: Foreign key to categories
- `amount`: Budget amount
- `month`: Budget month
- `year`: Budget year
- `created_at`: Creation timestamp

## 🎨 Default Categories

The application comes with 10 predefined expense categories:

1. **Food & Dining** 🍽️ - Restaurants, groceries, food delivery
2. **Transportation** 🚗 - Gas, public transport, car maintenance
3. **Shopping** 🛍️ - Clothing, electronics, general purchases
4. **Entertainment** 🎬 - Movies, games, subscriptions
5. **Bills & Utilities** 💡 - Electricity, water, internet, phone
6. **Healthcare** 🏥 - Medical expenses, insurance, pharmacy
7. **Education** 📚 - Courses, books, training
8. **Travel** ✈️ - Flights, hotels, vacation expenses
9. **Personal Care** 💄 - Grooming, beauty products
10. **Other** 📦 - Miscellaneous expenses

## 🔧 Customization

### Adding New Categories
Currently, categories are managed through the database. You can add new categories by:
1. Accessing the "Categories" section in the application
2. Or directly inserting into the MySQL database:
```sql
INSERT INTO categories (name, color) VALUES ('New Category', '#hexcolor');
```

### Modifying Database Connection
Edit `database.py` to change connection parameters:
```python
class DatabaseManager:
    def __init__(self, host='localhost', database='finance_tracker', user='root', password='your_password'):
```

### Styling Customization
Modify the color scheme in `finance_tracker.py`:
```python
self.colors = {
    'primary': '#2c3e50',    # Dark blue-gray
    'secondary': '#3498db',  # Blue
    'success': '#27ae60',    # Green
    'danger': '#e74c3c',     # Red
    'warning': '#f39c12',    # Orange
    'light': '#ecf0f1',      # Light gray
    'dark': '#34495e'        # Dark gray
}
```

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
- Ensure MySQL server is running
- Check username/password in `database.py`
- Verify MySQL service is accessible on localhost:3306

**Missing Dependencies**
```bash
pip install --upgrade -r requirements.txt
```

**Permission Denied (MySQL)**
```sql
-- Grant permissions to your MySQL user
GRANT ALL PRIVILEGES ON finance_tracker.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

**Chart Display Issues**
- Ensure matplotlib is properly installed
- Check if Tkinter supports matplotlib backend
- Try updating matplotlib: `pip install --upgrade matplotlib`

### Error Logs
The application prints error messages to the console. Common errors include:
- Database connection failures
- Invalid data entry (non-numeric amounts)
- Missing required fields

## 📊 Sample Data

To test the application with sample data, you can manually add some transactions:

### Sample Income Entries
- **Salary**: $3,500 (monthly)
- **Freelance**: $800 (project work)
- **Investment**: $150 (dividends)

### Sample Expense Entries
- **Groceries**: $120 (Food & Dining)
- **Gas**: $45 (Transportation)
- **Netflix**: $15 (Entertainment)
- **Electric Bill**: $85 (Bills & Utilities)

## 🚀 Future Enhancements

Potential features for future versions:
- **Multi-user Support**: User authentication and profiles
- **Data Export**: CSV/PDF export functionality
- **Recurring Transactions**: Automatic recurring income/expenses
- **Goal Setting**: Savings goals and progress tracking
- **Mobile App**: Companion mobile application
- **Cloud Sync**: Cloud database integration
- **Advanced Analytics**: Predictive spending analysis
- **Receipt Scanning**: OCR for expense receipt processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the error messages in the console
3. Ensure all dependencies are properly installed
4. Verify MySQL is running and accessible

## 🏆 Acknowledgments

- Built with Python and Tkinter for cross-platform compatibility
- Uses MySQL for reliable data persistence
- Matplotlib for beautiful data visualizations
- tkcalendar for enhanced date selection
- Inspired by modern personal finance management tools

---

**Happy budgeting! 💰**
