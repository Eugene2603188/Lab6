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
    
'''def process_delivery(current_total, new_value):
    global fail
    global stock

    if current_total + new_value <= 500:
        current_total = current_total + new_value
        print("Current inventory:", current_total)
        return current_total
    else:
        print("Inventory limit exceeded. Cannot add more stock.")
        fail += 1
        stock = "quit"
    return current_total

def calculate_tax(amount):
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


inventory = persistence(file_name)
history = history_tracking(inventory)
print_current_orders(history)

while quit != 1:
    product_name = input("Enter Product Name: ").strip()
    if product_name.lower() == "quit":
        quit = 1
        break

    quantity = input("Enter Quantity: ").strip()
    valid_quantity = get_valid_input(quantity)

    if quit == 1 or valid_quantity == "quit":
        break

generate_report(inventory, fail)

#Eugene Repo URL: https://github.com/Eugene2603188/Lab4

