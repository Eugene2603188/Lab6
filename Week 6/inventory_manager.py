import json

fail = 0
quit = 0
file_name = "inventory.json"
history = []

class Product:
    """Represents a single product in the inventory."""
    
    def __init__(self, product_id, name, price, quantity):
        """Constructor - initialize a product with its attributes."""
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__quantity = quantity
    
    def update_stock(self, new_quantity):
        """Update the stock quantity for this product."""
        self.__quantity = new_quantity
    
    def display_information(self):
        """Display this product's information."""
        print(f"ID: P{self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__quantity}")
    
    # Getters (to read private attributes from outside the class)
    def get_id(self):
        return self.__product_id
    
    def get_name(self):
        return self.__name
    
    def get_price(self):
        return self.__price
    
    def get_quantity(self):
        return self.__quantity

def get_valid_input(quantity):
    global fail
    global quit

    while True:
        if quantity.lower() == "quit":
            quit = 1
            return "quit"
        elif quantity.isdigit():
            return int(quantity)
        else:
            print("Invalid input. Please enter a positive number or 'quit' to exit.")
            fail += 1
            quantity = input("Enter Quantity: ").strip()
    
def check_quantity_max(history_list, new_quantity):
    global fail

    current_total = sum(item["quantity"] for item in history_list)
    if current_total + new_quantity <= 500:
        return True
    else:
        print("Inventory limit exceeded. Cannot add more stock.")
        fail += 1
        return False

def get_next_id(history_list):
    if len(history_list) > 0:
        return history_list[-1]["id"] + 1
    else:
        return 1001

#---- ALL DATA MANIPULATION FUNCTIONS -----
#Data Manipulation - Replaced previously print_current_orders()
def display_all(inventory):
    print("\nCurrent Inventory")
    print("----------------------------------------")
    if not inventory:
        print("No items in inventory.")
    else:
        for item in inventory:
            print(f"ID: P{item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['quantity']}")
    print("----------------------------------------")

#Data Manipulation - Replaced previously add_order()
def add_product(inventory, product_id, product_name, price, quantity):
    new_product = {
        "id": product_id,
        "name": product_name,
        "price": price,
        "quantity": quantity
    }
    inventory.append(new_product)
    print("\nProduct added successfully")
    return new_product

#Data Manipulation - update_stock()
def update_stock(inventory, search_term, new_quantity):
    found = False

    # Strip 'P' or 'p' if user inputs "P1001" instead of "1001"
    clean_term = search_term.lstrip("Pp").strip()
    
    for item in inventory:
        # Check if search_term matches the product name (case-insensitive) or product ID
        if str(item["id"]) == str(clean_term) or item["name"].lower() == str(clean_term).lower():
            item["quantity"] = new_quantity
            found = True
            break
            
    if not found:
        print(f"Product '{search_term}' not found in inventory.")

#Data Manipulation - search_product()
def search_product(inventory, search_term):
    found_items = []
    clean_term = search_term.lstrip("Pp").strip()
    
    for item in inventory:
        if str(item["id"]) == str(clean_term) or clean_term.lower() in item["name"].lower():
            found_items.append(item)
            
    if found_items:
        print("\nProduct Found")
        print("\n------------------------------------------------")
        for item in found_items:
            print(f"ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Quantity: {item['quantity']}")
        print("------------------------------------------------\n")
    else:
        print("Product not found.\n")

#---- ALL DATA PERSISTENCE FUNCTIONS -----
#Data Persistence - Replaced previously persistence() + history_tracking() + load_inventory()
def load_inventory(file_name):
    try:
        with open(file_name, "r") as f:
            return json.load(f)  # Automatically parses JSON back into a list of dictionaries
    except FileNotFoundError:
        print(f"{file_name} not found. Starting with an empty inventory.")
        return []
    except json.JSONDecodeError:
        # Handles case if file exists but is empty/corrupted
        return []
    
#Data Persistence - Replaced previously save_inventory()
def save_inventory(file_name, history_list):
    try:
        with open(file_name, "w") as f:
            json.dump(history_list, f, indent=4)
    except Exception as e:
        print(f"Error saving file: {e}\n")

#---- THE MENU SHIT -----
history = load_inventory(file_name)

print("\n========================================")
print("\nINVENTORY MANAGER SYSTEM")
print("\n========================================")

while True:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    
    choice = input("Enter option: ").strip()

    if choice == "1":
        display_all(history)

    elif choice == "2":
        print("\nAdd New Product")
        raw_id = input("Product ID: ").strip()

        #Remove 'P' or 'p' prefix if user inputs "P1001" instead of "1001"
        product_id = raw_id.lstrip("Pp")
        
        product_name = input("Product Name: ").strip()
        price = float(input("Price: ").strip())
        raw_qty = input("Stock Quantity: ").strip()
        valid_quantity = get_valid_input(raw_qty)
        
        if valid_quantity != "quit" and check_quantity_max(history, valid_quantity):
            add_product(history, product_id, product_name, price, valid_quantity)

    elif choice == "3":
        print("\nUpdate Stock")
        search_term = input("Enter Product ID: ").strip()

        #Remove 'P' or 'p' prefix if user inputs "P1001" instead of "1001"
        clean_term = search_term.lstrip("Pp").strip()
        
        found_product = None
        valid_quantity = None

        for item in history:
            if str(item["id"]) == clean_term:
                found_product = item
                break

        if found_product:
            print("\nProduct Found:")
            print(f"Name: {found_product['name']}")
            print(f"Current Stock: {found_product['quantity']}")

            # Prompt for new quantity
            raw_qty = input("\nNew Stock Quantity: ").strip()
            valid_quantity = get_valid_input(raw_qty)

            if valid_quantity != "quit":
                found_product["quantity"] = valid_quantity
                print("\nStock updated successfully!")
        else:
            print("Product not found.")
        
        
        if valid_quantity != "quit":
            update_stock(history, search_term, valid_quantity)
            
    elif choice == "4":
        search_term = input("Search Product ID: ").strip()
        search_product(history, search_term)

    elif choice == "5":
        save_inventory(file_name, history)
        print("\nSaving inventory...")
        print(f"Inventory saved successfully to {file_name}\n")
    
    elif choice == "6":
        save_inventory(file_name, history)
        print("\nSaving inventory before exit...")
        print("Inventory saved successfully.\n")
        print("Thank you for using Inventory Management System.")
        print("Program terminated.")
        break

    else:
        print("Invalid choice. Please select from 1 to 6.")

#Eugene Repo URL: https://github.com/Eugene2603188/Lab6

