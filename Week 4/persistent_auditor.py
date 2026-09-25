fail = 0
stock = 0


#Persistence
file_name= "inventory.txt"
inventory = []

try:
    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            if line != "":
                parts = line.split(",")
                item_id = int(parts[0].strip())
                name = parts[1].strip()
                quantity = int(parts[2].strip())

                inventory.append([item_id, name, quantity])
except FileNotFoundError:
    inventory = []  

#History Tracking
history = []


def get_valid_input():
    global fail
    global stock

    if stock.isdigit():
        return stock
    else:
        if stock != "quit":
            print("Invalid input. Please enter a positive number or 'quit' to exit.")
            fail = fail + 1
            stock = 0
        else:
            stock = "quit"
        return stock
    
def process_delivery(current_total, new_value):
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
    print("Number of Failed/Rejected Entries:", fail)

while (stock != "quit"):
    stock = input("Enter stock quantity: ")
    if stock == "quit":
        break
    get_valid_input()
    inventory = process_delivery(int(inventory), int(stock))

generate_report(inventory, fail)

#Eugene Repo URL: https://github.com/Eugene2603188/Lab4

