from database import (
    create_tables,
    get_customers,
    add_customer,
    delete_customer,
    add_transaction,
    get_transactions_by_customer
)

create_tables()

def show_customers():
    customers = get_customers()
    print("\n📋 Customer List")
    print("-" * 40)

    if not customers:
        print("No customers found.")
        return

    for c in customers:
        print(f"ID: {c[0]} | Name: {c[1]} | Phone: {c[2]} | Balance: {c[3]}")

def add_customer_menu():
    name = input("Customer Name: ")
    phone = input("Phone: ")
    add_customer(name, phone)
    print("✅ Customer added")

def delete_customer_menu():
    show_customers()
    cid = input("Enter Customer ID to delete: ")
    delete_customer(cid)
    print("🗑️ Customer deleted")

def add_transaction_menu():
    show_customers()
    cid = input("Customer ID: ")
    amount = float(input("Amount (+ credit / - debit): "))
    note = input("Note: ")
    add_transaction(cid, amount, note)
    print("💰 Transaction added")

def show_customer_transactions():
    show_customers()
    cid = input("Customer ID: ")

    transactions = get_transactions_by_customer(cid)
    print("\n📜 Transaction History")
    print("-" * 40)

    if not transactions:
        print("No transactions found.")
        return

    for t in transactions:
        print(f"Amount: {t[0]} | Note: {t[1]} | Date: {t[2]}")

def main_menu():
    while True:
        print("\n=== Business AI Menu ===")
        print("1. Show Customers")
        print("2. Add Customer")
        print("3. Delete Customer")
        print("4. Add Transaction")
        print("5. Show Customer Transactions")
        print("0. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            show_customers()
        elif choice == "2":
            add_customer_menu()
        elif choice == "3":
            delete_customer_menu()
        elif choice == "4":
            add_transaction_menu()
        elif choice == "5":
            show_customer_transactions()
        elif choice == "0":
            print("👋 Exit")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main_menu()
