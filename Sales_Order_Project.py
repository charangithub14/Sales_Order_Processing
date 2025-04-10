import uuid
import json
from datetime import datetime

customers = {}
products = {}
orders = []

TAX_RATE = 0.18

class Customer:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name

class Product:
    def __init__(self, name, price):
        self.id = str(uuid.uuid4())
        self.name = name
        self.price = price

class OrderItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def get_subtotal(self):
        return self.product.price * self.quantity

class Order:
    def __init__(self, customer, items):
        self.id = str(uuid.uuid4())
        self.customer = customer
        self.items = items
        self.status = "Pending"
        self.created_at = datetime.now()

    def calculate_total(self):
        subtotal = sum(item.get_subtotal() for item in self.items)
        tax = subtotal * TAX_RATE
        total = subtotal + tax
        return subtotal, tax, total

    def mark_delivered(self):
        self.status = "Delivered"

def add_customer(name):
    customer = Customer(name)
    customers[customer.id] = customer
    return customer

def add_product(name, price):
    product = Product(name, price)
    products[product.id] = product
    return product

def create_order(customer_id, product_orders):
    customer = customers[customer_id]
    items = [OrderItem(products[pid], qty) for pid, qty in product_orders]
    order = Order(customer, items)
    orders.append(order)
    return order

def generate_report():
    report = []
    for order in orders:
        subtotal, tax, total = order.calculate_total()
        report.append({
            "Order ID": order.id,
            "Customer": order.customer.name,
            "Status": order.status,
            "Subtotal": subtotal,
            "Tax": tax,
            "Total": total,
            "Date": order.created_at.strftime("%Y-%m-%d %H:%M")
        })
    return report

if __name__ == "__main__":
    charan = add_customer("Charan")
    nithin = add_customer("Nithin")
    lalith = add_customer("Lalith")

    laptop = add_product("Laptop", 60000)
    mobile = add_product("Mobile", 25000)
    pc = add_product("PC", 45000)

    order1 = create_order(charan.id, [(laptop.id, 1), (mobile.id, 2)])
    order2 = create_order(nithin.id, [(pc.id, 1)])
    order3 = create_order(lalith.id, [(mobile.id, 1), (laptop.id, 1)])

    order1.mark_delivered()

    print(json.dumps(generate_report(), indent=2))
