import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  inventory: any[] = [];
  orders: any[] = [];

  ngOnInit() {
    this.fetchInventory();
    this.fetchOrders();
  }

  fetchInventory() {
    fetch('https://flaks-app.onrender.com/data')
      .then(response => response.json())
      .then(data => {
        this.inventory = data[0];
      })
      .catch(error => {
        console.error('Error fetching inventory:', error);
      });
  }

  fetchOrders() {
    fetch('https://flaks-app.onrender.com/orders')
      .then(response => response.json())
      .then(data => {
        this.orders = data;
      })
      .catch(error => {
        console.error('Error fetching orders:', error);
      });
  }

  addDish(event: Event) {
    event.preventDefault();
    const name = (<HTMLInputElement>document.getElementById('name')).value;
    const price = (<HTMLInputElement>document.getElementById('price')).value;
    const availability = (<HTMLInputElement>document.getElementById('availability')).value;

    fetch('https://flaks-app.onrender.com/postdish', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name, price, availability })
    })
      .then(response => {
        if (response.ok) {
          this.fetchInventory();
          alert('Dish added to inventory.');
        } else {
          alert('Error adding dish.');
        }
      })
      .catch(error => {
        alert('Error adding dish.');
        console.error('Error adding dish:', error);
      });
  }

  placeOrder(event: Event) {
    event.preventDefault();
    const dishId = (<HTMLInputElement>document.getElementById('dishId')).value;
    const customerName = (<HTMLInputElement>document.getElementById('customerName')).value;

    fetch(`https://flaks-app.onrender.com/sold/${dishId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name: customerName })
    })
      .then(response => response.text())
      .then(data => {
        if (data === 'order received!') {
          this.fetchOrders();
          alert('Order placed successfully.');
        } else {
          alert(data);
        }
      })
      .catch(error => {
        alert('Error placing order.');
        console.error('Error placing order:', error);
      });
  }

  updateOrderStatus(event: Event) {
    event.preventDefault();
    const orderId = (<HTMLInputElement>document.getElementById('orderId')).value;
    const status = (<HTMLInputElement>document.getElementById('status')).value;

    fetch(`https://flaks-app.onrender.com/updateorders/${orderId}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ status })
    })
      .then(response => response.json())
      .then(data => {
        if (data === 'order status updated.') {
          this.fetchOrders();
          alert('Order status updated successfully.');
        } else {
          alert(data);
        }
      })
      .catch(error => {
        alert('Error updating order status.');
        console.error('Error updating order status:', error);
      });
  }

  deleteDish(dishId: number) {
    fetch(`https://flaks-app.onrender.com/delete/${dishId}`, {
      method: 'DELETE'
    })
      .then(response => {
        if (response.ok) {
          this.fetchInventory();
          alert('Dish deleted successfully.');
        } else {
          alert('Error deleting dish.');
        }
      })
      .catch(error => {
        alert('Error deleting dish.');
        console.error('Error deleting dish:', error);
      });
  }

  updateAvailability(dishId: number, availability: string) {
    const newAvailability = availability === 'yes' ? 'no' : 'yes';
    fetch(`https://flaks-app.onrender.com/update/${dishId}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ availability: newAvailability })
    })
      .then(response => {
        if (response.ok) {
          this.fetchInventory();
          alert('Dish availability updated successfully.');
        } else {
          alert('Error updating dish availability.');
        }
      })
      .catch(error => {
        alert('Error updating dish availability.');
        console.error('Error updating dish availability:', error);
      });
  }
}
