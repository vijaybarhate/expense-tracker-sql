import mysql.connector
from datetime import date, datetime
from dotenv import load_dotenv
from tabulate import tabulate
import csv
import os
import sys

# ── Load Environment Variables ────────────────────────────
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "expense_tracker")

VALID_CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Education", "Other"]
PAGE_SIZE = 10  # Number of expenses to display per page

# ── Connect to Database ────────────────────────────────────
def connect_db():
    """Establish a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as e:
        print(f"\n❌ Database Connection Failed!")
        print(f"   Error: {e}")
        print(f"\n💡 Make sure MySQL is running and your .env file has correct credentials.")
        print(f"   Host: {DB_HOST} | User: {DB_USER} | Database: {DB_NAME}")
        sys.exit(1)


def initialize_db(cursor):
    """Create required tables if they don't already exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(50) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            date DATE NOT NULL,
            note VARCHAR(255)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            month VARCHAR(7) NOT NULL UNIQUE,
            amount DECIMAL(10, 2) NOT NULL
        )
    """)


# ── Helper Functions ──────────────────────────────────────

def get_valid_amount(prompt="Amount (₹): "):
    """Prompt the user for a valid positive number."""
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print("❌ Amount must be greater than zero.")
                continue
            return amount
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")


def get_valid_date(prompt="Date (YYYY-MM-DD) or press Enter for today: "):
    """Prompt the user for a valid date in YYYY-MM-DD format."""
    while True:
        date_input = input(prompt).strip()
        if not date_input:
            return str(date.today())
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            return date_input
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD.")


def get_valid_id(prompt="Enter ID: "):
    """Prompt the user for a valid integer ID."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("❌ Invalid input. Please enter a valid ID number.")


def get_category():
    """Prompt the user to select a valid category."""
    print(f"\n   Available Categories:")
    for i, cat in enumerate(VALID_CATEGORIES, 1):
        print(f"   {i}. {cat}")
    while True:
        choice = input(f"   Select category (1-{len(VALID_CATEGORIES)}): ").strip()
        try:
            idx = int(choice)
            if 1 <= idx <= len(VALID_CATEGORIES):
                return VALID_CATEGORIES[idx - 1]
            else:
                print(f"❌ Please enter a number between 1 and {len(VALID_CATEGORIES)}.")
        except ValueError:
            print(f"❌ Invalid input. Enter a number between 1 and {len(VALID_CATEGORIES)}.")


def display_expenses_table(rows):
    """Display a list of expense rows as a formatted table."""
    if not rows:
        print("   No expenses found.")
        return
    table_data = []
    for row in rows:
        table_data.append([
            row[0],
            row[1],
            f"₹{row[2]:,.2f}",
            str(row[3]),
            row[4] or ""
        ])
    headers = ["ID", "Category", "Amount", "Date", "Note"]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid", stralign="left", numalign="left"))


def build_bar(value, max_value, bar_length=25):
    """Build a Unicode progress bar."""
    if max_value == 0:
        return "░" * bar_length
    filled = int((value / max_value) * bar_length)
    filled = min(filled, bar_length)
    return "▓" * filled + "░" * (bar_length - filled)


# ── Core Features ──────────────────────────────────────────

def add_expense(cursor, conn):
    """Add a new expense record."""
    print("\n╔══════════════════════════════════════╗")
    print("║         ➕ ADD NEW EXPENSE           ║")
    print("╚══════════════════════════════════════╝")

    category = get_category()
    amount = get_valid_amount()
    expense_date = get_valid_date()
    note = input("   Note (optional): ").strip()

    try:
        cursor.execute(
            "INSERT INTO expenses (category, amount, date, note) VALUES (%s, %s, %s, %s)",
            (category, amount, expense_date, note)
        )
        conn.commit()
        print(f"\n   ✅ Expense of ₹{amount:,.2f} added under '{category}' on {expense_date}!")
    except mysql.connector.Error as e:
        print(f"\n   ❌ Failed to add expense: {e}")


def view_expenses(cursor):
    """View all expenses with pagination."""
    print("\n╔══════════════════════════════════════╗")
    print("║         📋 ALL EXPENSES              ║")
    print("╚══════════════════════════════════════╝")

    cursor.execute("SELECT COUNT(*) FROM expenses")
    total_count = cursor.fetchone()[0]

    if total_count == 0:
        print("\n   No expenses found. Start by adding one!")
        return

    total_pages = (total_count + PAGE_SIZE - 1) // PAGE_SIZE
    current_page = 1

    while True:
        offset = (current_page - 1) * PAGE_SIZE
        cursor.execute(
            "SELECT * FROM expenses ORDER BY date DESC LIMIT %s OFFSET %s",
            (PAGE_SIZE, offset)
        )
        rows = cursor.fetchall()

        print(f"\n   📄 Page {current_page} of {total_pages}  ({total_count} total expenses)\n")
        display_expenses_table(rows)

        if total_pages <= 1:
            break

        print(f"\n   [N] Next  [P] Previous  [Q] Quit")
        nav = input("   Navigate: ").strip().lower()

        if nav == "n" and current_page < total_pages:
            current_page += 1
        elif nav == "p" and current_page > 1:
            current_page -= 1
        elif nav == "q":
            break
        elif nav == "n" and current_page >= total_pages:
            print("   ⚠️  Already on the last page.")
        elif nav == "p" and current_page <= 1:
            print("   ⚠️  Already on the first page.")


