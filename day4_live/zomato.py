import os

def clear_console():
    # Clear the console screen based on the operating system
    if os.name == 'nt':  # For Windows
        _ = os.system('cls')
    else:  # For Unix/Linux/MacOS
        _ = os.system('clear')

class Dish:
    def __init__(self, name, id, price, availability ):
        self.name = name
        self.id = id
        self.price = price
        self.availability = availability 

class Restaurant:
    def __init__(self, inventory, orders):
        self.inventory = inventory
        self.orders = orders

    def check_inventory(self):
        print("Dishes:")
        if len(self.inventory) == 0:
            print("No Available Dishes found.")
            return
        flag = True
        for dish in self.inventory:
            if dish.availability == "yes":
                print(f"ID: {dish.id}, Name: {dish.name}, Price: {dish.price}")
                flag = False
        if flag:print("No Available Dishes found.")


    def add(self, dish):
        for singledish in self.inventory:
            if singledish.id == dish.id:
                return "ID already  exist"
        self.inventory.append(dish)
        print("Dish added to inventory.")

    def remove(self, id):
        for singledish in self.inventory:
            if singledish.id == id:
                self.inventory.remove(singledish)
                print("Dish removed from inventory.")
                return
        print("Dish not found in inventory.")

    def update(self, id, availability):
        for singledish in self.inventory:
            if singledish.id == id:
                singledish.availability = availability
                print("Dish availability updated.")
                return
        print("Dish not found in inventory.")

    def neworder(self, id, name, orders_id):
        for dish in self.inventory:
            if dish.id == id:
                if dish.availability == "yes":
                    order = {
                        "id": orders_id,
                        "customer_name": name,
                        "name": dish.name,
                        "price": dish.price,
                        "status": "received"
                    }
                    self.orders.append(order)
                    print("order received!")
                    print(self.orders)
                    return
                else:
                    print("Dish is unavailable.")
                    return
        print("Dish not found in inventory.")

    def check_orders(self):
        print("Orders:")
        if len(self.orders) == 0:
            print("No orders found.")
            return
        for order in self.orders:
            print(f"ID: {order['id']}, Customer name: {order['customer_name']}, Name: {order['name']}, Price: {order['price']}, Status: {order['status']}")

    def update_status(self, id, status):
        for order in self.orders:
            if order['id'] == id:
                order['status'] = status
                print("order status updated.")
                return
        print("Order not found in orders.")

dish1 = Dish("Spaghetti Carbonara", 1, 12.99, "yes")
dish2 = Dish("Margherita Pizza", 2, 10.99, "yes")
dish3 = Dish("Chicken Tikka Masala", 3, 14.99, "yes")
dish4 = Dish("Caesar Salad", 4, 8.99, "yes")
dish5 = Dish("Beef Burger", 5, 9.99, "yes")

inventory = [dish1, dish2, dish3, dish4, dish5]

restaurant = Restaurant(inventory, [])

orders_id = 1
while(True):
    print("\n1. Check Available Dishes")
    print("2. Add a dish")
    print("3. Remove a dish")
    print("4. Update availability")
    print("5. New order")
    print("6. Check Orders")
    print("7. Update Status")
    print("8. Exit")

    choice = input("\nEnter your choice (1-8): ")

    print(choice)

    if choice == "1":
        restaurant.check_inventory()
    elif choice == "2":
        id = int(input("Enter dish ID: "))
        name = input("Enter dish name: ")
        price = float(input("Enter dish price: "))
        availability = input("Enter dish availability (yes/no): ")

        dish = Dish(name, id, price, availability)
        restaurant.add(dish)
    elif choice == "3":
        id = int(input("Enter dish ID to remove: "))
        restaurant.remove(id)
    elif choice == "4":
        id = int(input("Enter dish ID to update availability: "))
        availability = input("Enter updated availability (yes/no): ")
        restaurant.update(id, availability)
    elif choice == "5":
        id = int(input("Enter dish ID sold: "))
        name = input("Enter customer name: ")
        restaurant.neworder(id, name, orders_id)
        orders_id += 1
    elif choice == "6":
        restaurant.check_orders()
    elif choice == "7":
        id = int(input("Enter order ID to update availability: "))
        status = input("Enter Status (preparing/ready for pickup/delivered): ")
        restaurant.update_status(id, status)
    elif choice == "8":
        print("Exiting the application.")
        break
    else:
        print("Invalid choice. Please try again.")

