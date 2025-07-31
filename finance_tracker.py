import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import font as tkfont
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime, timedelta, date
import database
from collections import defaultdict
import numpy as np

class FinanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Configure styles
        self.setup_styles()
        
        # Initialize data
        self.categories = database.get_categories()
        
        # Create main interface
        self.create_main_interface()
        
        # Load dashboard data
        self.refresh_dashboard()
    
    def setup_styles(self):
        """Configure modern styling for the application"""
        style = ttk.Style()
        
        # Configure colors
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'light': '#ecf0f1',
            'dark': '#34495e'
        }
        
        # Configure ttk styles
        style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'), foreground=self.colors['primary'])
        style.configure('Heading.TLabel', font=('Helvetica', 12, 'bold'), foreground=self.colors['dark'])
        style.configure('Card.TFrame', background='white', relief='raised', borderwidth=1)
        style.configure('Primary.TButton', font=('Helvetica', 10, 'bold'))
        
    def create_main_interface(self):
        """Create the main application interface"""
        # Main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(0, weight=1)
        
        # Left sidebar
        self.create_sidebar(main_container)
        
        # Main content area
        self.create_main_content(main_container)
    
    def create_sidebar(self, parent):
        """Create the left sidebar with navigation"""
        sidebar = ttk.Frame(parent, style='Card.TFrame', padding="10")
        sidebar.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Title
        title_label = ttk.Label(sidebar, text="Finance Tracker", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Navigation buttons
        nav_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Add Income", self.show_add_income),
            ("Add Expense", self.show_add_expense),
            ("View Reports", self.show_reports),
            ("Budget Manager", self.show_budget_manager),
            ("Categories", self.show_categories)
        ]
        
        for i, (text, command) in enumerate(nav_buttons):
            btn = ttk.Button(sidebar, text=text, command=command, width=15)
            btn.grid(row=i+1, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # Quick stats
        self.create_quick_stats(sidebar, len(nav_buttons) + 2)
    
    def create_quick_stats(self, parent, start_row):
        """Create quick statistics display"""
        stats_frame = ttk.LabelFrame(parent, text="Quick Stats", padding="10")
        stats_frame.grid(row=start_row, column=0, pady=(20, 0), sticky=(tk.W, tk.E))
        
        self.stats_labels = {}
        stats = [
            ("Total Income", "income"),
            ("Total Expenses", "expenses"),
            ("Net Balance", "balance")
        ]
        
        for i, (label, key) in enumerate(stats):
            ttk.Label(stats_frame, text=f"{label}:", font=('Helvetica', 9, 'bold')).grid(row=i, column=0, sticky=tk.W)
            self.stats_labels[key] = ttk.Label(stats_frame, text="$0.00", foreground=self.colors['secondary'])
            self.stats_labels[key].grid(row=i, column=1, sticky=tk.E)
    
    def create_main_content(self, parent):
        """Create the main content area"""
        self.content_frame = ttk.Frame(parent)
        self.content_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        
        # Show dashboard by default
        self.show_dashboard()
    
    def clear_content(self):
        """Clear the main content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show the main dashboard"""
        self.clear_content()
        
        # Dashboard title
        title = ttk.Label(self.content_frame, text="Financial Dashboard", style='Title.TLabel')
        title.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # Create dashboard widgets
        self.create_dashboard_widgets()
    
    def create_dashboard_widgets(self):
        """Create dashboard widgets"""
        # Main dashboard frame
        dashboard = ttk.Frame(self.content_frame)
        dashboard.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        dashboard.columnconfigure(0, weight=1)
        dashboard.columnconfigure(1, weight=1)
        
        # Recent transactions
        self.create_recent_transactions(dashboard)
        
        # Expense visualization
        self.create_expense_chart(dashboard)
        
        # Monthly summary
        self.create_monthly_summary(dashboard)
    
    def create_recent_transactions(self, parent):
        """Create recent transactions display"""
        frame = ttk.LabelFrame(parent, text="Recent Transactions", padding="10")
        frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Treeview for transactions
        columns = ('Date', 'Type', 'Category', 'Description', 'Amount')
        self.transactions_tree = ttk.Treeview(frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.transactions_tree.heading(col, text=col)
            self.transactions_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.transactions_tree.yview)
        self.transactions_tree.configure(yscrollcommand=scrollbar.set)
        
        self.transactions_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        frame.columnconfigure(0, weight=1)
    
    def create_expense_chart(self, parent):
        """Create expense trend chart"""
        frame = ttk.LabelFrame(parent, text="Expense Trends (Last 30 Days)", padding="10")
        frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.fig.patch.set_facecolor('white')
        
        self.canvas = FigureCanvasTkAgg(self.fig, frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
    
    def create_monthly_summary(self, parent):
        """Create monthly summary"""
        frame = ttk.LabelFrame(parent, text="This Month Summary", padding="10")
        frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        self.summary_labels = {}
        summary_items = [
            ("Income", "monthly_income"),
            ("Expenses", "monthly_expenses"),
            ("Savings", "monthly_savings"),
            ("Top Category", "top_category")
        ]
        
        for i, (label, key) in enumerate(summary_items):
            ttk.Label(frame, text=f"{label}:", font=('Helvetica', 10, 'bold')).grid(row=i, column=0, sticky=tk.W, pady=5)
            self.summary_labels[key] = ttk.Label(frame, text="$0.00")
            self.summary_labels[key].grid(row=i, column=1, sticky=tk.E, pady=5)
        
        frame.columnconfigure(1, weight=1)
    
    def show_add_income(self):
        """Show add income form"""
        self.clear_content()
        
        title = ttk.Label(self.content_frame, text="Add Income", style='Title.TLabel')
        title.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # Form frame
        form_frame = ttk.LabelFrame(self.content_frame, text="Income Details", padding="20")
        form_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Form fields
        ttk.Label(form_frame, text="Amount:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.income_amount = ttk.Entry(form_frame, width=20)
        self.income_amount.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Label(form_frame, text="Source:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.income_source = ttk.Entry(form_frame, width=20)
        self.income_source.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Label(form_frame, text="Date:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.income_date = DateEntry(form_frame, width=18, background='darkblue',
                                   foreground='white', borderwidth=2)
        self.income_date.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        ttk.Label(form_frame, text="Description:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.income_description = tk.Text(form_frame, height=3, width=30)
        self.income_description.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Submit button
        submit_btn = ttk.Button(form_frame, text="Add Income", command=self.add_income,
                              style='Primary.TButton')
        submit_btn.grid(row=4, column=1, pady=20, sticky=tk.E)
        
        form_frame.columnconfigure(1, weight=1)
    
    def show_add_expense(self):
        """Show add expense form"""
        self.clear_content()
        
        title = ttk.Label(self.content_frame, text="Add Expense", style='Title.TLabel')
        title.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # Form frame
        form_frame = ttk.LabelFrame(self.content_frame, text="Expense Details", padding="20")
        form_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Form fields
        ttk.Label(form_frame, text="Amount:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.expense_amount = ttk.Entry(form_frame, width=20)
        self.expense_amount.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Label(form_frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.expense_category = ttk.Combobox(form_frame, width=18, state="readonly")
        self.expense_category['values'] = [cat['name'] for cat in self.categories]
        self.expense_category.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Label(form_frame, text="Date:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.expense_date = DateEntry(form_frame, width=18, background='darkblue',
                                    foreground='white', borderwidth=2)
        self.expense_date.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        ttk.Label(form_frame, text="Description:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.expense_description = tk.Text(form_frame, height=3, width=30)
        self.expense_description.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Submit button
        submit_btn = ttk.Button(form_frame, text="Add Expense", command=self.add_expense,
                              style='Primary.TButton')
        submit_btn.grid(row=4, column=1, pady=20, sticky=tk.E)
        
        form_frame.columnconfigure(1, weight=1)
    
    def show_reports(self):
        """Show financial reports"""
        self.clear_content()
        
        title = ttk.Label(self.content_frame, text="Financial Reports", style='Title.TLabel')
        title.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # Report controls
        controls_frame = ttk.Frame(self.content_frame)
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(controls_frame, text="Period:").grid(row=0, column=0, padx=(0, 10))
        
        self.report_period = ttk.Combobox(controls_frame, values=["Last 7 days", "Last 30 days", "Last 3 months", "Last year"], state="readonly")
        self.report_period.set("Last 30 days")
        self.report_period.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(controls_frame, text="Generate Report", command=self.generate_report).grid(row=0, column=2, padx=(10, 0))
        
        # Report content
        self.report_frame = ttk.Frame(self.content_frame)
        self.report_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.report_frame.columnconfigure(0, weight=1)
        self.report_frame.rowconfigure(0, weight=1)
        
        # Generate initial report
        self.generate_report()
    
    def show_budget_manager(self):
        """Show budget management interface"""
        self.clear_content()
        
        title = ttk.Label(self.content_frame, text="Budget Manager", style='Title.TLabel')
        title.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # Budget controls
        controls_frame = ttk.Frame(self.content_frame)
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Button(controls_frame, text="Set New Budget", command=self.set_budget).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(controls_frame, text="View Budget Status", command=self.view_budget_status).grid(row=0, column=1)
        
        # Budget display
        self.budget_frame = ttk.Frame(self.content_frame)
        self.budget_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.view_budget_status()
    
    def show_categories(self):
        """Show category management"""
        self.clear_content()
        
        title = ttk.Label(self.content_frame, text="Category Management", style='Title.TLabel')
        title.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # Categories list
        categories_frame = ttk.LabelFrame(self.content_frame, text="Categories", padding="10")
        categories_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Treeview for categories
        columns = ('Name', 'Color')
        self.categories_tree = ttk.Treeview(categories_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.categories_tree.heading(col, text=col)
            self.categories_tree.column(col, width=150)
        
        self.categories_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Load categories
        self.load_categories()
        
        categories_frame.columnconfigure(0, weight=1)
        categories_frame.rowconfigure(0, weight=1)
    
    def add_income(self):
        """Add income to database"""
        try:
            amount = float(self.income_amount.get())
            source = self.income_source.get()
            date_val = self.income_date.get_date()
            description = self.income_description.get("1.0", tk.END).strip()
            
            if not source:
                messagebox.showerror("Error", "Please enter income source")
                return
            
            result = database.add_income(amount, source, date_val, description)
            if result:
                messagebox.showinfo("Success", "Income added successfully!")
                self.clear_income_form()
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", "Failed to add income")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
    
    def add_expense(self):
        """Add expense to database"""
        try:
            amount = float(self.expense_amount.get())
            category_name = self.expense_category.get()
            date_val = self.expense_date.get_date()
            description = self.expense_description.get("1.0", tk.END).strip()
            
            if not category_name or not description:
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            # Find category ID
            category_id = None
            for cat in self.categories:
                if cat['name'] == category_name:
                    category_id = cat['id']
                    break
            
            if category_id is None:
                messagebox.showerror("Error", "Invalid category selected")
                return
            
            result = database.add_expense(amount, category_id, description, date_val)
            if result:
                messagebox.showinfo("Success", "Expense added successfully!")
                self.clear_expense_form()
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", "Failed to add expense")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
    
    def clear_income_form(self):
        """Clear income form fields"""
        self.income_amount.delete(0, tk.END)
        self.income_source.delete(0, tk.END)
        self.income_description.delete("1.0", tk.END)
        self.income_date.set_date(datetime.now().date())
    
    def clear_expense_form(self):
        """Clear expense form fields"""
        self.expense_amount.delete(0, tk.END)
        self.expense_category.set('')
        self.expense_description.delete("1.0", tk.END)
        self.expense_date.set_date(datetime.now().date())
    
    def refresh_dashboard(self):
        """Refresh dashboard data"""
        self.update_quick_stats()
        self.update_recent_transactions()
        self.update_expense_chart()
        self.update_monthly_summary()
    
    def update_quick_stats(self):
        """Update quick statistics"""
        # Get current month data
        today = datetime.now().date()
        start_of_month = today.replace(day=1)
        
        income_data = database.get_income_by_date_range(start_of_month, today)
        expense_data = database.get_expenses_by_date_range(start_of_month, today)
        
        total_income = sum(item['amount'] for item in income_data)
        total_expenses = sum(item['amount'] for item in expense_data)
        net_balance = total_income - total_expenses
        
        self.stats_labels['income'].config(text=f"${total_income:.2f}")
        self.stats_labels['expenses'].config(text=f"${total_expenses:.2f}")
        self.stats_labels['balance'].config(text=f"${net_balance:.2f}",
                                          foreground=self.colors['success'] if net_balance >= 0 else self.colors['danger'])
    
    def update_recent_transactions(self):
        """Update recent transactions display"""
        if not hasattr(self, 'transactions_tree'):
            return
            
        # Clear existing items
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)
        
        # Get recent data
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        income_data = database.get_income_by_date_range(start_date, end_date)
        expense_data = database.get_expenses_by_date_range(start_date, end_date)
        
        # Combine and sort transactions
        transactions = []
        
        for item in income_data:
            transactions.append({
                'date': item['date'],
                'type': 'Income',
                'category': item['source'],
                'description': item['description'] or '',
                'amount': f"+${item['amount']:.2f}"
            })
        
        for item in expense_data:
            transactions.append({
                'date': item['date'],
                'type': 'Expense',
                'category': item['category_name'] or 'Unknown',
                'description': item['description'],
                'amount': f"-${item['amount']:.2f}"
            })
        
        # Sort by date (newest first)
        transactions.sort(key=lambda x: x['date'], reverse=True)
        
        # Add to treeview (limit to 10 most recent)
        for transaction in transactions[:10]:
            self.transactions_tree.insert('', 'end', values=(
                transaction['date'].strftime('%Y-%m-%d'),
                transaction['type'],
                transaction['category'],
                transaction['description'][:30] + '...' if len(transaction['description']) > 30 else transaction['description'],
                transaction['amount']
            ))
    
    def update_expense_chart(self):
        """Update expense trend chart"""
        if not hasattr(self, 'ax'):
            return
            
        self.ax.clear()
        
        # Get last 30 days of expenses
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        expenses = database.get_expenses_by_date_range(start_date, end_date)
        
        if not expenses:
            self.ax.text(0.5, 0.5, 'No expense data available', 
                        horizontalalignment='center', verticalalignment='center',
                        transform=self.ax.transAxes)
        else:
            # Group expenses by date
            daily_expenses = defaultdict(float)
            for expense in expenses:
                daily_expenses[expense['date']] += float(expense['amount'])
            
            # Create date range
            dates = []
            amounts = []
            current_date = start_date
            
            while current_date <= end_date:
                dates.append(current_date)
                amounts.append(daily_expenses.get(current_date, 0))
                current_date += timedelta(days=1)
            
            self.ax.plot(dates, amounts, marker='o', linewidth=2, markersize=4, color=self.colors['secondary'])
            self.ax.set_title('Daily Expenses (Last 30 Days)')
            self.ax.set_xlabel('Date')
            self.ax.set_ylabel('Amount ($)')
            self.ax.grid(True, alpha=0.3)
            
            # Format x-axis
            self.ax.tick_params(axis='x', rotation=45)
        
        self.fig.tight_layout()
        self.canvas.draw()
    
    def update_monthly_summary(self):
        """Update monthly summary"""
        if not hasattr(self, 'summary_labels'):
            return
            
        # Get current month data
        today = datetime.now().date()
        start_of_month = today.replace(day=1)
        
        income_data = database.get_income_by_date_range(start_of_month, today)
        expense_data = database.get_expenses_by_date_range(start_of_month, today)
        
        monthly_income = sum(item['amount'] for item in income_data)
        monthly_expenses = sum(item['amount'] for item in expense_data)
        monthly_savings = monthly_income - monthly_expenses
        
        # Find top expense category
        category_totals = defaultdict(float)
        for expense in expense_data:
            category_name = expense['category_name'] or 'Unknown'
            category_totals[category_name] += float(expense['amount'])
        
        top_category = max(category_totals.items(), key=lambda x: x[1])[0] if category_totals else "None"
        
        self.summary_labels['monthly_income'].config(text=f"${monthly_income:.2f}")
        self.summary_labels['monthly_expenses'].config(text=f"${monthly_expenses:.2f}")
        self.summary_labels['monthly_savings'].config(text=f"${monthly_savings:.2f}",
                                                    foreground=self.colors['success'] if monthly_savings >= 0 else self.colors['danger'])
        self.summary_labels['top_category'].config(text=top_category)
    
    def generate_report(self):
        """Generate financial report"""
        # Clear existing report
        for widget in self.report_frame.winfo_children():
            widget.destroy()
        
        # Get date range based on selection
        period = self.report_period.get()
        end_date = datetime.now().date()
        
        if period == "Last 7 days":
            start_date = end_date - timedelta(days=7)
        elif period == "Last 30 days":
            start_date = end_date - timedelta(days=30)
        elif period == "Last 3 months":
            start_date = end_date - timedelta(days=90)
        else:  # Last year
            start_date = end_date - timedelta(days=365)
        
        # Get data
        income_data = database.get_income_by_date_range(start_date, end_date)
        expense_data = database.get_expenses_by_date_range(start_date, end_date)
        
        # Create report
        report_text = tk.Text(self.report_frame, wrap=tk.WORD, height=20)
        report_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.report_frame, orient=tk.VERTICAL, command=report_text.yview)
        report_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Generate report content
        total_income = sum(item['amount'] for item in income_data)
        total_expenses = sum(item['amount'] for item in expense_data)
        net_savings = total_income - total_expenses
        
        report_content = f"""
FINANCIAL REPORT - {period}
Period: {start_date} to {end_date}
{'='*50}

SUMMARY:
Total Income: ${total_income:.2f}
Total Expenses: ${total_expenses:.2f}
Net Savings: ${net_savings:.2f}

INCOME BREAKDOWN:
"""
        
        # Income sources
        income_sources = defaultdict(float)
        for item in income_data:
            income_sources[item['source']] += float(item['amount'])
        
        for source, amount in sorted(income_sources.items(), key=lambda x: x[1], reverse=True):
            report_content += f"  {source}: ${amount:.2f}\n"
        
        report_content += "\nEXPENSE BREAKDOWN:\n"
        
        # Expense categories
        expense_categories = defaultdict(float)
        for item in expense_data:
            category = item['category_name'] or 'Unknown'
            expense_categories[category] += float(item['amount'])
        
        for category, amount in sorted(expense_categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
            report_content += f"  {category}: ${amount:.2f} ({percentage:.1f}%)\n"
        
        report_text.insert(tk.END, report_content)
        report_text.config(state=tk.DISABLED)
    
    def set_budget(self):
        """Set budget for a category"""
        # Simple budget setting dialog
        category_names = [cat['name'] for cat in self.categories]
        
        if not category_names:
            messagebox.showwarning("Warning", "No categories available")
            return
        
        # Create budget dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Set Budget")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Category:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(dialog, textvariable=category_var, values=category_names, state="readonly")
        category_combo.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Monthly Budget:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        budget_var = tk.StringVar()
        budget_entry = ttk.Entry(dialog, textvariable=budget_var)
        budget_entry.grid(row=1, column=1, padx=10, pady=10)
        
        def save_budget():
            try:
                category_name = category_var.get()
                budget_amount = float(budget_var.get())
                
                if not category_name:
                    messagebox.showerror("Error", "Please select a category")
                    return
                
                # Find category ID
                category_id = None
                for cat in self.categories:
                    if cat['name'] == category_name:
                        category_id = cat['id']
                        break
                
                # Save budget (simplified - using current month/year)
                today = datetime.now()
                db = database.get_db()
                if db:
                    query = """
                    INSERT INTO budgets (category_id, amount, month, year) 
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE amount = VALUES(amount)
                    """
                    db.execute_query(query, (category_id, budget_amount, today.month, today.year))
                    db.close_connection()
                    
                    messagebox.showinfo("Success", "Budget set successfully!")
                    dialog.destroy()
                    self.view_budget_status()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid budget amount")
        
        ttk.Button(dialog, text="Save", command=save_budget).grid(row=2, column=1, padx=10, pady=20)
    
    def view_budget_status(self):
        """View current budget status"""
        # Clear existing widgets
        for widget in self.budget_frame.winfo_children():
            widget.destroy()
        
        # Get current month budgets
        today = datetime.now()
        db = database.get_db()
        if not db:
            return
        
        query = """
        SELECT b.amount as budget_amount, c.name as category_name, c.color,
               COALESCE(SUM(e.amount), 0) as spent_amount
        FROM budgets b
        JOIN categories c ON b.category_id = c.id
        LEFT JOIN expenses e ON e.category_id = c.id 
                             AND MONTH(e.date) = %s 
                             AND YEAR(e.date) = %s
        WHERE b.month = %s AND b.year = %s
        GROUP BY b.id, c.name, c.color, b.amount
        """
        
        budgets = db.execute_query(query, (today.month, today.year, today.month, today.year))
        db.close_connection()
        
        if not budgets:
            ttk.Label(self.budget_frame, text="No budgets set for this month").grid(row=0, column=0, padx=20, pady=20)
            return
        
        # Create budget status display
        for i, budget in enumerate(budgets):
            frame = ttk.LabelFrame(self.budget_frame, text=budget['category_name'], padding="10")
            frame.grid(row=i//2, column=i%2, padx=10, pady=10, sticky=(tk.W, tk.E))
            
            budget_amount = float(budget['budget_amount'])
            spent_amount = float(budget['spent_amount'])
            remaining = budget_amount - spent_amount
            percentage = (spent_amount / budget_amount * 100) if budget_amount > 0 else 0
            
            ttk.Label(frame, text=f"Budget: ${budget_amount:.2f}").grid(row=0, column=0, sticky=tk.W)
            ttk.Label(frame, text=f"Spent: ${spent_amount:.2f}").grid(row=1, column=0, sticky=tk.W)
            ttk.Label(frame, text=f"Remaining: ${remaining:.2f}").grid(row=2, column=0, sticky=tk.W)
            
            # Progress bar
            progress = ttk.Progressbar(frame, length=200, mode='determinate')
            progress.grid(row=3, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
            progress['value'] = min(percentage, 100)
            
            # Status label
            status_color = self.colors['success'] if percentage <= 80 else self.colors['warning'] if percentage <= 100 else self.colors['danger']
            status_text = f"{percentage:.1f}% used"
            status_label = ttk.Label(frame, text=status_text)
            status_label.grid(row=4, column=0, pady=(5, 0))
        
        self.budget_frame.columnconfigure(0, weight=1)
        self.budget_frame.columnconfigure(1, weight=1)
    
    def load_categories(self):
        """Load categories into treeview"""
        if not hasattr(self, 'categories_tree'):
            return
            
        # Clear existing items
        for item in self.categories_tree.get_children():
            self.categories_tree.delete(item)
        
        # Add categories
        for category in self.categories:
            self.categories_tree.insert('', 'end', values=(
                category['name'],
                category['color']
            ))

def main():
    # Test database connection
    db = database.get_db()
    if not db:
        messagebox.showerror("Database Error", 
                           "Could not connect to MySQL database. Please ensure MySQL is running and check your connection settings in database.py")
        return
    db.close_connection()
    
    # Create and run application
    root = tk.Tk()
    app = FinanceTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()