def update_expense(cursor, conn):
    """Update an existing expense record."""
    print("\n╔══════════════════════════════════════╗")
    print("║         ✏️  UPDATE EXPENSE            ║")
    print("╚══════════════════════════════════════╝")

    exp_id = get_valid_id("   Enter ID of expense to update: ")

    cursor.execute("SELECT * FROM expenses WHERE id = %s", (exp_id,))
    row = cursor.fetchone()

    if not row:
        print(f"\n   ❌ Expense ID {exp_id} not found.")
        return

    print(f"\n   Current Details:")
    display_expenses_table([row])

    print(f"\n   Leave blank to keep current value.\n")

    # Category
    print(f"   Current Category: {row[1]}")
    change_cat = input("   Change category? (y/n): ").strip().lower()
    if change_cat == "y":
        new_category = get_category()
    else:
        new_category = row[1]

    # Amount
    amount_input = input(f"   New Amount (current: ₹{row[2]:,.2f}): ").strip()
    if amount_input:
        try:
            new_amount = float(amount_input)
            if new_amount <= 0:
                print("   ⚠️  Invalid amount. Keeping current value.")
                new_amount = float(row[2])
        except ValueError:
            print("   ⚠️  Invalid input. Keeping current value.")
            new_amount = float(row[2])
    else:
        new_amount = float(row[2])

    # Date
    date_input = input(f"   New Date (current: {row[3]}, format YYYY-MM-DD): ").strip()
    if date_input:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            new_date = date_input
        except ValueError:
            print("   ⚠️  Invalid date. Keeping current value.")
            new_date = str(row[3])
    else:
        new_date = str(row[3])

    # Note
    note_input = input(f"   New Note (current: {row[4] or 'None'}): ").strip()
    new_note = note_input if note_input else row[4]

    try:
        cursor.execute(
            "UPDATE expenses SET category=%s, amount=%s, date=%s, note=%s WHERE id=%s",
            (new_category, new_amount, new_date, new_note, exp_id)
        )
        conn.commit()
        print(f"\n   ✅ Expense ID {exp_id} updated successfully!")
    except mysql.connector.Error as e:
        print(f"\n   ❌ Failed to update expense: {e}")


def delete_expense(cursor, conn):
    """Delete an expense with confirmation."""
    print("\n╔══════════════════════════════════════╗")
    print("║         🗑️  DELETE EXPENSE            ║")
    print("╚══════════════════════════════════════╝")

    exp_id = get_valid_id("   Enter ID of expense to delete: ")

    cursor.execute("SELECT * FROM expenses WHERE id = %s", (exp_id,))
    row = cursor.fetchone()

    if not row:
        print(f"\n   ❌ Expense ID {exp_id} not found.")
        return

    print(f"\n   Expense to delete:")
    display_expenses_table([row])

    confirm = input("\n   ⚠️  Are you sure you want to delete this? (yes/no): ").strip().lower()
    if confirm in ("yes", "y"):
        try:
            cursor.execute("DELETE FROM expenses WHERE id = %s", (exp_id,))
            conn.commit()
            print(f"\n   ✅ Expense ID {exp_id} deleted!")
        except mysql.connector.Error as e:
            print(f"\n   ❌ Failed to delete: {e}")
    else:
        print("   ↩️  Deletion cancelled.")


