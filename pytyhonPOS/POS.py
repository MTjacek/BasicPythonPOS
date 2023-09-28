import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Create the "inventory" table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        item_number INTEGER PRIMARY KEY,
        on_hand INTEGER
    )
""")
conn.commit()

def store_item(item_number, amount):
    # Check if the item already exists in the inventory
    cursor.execute("SELECT on_hand FROM inventory WHERE item_number=?", (item_number,))
    existing_amount = cursor.fetchone()

    if existing_amount is None:
        # If the item doesn't exist, insert a new row
        cursor.execute("INSERT INTO inventory (item_number, on_hand) VALUES (?, ?)", (item_number, amount))
    else:
        # If the item exists, update the "on_hand" value
        new_amount = existing_amount[0] + amount
        cursor.execute("UPDATE inventory SET on_hand=? WHERE item_number=?", (new_amount, item_number))
    
    conn.commit()
    print(f"Stored {amount} of item {item_number} in inventory.")

def check_item(item_number):
    # Check the amount on hand for the specified item
    cursor.execute("SELECT on_hand FROM inventory WHERE item_number=?", (item_number,))
    result = cursor.fetchone()

    if result is not None:
        print(f"Item {item_number} - Amount on hand: {result[0]}")
    else:
        print(f"Item {item_number} not found in inventory.")

def sell_item(item_number, amount_sold):
    # Check if the item exists in the inventory
    cursor.execute("SELECT on_hand FROM inventory WHERE item_number=?", (item_number,))
    existing_amount = cursor.fetchone()

    if existing_amount is not None:
        current_amount = existing_amount[0]
        if current_amount >= amount_sold:
            new_amount = current_amount - amount_sold
            cursor.execute("UPDATE inventory SET on_hand=? WHERE item_number=?", (new_amount, item_number))
            conn.commit()
            print(f"Sold {amount_sold} of item {item_number}.")
        else:
            print(f"Error: Insufficient quantity on hand for item {item_number}.")
    else:
        print(f"Item {item_number} not found in inventory.")

def main():
    print("Welcome")

    while True:
        user_input = input("Enter a command (store, check, sold, or 'exit' to quit): ").strip().lower()

        if user_input == 'store':
            try:
                item_number = int(input("Enter item number: "))
                amount = int(input("Enter amount: "))
                store_item(item_number, amount)
            except ValueError:
                print("Invalid input. Item number and amount must be integers.")
        elif user_input == 'check':
            try:
                item_number = int(input("Enter item number to check: "))
                check_item(item_number)
            except ValueError:
                print("Invalid input. Item number must be an integer.")
        elif user_input == 'sold':
            try:
                item_number = int(input("Enter item number to sell: "))
                amount_sold = int(input("Enter amount to sell: "))
                sell_item(item_number, amount_sold)
            except ValueError:
                print("Invalid input. Item number and amount must be integers.")
        elif user_input == 'exit':
            print("Exiting the program.")
            break
        else:
            print("Invalid command. Please enter 'store', 'name', 'check', 'sold', or 'exit'.")

if __name__ == "__main__":
    main()

# Close the database connection when done
conn.close()
