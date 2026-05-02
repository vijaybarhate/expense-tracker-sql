import mysql.connector
from datetime import date

# ── Connect to Database ────────────────────────────────
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="expense_tracker"
)
cursor = conn.cursor()

# ── Functions ──────────────────────────────────────────

def add_expense():
    print("\n--- Add Expense ---")
    category = input("Category (Food/Transport/Shopping/Bills/Other): ").strip()
    amount = float(input("Amount (₹): "))
    date_input = input("Date (YYYY-MM-DD) or press Enter for today: ").strip()
    expense_date = date_input if date_input else str(date.today())
    note = input("Note (optional): ").strip()

    cursor.execute(
        "INSERT INTO expenses (category, amount, date, note) VALUES (%s, %s, %s, %s)",
        (category, amount, expense_date, note)
    )
    conn.commit()
    print(f"✅ Expense of ₹{amount} added under '{category}'!")

def view_expenses():
    print("\n--- All Expenses ---")
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    if not rows:
        print("No expenses found.")
        return
    print(f"\n{'ID':<5} {'Category':<15} {'Amount':>10} {'Date':<15} {'Note'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<15} ₹{row[2]:>9} {str(row[3]):<15} {row[4] or ''}")

def delete_expense():
    view_expenses()
    print("\n--- Delete Expense ---")
    exp_id = int(input("Enter ID to delete: "))
    cursor.execute("DELETE FROM expenses WHERE id = %s", (exp_id,))
    conn.commit()
    if cursor.rowcount:
        print(f"✅ Expense ID {exp_id} deleted!")
    else:
        print("❌ ID not found.")

def summary():
    print("\n--- Summary ---")
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0
    print(f"💰 Total Spent: ₹{total}")

    print("\n📊 Category-wise Breakdown:")
    cursor.execute(
        "SELECT category, SUM(amount), COUNT(*) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC"
    )
    rows = cursor.fetchall()
    print(f"\n{'Category':<15} {'Total':>10} {'Transactions':>15}")
    print("-" * 45)
    for row in rows:
        print(f"{row[0]:<15} ₹{row[1]:>9} {row[2]:>15}")

    print("\n📅 Monthly Breakdown:")
    cursor.execute(
        "SELECT DATE_FORMAT(date, '%Y-%m') as month, SUM(amount) FROM expenses GROUP BY month ORDER BY month DESC"
    )
    rows = cursor.fetchall()
    print(f"\n{'Month':<15} {'Total':>10}")
    print("-" * 30)
    for row in rows:
        print(f"{row[0]:<15} ₹{row[1]:>9}")

def search_by_category():
    category = input("\nEnter category to search: ").strip()
    cursor.execute(
        "SELECT * FROM expenses WHERE category = %s ORDER BY date DESC",
        (category,)
    )
    rows = cursor.fetchall()
    if not rows:
        print("No expenses found for this category.")
        return
    print(f"\n{'ID':<5} {'Category':<15} {'Amount':>10} {'Date':<15} {'Note'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<15} ₹{row[2]:>9} {str(row[3]):<15} {row[4] or ''}")

# ── Main Menu ──────────────────────────────────────────

def main():
    print("=" * 40)
    print("   💰 EXPENSE TRACKER WITH SQL")
    print("=" * 40)

    while True:
        print("\n1. Add Expense")
        print("2. View All Expenses")
        print("3. Delete Expense")
        print("4. Summary & Analytics")
        print("5. Search by Category")
        print("6. Exit")

        choice = input("\nEnter choice (1-6): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            summary()
        elif choice == "5":
            search_by_category()
        elif choice == "6":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()