from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_bcrypt import Bcrypt
import jwt
import os
import openai

app = Flask(__name__)
app.debug = True
secretKey = os.getenv("SUPER_SECRET_KEY")
socketio = SocketIO(app)
bcrypt = Bcrypt(app)
openai.api_key = os.getenv("OPENAI_API_KEY")


class Dish:
    def __init__(self, name, id, price, availability):
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
                        "status": "received",
                        "rating": 2
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

    def update_rating(self, id, rate):
        for order in self.orders:
            if order['id'] == id:
                order['rating'] = rate
                return "order rating updated."
        return "Order not found in orders."


dish1 = Dish("Spaghetti Carbonara", 1, 12.99, "yes")
dish2 = Dish("Margherita Pizza", 2, 10.99, "no")
dish3 = Dish("Chicken Tikka Masala", 3, 14.99, "yes")
dish4 = Dish("Caesar Salad", 4, 8.99, "no")
dish5 = Dish("Beef Burger", 5, 9.99, "yes")

id = 6

inventory = [dish1, dish2, dish3, dish4, dish5]

restaurant = Restaurant(inventory, [])

orders_id = 1


@app.route('/')
def index():
    dist = [dish.__dict__() for dish in restaurant.check_inventory()]
    # return jsonify(dist)
    return render_template('index.html', inventory=dist)


@app.route('/login')
def admin():
    return render_template('login.html')


@app.route('/admin')
def login():
    return render_template('admin.html')


@app.route('/data')
def data():
    res = restaurant.orders
    dist = [dish.__dict__() for dish in restaurant.check_inventory()]
    return jsonify(dist, res)


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


@app.route("/updaterating/<orderid>", methods=['PATCH'])
def updaterating(orderid):
    x = request.get_json()
    res = restaurant.update_rating(int(orderid), x["rating"])
    return jsonify(res)


# socket started

connected_users = {}


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('connect_with_details')
def handle_connect_with_details(data):
    additional_data = data  # Access the additional details sent from the client
    user_info = {
        "email": "socket_id",
        'additional_data': additional_data,  # Store the additional details
        # Add any other user information you want to track
    }
    connected_users["socket_id"] = user_info
    print('Client connected. Socket ID:', "socket_id")


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


# signup/login login
userbase = {}


@socketio.on('signup')
def handle_signup(data):
    global userbase
    name = data['name']
    email = data['email']
    password = data['password']

    pw_hash = bcrypt.generate_password_hash(password)

    userbase[email] = {
        "name": name,
        "password": pw_hash
    }
    print(userbase)
    emit('signup_response', {'message': 'Signup successful'})


@socketio.on('login')
def handle_login(data):
    email = data['email']
    password = data['password']

    if userbase[email]:
        isGenuine = bcrypt.check_password_hash(
            userbase[email]["password"], password)
        if isGenuine:
            encoded_jwt = jwt.encode(
                {"email": email}, secretKey, algorithm="HS256")
            emit('login_response', {
                 'message': 'Login successful', "token": encoded_jwt})
        else:
            emit('login_response', {'message': 'Incorrect password'})


@socketio.on('gpt')
def handle_chat(data):
    input = data["input"]
    question = "so we are running a Restaurant Management app, we have a Restaurant website where the user comes login and then they redirect to the home page the inventory where all dishes are listed also on the same page we show user orders in the list where the user can see the order status in real-time like when order placed its status is 'Received' then it can update into 'Preparing', 'Delivered', 'Canceled' based on status. also user can buy online and we will deliver food to their doorstep. we serve our customers from morning 10 am to evening 10 pm, customer can book their table at our Restaurant by contacting us via phone call. delivery time is 1-3 hour. ``` So based on the above details you have about our business your task is to provide relevant answers to users, also make sure you feel them as you are human and also if you don't know the answer just keep giving round and round answer like a smart customer care representative. give them numbers so they can easily belive```"

    if len(data["chat"]):
        chat = data["chat"]
    else:
        chat = [
        {"role": "system", "content": question}
    ]

    chat.append({"role": "user", "content": input})

    print(chat)
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat,
        max_tokens=60,
        n=1
    )
    chat.append(res.choices[0].message)
    text = res.choices[0].message
    emit("gpt", {"answer": text, "chat": chat})


if __name__ == '__main__':
    app.run()
