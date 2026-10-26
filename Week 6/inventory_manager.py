import json

file_name = "inventory.json"

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

class Inventory:
    """Manages a collection of products in the inventory."""
    
    def __init__(self):
        """Constructor - initialize an empty product list."""
        self.__products = []

    def get_total_stock(self):
        """Return total quantity of all products in inventory."""
        return sum(product.get_quantity() for product in self.__products)
    
    def add_product(self, product_id, name, price, quantity):
        """Add a new product to the inventory."""
        product = Product(product_id, name, price, quantity)
        self.__products.append(product)
        print("\nProduct added successfully")
    
    def search_product_by_term(self, search_term):
        """Search for products by ID or name. Returns list of matching products."""
        found_items = []
        clean_term = search_term.lstrip("Pp").strip()
        
        for product in self.__products:
            # Match by ID or name (case-insensitive)
            if str(product.get_id()) == clean_term or clean_term.lower() in product.get_name().lower():
                found_items.append(product)
        
        return found_items

    def update_product_stock(self, search_term, new_quantity):
        """Update stock for a product by ID or name. Returns True if successful."""
        clean_term = search_term.lstrip("Pp").strip()
        
        for product in self.__products:
            # Match by ID or name (case-insensitive)
            if str(product.get_id()) == clean_term or clean_term.lower() in product.get_name().lower():
                product.update_stock(new_quantity)
                return True
        
        return False
    
    def display_all(self):
        """Display all products in the inventory."""
        if not self.__products:
            print("Inventory is empty.")
        else:
            for product in self.__products:
                product.display_information()
    
    def get_products(self):
        """Return the list of all products."""
        return self.__products

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

#Reads the JSON file into dict
def read_json(file_name):
    try:
        with open(file_name, "r") as f:
            return json.load(f)  # Automatically parses JSON back into a list of dictionaries
    except FileNotFoundError:
        print(f"{file_name} not found. Starting with an empty inventory.")
        return []
    except json.JSONDecodeError:
        # Handles case if file exists but is empty/corrupted
        return []
    
#All the dict shit from JSON file to Product objects
def load_product_objects(file_name, inventory_obj):
    """Load products from JSON file into Inventory object as Product instances."""
    data = read_json(file_name)  # Calls Function 1
    for item in data:
        # Convert dictionary → Product object
        product = Product(item["id"], item["name"], item["price"], item["quantity"])
        # Add Product object to Inventory
        inventory_obj.add_product(product)

#Saves the Product objects to JSON file
def save_product_objects_to_json(file_name, inventory_obj):
    """Convert Product objects to dictionaries and save to JSON."""
    try:
        products_data = []
        for product in inventory_obj.get_products():  # Loop through Product objects
            # Extract data from each Product using getters
            products_data.append({
                "id": product.get_id(),
                "name": product.get_name(),
                "price": product.get_price(),
                "quantity": product.get_quantity()
            })
        # Save list of dictionaries to JSON file
        with open(file_name, "w") as f:
            json.dump(products_data, f, indent=4)
    except Exception as e:
        print(f"Error saving file: {e}\n")

#---- THE MENU SHIT -----
inventory = Inventory()
load_product_objects("inventory.json", inventory)

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
        inventory.display_all()

    elif choice == "2":
        print("\nAdd New Product")
        raw_id = input("Product ID: ").strip()
        product_id = int(raw_id.lstrip("Pp"))
        product_name = input("Product Name: ").strip()
        price = float(input("Price: ").strip())
        raw_qty = input("Stock Quantity: ").strip()
        valid_quantity = get_valid_input(raw_qty)
        
        if valid_quantity != "quit":
            current_total = inventory.get_total_stock()
            if current_total + valid_quantity <= 500:
                inventory.add_product(product_id, product_name, price, valid_quantity)
            else:
                print(f"Current stock: {current_total} | Limit: 500 | Available space: {500 - current_total}")

    elif choice == "3":
        print("\nUpdate Stock")
        search_term = input("Enter Product ID or Name: ").strip()
        
        # Find the product first
        found_items = inventory.search_product_by_term(search_term)
        
        if found_items:
            product = found_items[0]  # Use first match
            print("\nProduct Found:")
            product.display_information()
            
            # Prompt for new quantity
            raw_qty = input("\nNew Stock Quantity: ").strip()
            valid_quantity = get_valid_input(raw_qty)
            
            if valid_quantity != "quit":
                current_total = inventory.get_total_stock()
                old_quantity = product.get_quantity()
                new_total = current_total - old_quantity + valid_quantity
                
                if new_total <= 500:
                    inventory.update_product_stock(search_term, valid_quantity)
                    print("\nStock updated successfully!")
                else:
                    print(f"Current stock (excl. this product): {current_total - old_quantity} | New quantity: {valid_quantity} | Total would be: {new_total} | Limit: 500")
        else:
            print("Product not found.")
            
    elif choice == "4":
        search_term = input("Search Product ID: ").strip()
        found_items = inventory.search_product_by_term(search_term)
        
        if found_items:
            print("\nProduct Found")
            print("\n------------------------------------------------")
            for product in found_items:
                product.display_information()
            print("------------------------------------------------\n")
        else:
            print("Product not found.\n")
        
    elif choice == "5":
        save_product_objects_to_json(file_name, inventory)
        print("\nSaving inventory...")
        print(f"Inventory saved successfully to {file_name}\n")

    elif choice == "6":
        save_product_objects_to_json(file_name, inventory) 
        print("\nSaving inventory before exit...")
        print("Inventory saved successfully.\n")
        print("Thank you for using Inventory Management System.")
        print("Program terminated.")
        break

    else:
        print("Invalid choice. Please select from 1 to 6.")

#Eugene Repo URL: https://github.com/Eugene2603188/Lab6

