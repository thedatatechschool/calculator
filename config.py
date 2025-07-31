# Personal Finance Tracker Configuration
# Edit these settings to match your environment

# Database Configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'database': 'finance_tracker',
    'user': 'root',
    'password': '',  # Add your MySQL password here
    'port': 3306
}

# Application Settings
APP_CONFIG = {
    'window_title': 'Personal Finance Tracker',
    'window_size': '1200x800',
    'theme': 'default',  # Can be extended for custom themes
}

# Chart Settings
CHART_CONFIG = {
    'default_days': 30,
    'chart_style': 'seaborn',  # matplotlib style
    'dpi': 100,
    'figure_size': (6, 4)
}

# Default Categories (will be created if they don't exist)
DEFAULT_CATEGORIES = [
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

# Color Scheme
COLORS = {
    'primary': '#2c3e50',
    'secondary': '#3498db',
    'success': '#27ae60',
    'danger': '#e74c3c',
    'warning': '#f39c12',
    'light': '#ecf0f1',
    'dark': '#34495e'
}

# Date Formats
DATE_FORMATS = {
    'display': '%Y-%m-%d',
    'input': '%Y-%m-%d',
    'report': '%B %d, %Y'
}

# Validation Rules
VALIDATION = {
    'max_amount': 999999.99,
    'min_amount': 0.01,
    'max_description_length': 500,
    'required_fields': ['amount', 'description']
}