def summary(cursor):
    """Display spending summary with visual bar charts."""
    print("\n╔══════════════════════════════════════╗")
    print("║       📊 SUMMARY & ANALYTICS         ║")
    print("╚══════════════════════════════════════╝")

    # Total spent
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0
    print(f"\n   💰 Total Spent: ₹{total:,.2f}")

    # Total transactions
    cursor.execute("SELECT COUNT(*) FROM expenses")
    count = cursor.fetchone()[0]
    print(f"   📝 Total Transactions: {count}")

    if count == 0:
        return

    # Average expense
    print(f"   📈 Average Expense: ₹{total / count:,.2f}")

    # Highest & Lowest
    cursor.execute("SELECT category, amount, date FROM expenses ORDER BY amount DESC LIMIT 1")
    highest = cursor.fetchone()
    cursor.execute("SELECT category, amount, date FROM expenses ORDER BY amount ASC LIMIT 1")
    lowest = cursor.fetchone()
    print(f"   🔺 Highest: ₹{highest[1]:,.2f} ({highest[0]}, {highest[2]})")
    print(f"   🔻 Lowest:  ₹{lowest[1]:,.2f} ({lowest[0]}, {lowest[2]})")

    # Category breakdown with bar chart
    print("\n   ┌─────────────────────────────────────────────────────────────────┐")
    print("   │                  📊 CATEGORY-WISE BREAKDOWN                    │")
    print("   └─────────────────────────────────────────────────────────────────┘")
    cursor.execute(
        "SELECT category, SUM(amount), COUNT(*) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC"
    )
    rows = cursor.fetchall()

    max_amount = float(rows[0][1]) if rows else 0

    for row in rows:
        cat_name = row[0]
        cat_total = float(row[1])
        cat_count = row[2]
        percentage = (cat_total / float(total)) * 100 if total else 0
        bar = build_bar(cat_total, max_amount)
        print(f"   {cat_name:<15} {bar}  ₹{cat_total:>10,.2f}  ({cat_count} txns, {percentage:>5.1f}%)")

    # Monthly breakdown
    print("\n   ┌─────────────────────────────────────────────────────────────────┐")
    print("   │                    📅 MONTHLY BREAKDOWN                        │")
    print("   └─────────────────────────────────────────────────────────────────┘")
    cursor.execute(
        "SELECT DATE_FORMAT(date, '%%Y-%%m') as month, SUM(amount), COUNT(*) FROM expenses GROUP BY month ORDER BY month DESC"
    )
    monthly_rows = cursor.fetchall()
    max_monthly = max(float(r[1]) for r in monthly_rows) if monthly_rows else 0

    for row in monthly_rows:
        month_name = row[0]
        month_total = float(row[1])
        month_count = row[2]
        bar = build_bar(month_total, max_monthly)
        print(f"   {month_name:<10} {bar}  ₹{month_total:>10,.2f}  ({month_count} txns)")

        # Budget check for this month
        cursor.execute("SELECT amount FROM budgets WHERE month = %s", (month_name,))
        budget_row = cursor.fetchone()
        if budget_row:
            budget_amt = float(budget_row[0])
            if month_total > budget_amt:
                print(f"              🚨 OVER BUDGET by ₹{month_total - budget_amt:,.2f}  (Budget: ₹{budget_amt:,.2f})")
            else:
                remaining = budget_amt - month_total
                print(f"              ✅ Under budget — ₹{remaining:,.2f} remaining  (Budget: ₹{budget_amt:,.2f})")


def search_by_category(cursor):
    """Search expenses by category (case-insensitive)."""
    print("\n╔══════════════════════════════════════╗")
    print("║       🔍 SEARCH BY CATEGORY          ║")
    print("╚══════════════════════════════════════╝")

    category = get_category()

    cursor.execute(
        "SELECT * FROM expenses WHERE LOWER(category) = LOWER(%s) ORDER BY date DESC",
        (category,)
    )
    rows = cursor.fetchall()

    if not rows:
        print(f"\n   No expenses found for category '{category}'.")
        return

    # Category total
    total = sum(float(row[2]) for row in rows)
    print(f"\n   Found {len(rows)} expense(s) under '{category}'  |  Total: ₹{total:,.2f}\n")
    display_expenses_table(rows)


def filter_by_date(cursor):
    """Filter expenses between two dates."""
    print("\n╔══════════════════════════════════════╗")
    print("║       📅 FILTER BY DATE RANGE        ║")
    print("╚══════════════════════════════════════╝")

    print("\n   Enter the date range to filter expenses:")
    start_date = get_valid_date("   Start Date (YYYY-MM-DD): ")
    end_date = get_valid_date("   End Date   (YYYY-MM-DD): ")

    if start_date > end_date:
        print("   ⚠️  Start date is after end date. Swapping them.")
        start_date, end_date = end_date, start_date

    cursor.execute(
        "SELECT * FROM expenses WHERE date BETWEEN %s AND %s ORDER BY date DESC",
        (start_date, end_date)
    )
    rows = cursor.fetchall()

    if not rows:
        print(f"\n   No expenses found between {start_date} and {end_date}.")
        return

    total = sum(float(row[2]) for row in rows)
    print(f"\n   📆 {start_date} → {end_date}  |  {len(rows)} expense(s)  |  Total: ₹{total:,.2f}\n")
    display_expenses_table(rows)


