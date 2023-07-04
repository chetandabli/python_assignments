from flask import Flask, request, jsonify, json

app = Flask(__name__)

class Dish:
    def __init__(self, name, id, price, availability ):
        self.name = name
        self.id = id
        self.price = price
        self.availability = availability 

    def __dict__(self):
        return {
            'name': self.name,
            'id': self.id,
            'price': self.price,
            'availability': self.availability
        }

class Restaurant:
    def __init__(self, inventory, orders):
        self.inventory = inventory
        self.orders = orders
    
    def check_inventory(self):
        if len(self.inventory) == 0:
            return "No Available Dishes found."
        return self.inventory
    
    def add(self, dish):
        for singledish in self.inventory:
            if singledish.id == dish.id:
                return "ID already  exist"
        self.inventory.append(dish)
        return "Dish added to inventory."

    def remove(self, id):
        for singledish in self.inventory:
            if singledish.id == id:
                self.inventory.remove(singledish)
                return "Dish removed from inventory."
        return "Dish not found in inventory."

    def update(self, id, availability):
        print(id)
        for singledish in self.inventory:
            if singledish.id == id:
                singledish.availability = availability
                return "Dish availability updated."
        return "Dish not found in inventory."
    
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
                    return "order received!"
                else:
                    return "Dish is unavailable."
        return "Dish not found in inventory."
    
    def check_orders(self):
        if len(self.orders) == 0:
            return "No orders found."
        return self.orders
    
    def update_status(self, id, status):
        for order in self.orders:
            if order['id'] == id:
                order['status'] = status
                return "order status updated."
        return "Order not found in orders."

dish1 = Dish("Spaghetti Carbonara", 1, 12.99, "yes")
dish2 = Dish("Margherita Pizza", 2, 10.99, "yes")
dish3 = Dish("Chicken Tikka Masala", 3, 14.99, "yes")
dish4 = Dish("Caesar Salad", 4, 8.99, "yes")
dish5 = Dish("Beef Burger", 5, 9.99, "yes")

id = 6

inventory = [dish1, dish2, dish3, dish4, dish5]

restaurant = Restaurant(inventory, [])

orders_id = 1

@app.route('/')
def index():
    dist = [dish.__dict__() for dish in restaurant.check_inventory()]
    return jsonify(dist)

@app.route("/postdish", methods=['POST'])
def post():
    global id
    x = request.get_json()
    newdish = Dish(x["name"], id, x["price"], x["availability"])
    id += 1
    res = restaurant.add(newdish)
    return res, 201

@app.route("/delete/<deleteid>", methods=['DELETE'])
def delete(deleteid):
    res = restaurant.remove(int(deleteid))
    return res

@app.route("/update/<updateid>", methods=['PATCH'])
def update(updateid):
    x = request.get_json()
    res = restaurant.update(int(updateid), x["availability"])
    return res

@app.route("/sold/<soldid>", methods=['POST'])
def sold(soldid):
    global orders_id
    x = request.get_json()
    res = restaurant.neworder(int(soldid), x["name"], orders_id)
    orders_id += 1
    return res

@app.route("/orders", methods=['GET'])
def orders():
    res = restaurant.orders
    return jsonify(res)

@app.route("/updateorders/<orderid>", methods=['PATCH'])
def updateorders(orderid):
    x = request.get_json()
    res = restaurant.update_status(int(orderid), x["status"])
    return jsonify(res)


if __name__ == '__main__':
    app.run()