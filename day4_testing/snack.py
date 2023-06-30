class Snack:
    def __init__(self, snack_id, name, price, availability):
        self.snack_id = snack_id
        self.name = name
        self.price = price
        self.availability = availability

class Canteen:
    def __init__(self):
        self.inventory = []
        self.sales = []

    def add_snack(self, snack):
        self.inventory.append(snack)
        print("Snack added to inventory.")

    def remove_snack(self, snack_id):
        for snack in self.inventory:
            if snack.snack_id == snack_id:
                self.inventory.remove(snack)
                print("Snack removed from inventory.")
                return
        print("Snack not found in inventory.")

    def update_snack_availability(self, snack_id, availability):
        for snack in self.inventory:
            if snack.snack_id == snack_id:
                snack.availability = availability
                print("Snack availability updated.")
                return
        print("Snack not found in inventory.")

    def record_sale(self, snack_id):
        for snack in self.inventory:
            if snack.snack_id == snack_id:
                if snack.availability == "yes":
                    self.sales.append(snack)
                    snack.availability = "no"
                    print("Sale recorded.")
                    return
                else:
                    print("Snack is unavailable.")
                    return
        print("Snack not found in inventory.")

    def print_inventory(self):
        print("Snack Inventory:")
        if len(self.inventory) == 0:
            print("No snacks in inventory.")
        for snack in self.inventory:
            print(f"ID: {snack.snack_id}, Name: {snack.name}, Price: {snack.price}, Availability: {snack.availability}")

    def print_sales(self):
        print("Sales Records:")
        if len(self.sales) == 0:
            print("No sales made.")
        for snack in self.sales:
            print(f"ID: {snack.snack_id}, Name: {snack.name}, Price: {snack.price}")

# Create an instance of the Canteen class
canteen = Canteen()

while True:
    print("\n1. Add a snack")
    print("2. Remove a snack")
    print("3. Update snack availability")
    print("4. Record a sale")
    print("5. Print inventory")
    print("6. Print sales records")
    print("7. Exit")

    choice = input("\nEnter your choice (1-7): ")

    if choice == "1":
        snack_id = int(input("Enter snack ID: "))
        name = input("Enter snack name: ")
        price = float(input("Enter snack price: "))
        availability = input("Enter snack availability (yes/no): ")

        snack = Snack(snack_id, name, price, availability)
        canteen.add_snack(snack)

    elif choice == "2":
        snack_id = int(input("Enter snack ID to remove: "))
        canteen.remove_snack(snack_id)

    elif choice == "3":
        snack_id = int(input("Enter snack ID to update availability: "))
        availability = input("Enter updated availability (yes/no): ")
        canteen.update_snack_availability(snack_id, availability)

    elif choice == "4":
        snack_id = int(input("Enter snack ID sold: "))
        canteen.record_sale(snack_id)

    elif choice == "5":
        canteen.print_inventory()

    elif choice == "6":
        canteen.print_sales()

    elif choice == "7":
        print("Exiting the application.")
        break

    else:
        print("Invalid choice. Please try again.")
