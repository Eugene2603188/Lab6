fail = 0
quit = 0
file_name = "Week 4/inventory.txt"
history = []

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

    current_total = sum(item[2] for item in history_list)
    if current_total + new_quantity <= 500:
        return True
    else:
        print("Inventory limit exceeded. Cannot add more stock.")
        fail += 1
        return False

'''def calculate_tax(amount):
    tax_rate = 0.10
    tax_amount = amount * tax_rate
    return tax_amount
    
def generate_report(inventory, fail):
    print("Total Unit Processed:", inventory)
    print("Number of Failed/Rejected Entries:", fail)'''

def print_current_orders(list_of_orders):
    if list_of_orders== []:
        print("No current orders found.")
    else:
        for item in list_of_orders:
            print(item[0], item[1], item[2])

#Persistence
def persistence(file_name):
    try:
        with open(file_name, "r") as f:
            inventory = f.read()
            return inventory
    except FileNotFoundError:
        inventory = ""
        return inventory

#History Tracking
def history_tracking(inventory_data):
    parsed_history = []
    if inventory_data != "":
        for line in inventory_data.splitlines():
            line = line.strip()
            if line != "":
                parts = line.split(",")
                item_id = int(parts[0].strip())
                name = parts[1].strip()
                quantity = int(parts[2].strip())

                parsed_history.append([item_id, name, quantity])
    return parsed_history

def get_next_id(history_list):
    if len(history_list) > 0:
        return history_list[-1][0] + 1
    else:
        return 1001

def add_order(history_list, product_name, quantity):
    next_id = get_next_id(history_list)
    new_item = [next_id, product_name, quantity]
    history_list.append(new_item)
    return new_item

#Load Inventory
def load_inventory(file_name):
    raw_data = persistence(file_name)
    return history_tracking(raw_data)

#Save Inventory
def save_inventory(file_name, history_list):
    with open(file_name, "w") as f:
        for item in history_list:
            f.write(f"{item[0]}, {item[1]}, {item[2]}\n")

print("Current Orders:\n")
history = load_inventory(file_name)
print_current_orders(history)
print("\n")

while quit != 1:
    product_name = input("Enter Product Name: ").strip()

    if product_name.lower() == "quit":
        quit = 1
        break

    quantity = input("Enter Quantity: ").strip()
    valid_quantity = get_valid_input(quantity)

    if quit == 1 or valid_quantity == "quit":
        break

    if check_quantity_max(history, valid_quantity):
        new_item = add_order(history, product_name, valid_quantity)
        print(f"New Order Added:\n{new_item[0]},{product_name},{valid_quantity}\n")

if len(history) > 0:
    save_inventory(file_name, history)
    print("All orders successfully saved to inventory.txt")

#Eugene Repo URL: https://github.com/Eugene2603188/Lab4

