# 💰 Expense Tracker CLI with SQL — Financial Console

A powerful command-line financial management application built with Python and MySQL. This utility helps you track, analyze, and budget personal finances directly from the terminal, using parameterized SQL queries for security and environment configuration files for credentials.

---

## 🖥️ Terminal Interface Preview

The console interface utilizes unicode boxes and text-based analytics charts for clear, distraction-free viewing:

### Main Dashboard
```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║      💰  E X P E N S E   T R A C K E R   v2.0  💰       ║
║         ─── Powered by Python & MySQL ───                 ║
║                                                           ║
╠═══════════════════════════════════════════════════════════╣
║   Track · Analyze · Budget · Export                       ║
╚═══════════════════════════════════════════════════════════╝
```

### Visual Category Aggregation
```
   ┌─────────────────────────────────────────────────────────────────┐
   │                  📊 CATEGORY-WISE BREAKDOWN                    │
   └─────────────────────────────────────────────────────────────────┘
   Food            ██████████████████████░░░  ₹12,450.00  (14 txns, 42.5%)
   Bills           ██████████████░░░░░░░░░░░  ₹8,200.00   (4 txns,  28.0%)
   Transport       ███████░░░░░░░░░░░░░░░░░░  ₹3,150.00   (9 txns,  10.7%)
   Entertainment   ████░░░░░░░░░░░░░░░░░░░░░  ₹2,100.00   (3 txns,   7.2%)
```

### Paginated Transactions Log
```
┌──────┬────────────┬───────────┬────────────┬─────────────────────────────┐
│ ID   │ Category   │ Amount    │ Date       │ Note                        │
├──────┼────────────┼───────────┼────────────┼─────────────────────────────┤
│ 42   │ Food       │ ₹450.00   │ 2026-06-09 │ Team dinner                 │
│ 41   │ Bills      │ ₹3,200.00 │ 2026-06-08 │ Internet bill (unlimited)   │
│ 40   │ Transport  │ ₹120.00   │ 2026-06-08 │ Metro ride                  │
└──────┴────────────┴───────────┴────────────┴─────────────────────────────┘
  Page 1 of 5 (12 total expenses)  --  [N] Next  [P] Previous  [Q] Quit
```

---

## ✨ Features

* **Full Transaction CRUD**: Create, read, update, and delete expenses with double-verification deletion prompts.
* **Smart Page Navigation**: Browses extensive transaction histories using paginated data grids (10 rows per page) in the console.
* **Monthly Budget Monitor**: Set monthly spending limits. The console flags target months with color-coded alerts if expenditures breach limits:
  ```
  🚨 OVER BUDGET by ₹1,450.00  (Budget: ₹10,000.00)
  ```
* **Text-Based Analytics Bar Charts**: Generates graphical summaries of monthly and category-wise spending patterns using dynamic text bars.
* **Data Filters**: Instantly filters records by category (case-insensitive) or specific calendar date ranges.
* **Automated CSV Backup**: Exports all transaction records to timestamped CSV sheets stored in an auto-created `exports/` folder.
* **Secure Database Configuration**: Isolates sensitive MySQL database credentials using environment files (`.env`).
* **SQL Injection Shield**: Formulates all database calls using parameterized queries (`%s` markers).

---

## 🧰 Tech Stack

* **Language**: Python 3.x
* **Database**: MySQL Server 8.0+
* **Drivers**: `mysql-connector-python`
* **Configuration**: `python-dotenv`
* **Output Formatting**: `tabulate` (Fancy grid layout)

---

## 🗄️ Database Architecture

The system utilizes two normalized relational database tables:

```
expense_tracker (Database)
├── expenses (Table)
│   ├── id (INT, AUTO_INCREMENT, PRIMARY KEY)
│   ├── category (VARCHAR 50)
│   ├── amount (DECIMAL 10,2)
│   ├── date (DATE)
│   └── note (VARCHAR 255)
│
└── budgets (Table)
    ├── id (INT, AUTO_INCREMENT, PRIMARY KEY)
    ├── month (VARCHAR 7, UNIQUE) - Format: YYYY-MM
    └── amount (DECIMAL 10,2)
```

---

## 📦 How to Run

### Prerequisites
* Python 3.x installed.
* MySQL Server instance running locally or remotely.

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/vijaybarhate/expense-tracker-sql.git
   cd expense-tracker-sql
   ```

2. **Install Required Libraries**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database Credentials**
   Create a `.env` file in the root of the project:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password_here
   DB_NAME=expense_tracker
   ```

4. **Initialize & Run**
   Execute the application. The system will automatically detect if the tables are missing and initialize them for you:
   ```bash
   python expense_tracker.py
   ```

---

## 🧠 Challenges Faced

* **Preventing SQL Injections**: Dynamic search options (like category-wise searches) require variables in SQL queries. Instead of using string formatting (which is prone to security risks), we carefully structured our logic to separate SQL schemas from data inputs, passing inputs solely as tuple parameters.
* **Paginated Console Grid**: Standard Python script outputs print all records at once, cluttering the terminal. We engineered a console pagination loop that slices query results, yielding exactly 10 lines per screen, and accepts character inputs (`n`/`p`/`q`) to navigate pages dynamically.
* **State Checking & Database Synchronization**: Checking budgets requires querying expenditures for a specific month. We formulated SQL aggregations using the database engine's native `DATE_FORMAT(date, '%Y-%m')` function, moving calculations server-side to keep execution times fast.

---

## 🔮 Future Improvements

- [ ] **Graphical User Interface (GUI)**: Build a desktop interface using Tkinter or PyQt for easier visualization.
- [ ] **Sub-Category Support**: Enable detailed categories (e.g. food -> groceries, restaurants).
- [ ] **Automatic Category Prediction**: Use basic machine learning (Naive Bayes) to predict transaction categories from notes/merchant descriptions.

---

Built with 🖤 by [Vijay Barhate](https://github.com/vijaybarhate)
