# 💰 Expense Tracker with SQL

A powerful **command-line Expense Tracker** built with **Python** and **MySQL** that helps you track, analyze, and manage your personal finances — right from the terminal.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ➕ **Add Expense** | Log expenses with category, amount, date, and optional notes |
| 📋 **View Expenses** | Browse all expenses with **paginated** table view |
| ✏️ **Update Expense** | Edit any field of an existing expense |
| 🗑️ **Delete Expense** | Remove expenses with **confirmation prompt** |
| 📊 **Summary & Analytics** | View total spending, averages, highs/lows, and **visual bar charts** |
| 🔍 **Search by Category** | Filter and view expenses by category (case-insensitive) |
| 📅 **Date Range Filter** | View expenses between two specific dates |
| 💵 **Monthly Budget** | Set monthly spending limits and get **over-budget warnings** |
| 📤 **Export to CSV** | Export all expenses to a timestamped CSV file |

---

## 🛠️ Technologies Used

- **Python 3.x** — Core application logic
- **MySQL 8.0** — Database for persistent storage
- **mysql-connector-python** — MySQL driver for Python
- **python-dotenv** — Secure credential management via `.env`
- **tabulate** — Beautiful terminal table formatting

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/expense-tracker-sql.git
cd expense-tracker-sql
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up MySQL Database

Open MySQL and create the database:

```sql
CREATE DATABASE expense_tracker;
```

> **Note:** The application will automatically create the required tables (`expenses`, `budgets`) when you run it for the first time.

### 4. Configure Environment Variables

Create a `.env` file in the project root (or edit the existing one):

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=expense_tracker
```

### 5. Run the Application

```bash
python expense_tracker.py
```

---

## 🚀 Usage

When you launch the app, you'll see a styled main menu:

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

Simply enter the number of the option you want and follow the prompts.

### Quick Examples

**Adding an expense:**
> Select category → Enter amount → Enter date (or press Enter for today) → Add a note

**Viewing the summary:**
> See total spending, category-wise bar charts, monthly breakdowns, and budget status

**Exporting data:**
> All expenses are saved as a `.csv` file inside the `exports/` folder

---

## 📁 Project Structure

```
Expense Tracker with SQL/
├── expense_tracker.py    # Main application
├── requirements.txt      # Python dependencies
├── .env                  # Database credentials (not committed)
├── .gitignore            # Git ignore rules
├── exports/              # CSV export folder (auto-created)
└── README.md             # This file
```

---

## 🔒 Security

- Database credentials are stored in a `.env` file, **not hardcoded**
- `.env` is included in `.gitignore` to prevent accidental commits
- All SQL queries use **parameterized statements** to prevent SQL injection

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> Built with ❤️ using Python & MySQL
