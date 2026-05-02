# 💰 Expense Tracker with SQL

A command-line expense tracking application built with Python and MySQL that helps manage and analyze personal expenses.

---

## 🚀 Features

- ➕ Add expenses with category, amount, date and notes
- 📋 View all expenses in a formatted table
- 🗑️ Delete expenses by ID
- 📊 Summary with total spent and category-wise breakdown
- 📅 Monthly spending breakdown
- 🔍 Search expenses by category
- 💾 All data persisted in MySQL database

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)

---

## 📦 How to Run

1. Clone the repository
2. Install dependency:
```
pip install mysql-connector-python
```
3. Set up MySQL database:
```sql
CREATE DATABASE expense_tracker;
USE expense_tracker;
CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    date DATE NOT NULL,
    note VARCHAR(255)
);
```
4. Update your MySQL password in `expense_tracker.py`
5. Run:
```
python expense_tracker.py
```

---

## 📄 License

Open source for educational use.