def set_budget(cursor, conn):
    """Set a monthly spending budget."""
    print("\n╔══════════════════════════════════════╗")
    print("║       💵 SET MONTHLY BUDGET          ║")
    print("╚══════════════════════════════════════╝")

    current_month = date.today().strftime("%Y-%m")
    month_input = input(f"   Month (YYYY-MM) or press Enter for current ({current_month}): ").strip()

    if month_input:
        try:
            datetime.strptime(month_input + "-01", "%Y-%m-%d")
            target_month = month_input
        except ValueError:
            print("   ❌ Invalid month format. Use YYYY-MM.")
            return
    else:
        target_month = current_month

    # Show current budget if exists
    cursor.execute("SELECT amount FROM budgets WHERE month = %s", (target_month,))
    existing = cursor.fetchone()
    if existing:
        print(f"   ℹ️  Current budget for {target_month}: ₹{existing[0]:,.2f}")

    budget_amount = get_valid_amount("   Enter budget amount (₹): ")

    try:
        cursor.execute(
            "INSERT INTO budgets (month, amount) VALUES (%s, %s) ON DUPLICATE KEY UPDATE amount = %s",
            (target_month, budget_amount, budget_amount)
        )
        conn.commit()
        print(f"\n   ✅ Budget for {target_month} set to ₹{budget_amount:,.2f}")

        # Show current spending for that month
        cursor.execute(
            "SELECT SUM(amount) FROM expenses WHERE DATE_FORMAT(date, '%%Y-%%m') = %s",
            (target_month,)
        )
        spent = cursor.fetchone()[0] or 0
        remaining = budget_amount - float(spent)
        if remaining >= 0:
            print(f"   📊 Spent so far: ₹{spent:,.2f}  |  Remaining: ₹{remaining:,.2f}")
        else:
            print(f"   🚨 Spent so far: ₹{spent:,.2f}  |  OVER BUDGET by ₹{abs(remaining):,.2f}!")

    except mysql.connector.Error as e:
        print(f"\n   ❌ Failed to set budget: {e}")


def export_csv(cursor):
    """Export all expenses to a CSV file."""
    print("\n╔══════════════════════════════════════╗")
    print("║         📤 EXPORT TO CSV             ║")
    print("╚══════════════════════════════════════╝")

    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()

    if not rows:
        print("\n   No expenses to export.")
        return

    # Create exports directory if it doesn't exist
    os.makedirs("exports", exist_ok=True)

    filename = f"exports/expenses_{date.today().strftime('%Y%m%d_%H%M%S')}.csv"

    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Category", "Amount", "Date", "Note"])
            for row in rows:
                writer.writerow([row[0], row[1], float(row[2]), str(row[3]), row[4] or ""])

        print(f"\n   ✅ Exported {len(rows)} expenses to '{filename}'")
        print(f"   📂 File size: {os.path.getsize(filename):,} bytes")
    except IOError as e:
        print(f"\n   ❌ Export failed: {e}")


# ── Main Menu ──────────────────────────────────────────────

BANNER = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║      💰  E X P E N S E   T R A C K E R   v2.0  💰       ║
║         ─── Powered by Python & MySQL ───                 ║
║                                                           ║
╠═══════════════════════════════════════════════════════════╣
║   Track · Analyze · Budget · Export                       ║
╚═══════════════════════════════════════════════════════════╝
"""

MENU = """
   ┌─────────────────────────────────┐
   │         📌 MAIN MENU            │
   ├─────────────────────────────────┤
   │  1.  ➕  Add Expense            │
   │  2.  📋  View All Expenses      │
   │  3.  ✏️   Update Expense         │
   │  4.  🗑️   Delete Expense         │
   │  5.  📊  Summary & Analytics    │
   │  6.  🔍  Search by Category     │
   │  7.  📅  Filter by Date Range   │
   │  8.  💵  Set Monthly Budget     │
   │  9.  📤  Export to CSV          │
   │  0.  👋  Exit                   │
   └─────────────────────────────────┘
"""


def main():
    print(BANNER)

    conn = connect_db()
    cursor = conn.cursor()

    try:
        initialize_db(cursor)
        conn.commit()

        while True:
            print(MENU)
            choice = input("   Enter choice (0-9): ").strip()

            if choice == "1":
                add_expense(cursor, conn)
            elif choice == "2":
                view_expenses(cursor)
            elif choice == "3":
                update_expense(cursor, conn)
            elif choice == "4":
                delete_expense(cursor, conn)
            elif choice == "5":
                summary(cursor)
            elif choice == "6":
                search_by_category(cursor)
            elif choice == "7":
                filter_by_date(cursor)
            elif choice == "8":
                set_budget(cursor, conn)
            elif choice == "9":
                export_csv(cursor)
            elif choice == "0":
                print("\n   👋 Goodbye! Keep tracking your expenses!")
                break
            else:
                print("   ❌ Invalid choice. Please enter a number from 0-9.")

    except KeyboardInterrupt:
        print("\n\n   👋 Session interrupted. Goodbye!")
    finally:
        cursor.close()
        conn.close()
        print("   🔒 Database connection closed.\n")


if __name__ == "__main__":
    main()