import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_path)

from app import app, id, orders_id

def test_index():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_login():
    client = app.test_client()
    response = client.get('/login')
    assert response.status_code == 200

def test_admin():
    client = app.test_client()
    response = client.get('/admin')
    assert response.status_code == 200

def test_data():
    client = app.test_client()
    response = client.get('/data')
    assert response.status_code == 200

def test_post():
    client = app.test_client()
    response = client.post('/postdish', json={"name": "Beef Burger", "id": id, "price": 10.99, "availability": "yes"})
    assert response.status_code == 201

def test_delete():
    client = app.test_client()
    response = client.delete('/delete/3')
    assert response.status_code == 200
    assert response.data == b"Dish removed from inventory."

def test_delete():
    client = app.test_client()
    response = client.delete('/delete/6')
    assert response.status_code == 200
    assert response.data == b"Dish removed from inventory."

def test_update():
    client = app.test_client()
    response = client.patch('/update/3', json={"availability": "no"})
    assert response.status_code == 400
    assert response.data == b"Dish not found in inventory."

def test_update():
    client = app.test_client()
    response = client.patch('/update/2', json={"availability": "no"})
    assert response.status_code == 200
    assert response.data == b"Dish availability updated."

def test_sold():
    client = app.test_client()
    response = client.post('/sold/2', json={"name": "Chetan"})
    assert response.status_code == 200
    assert response.data == b"order received!"

def test_sold():
    client = app.test_client()
    response = client.post('/sold/4', json={"name": "Chetan"})
    assert response.status_code == 200
    assert response.data == b"order received!"

def test_sold():
    client = app.test_client()
    response = client.post('/sold/8', json={"name": "Chetan"})
    assert response.status_code == 200
    assert response.data == b"Dish not found in inventory."

def test_sold():
    client = app.test_client()
    response = client.post('/sold/4', json={"name": "Chetan"})
    assert response.status_code == 200
    assert response.data == b"Dish is unavailable."


