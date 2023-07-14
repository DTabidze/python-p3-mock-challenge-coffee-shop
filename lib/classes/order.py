import sqlite3
from customer import Customer
from coffee import Coffee

DB_URL = "app.db"


class Order:
    @classmethod
    def drop_table(cls):
        query = """
                    DROP TABLE IF EXISTS orders;
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute(query)

    @classmethod
    def create_table(cls):
        query = """
                    CREATE TABLE IF NOT EXISTS orders(
                        id INTEGER PRIMARY KEY,
                        customer_id INTEGER NOT NULL,
                        coffee_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        total_price REAL NOT NULL,
                        FOREIGN KEY(customer_id) REFERENCES customers(id),
                        FOREIGN KEY(coffee_id) REFERENCES coffees(id)
                    );
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.close()

    def __init__(self, customer, coffee, quantity, total_price=None, id=None):
        self.customer = customer
        self.coffee = coffee
        self.quantity = quantity
        self.total_price = self.coffee.price * self.quantity
        self.id = id

    def save(self):
        Order.create_table()
        query = """
                    INSERT INTO orders(customer_id,coffee_id,quantity,total_price)
                    VALUES (?,?,?,?);
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        result = cursor.execute(
            query, (self.customer.id, self.coffee.id, self.quantity, self.total_price)
        )
        conn.commit()
        self.id = result.lastrowid
        conn.close()

    def get_customer_from_order(self):
        query = """
                    SELECT * FROM customers WHERE customers.id == ?;
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        result = cursor.execute(query, (self.customer.id,)).fetchall()[0]
        customer = Customer(result[1], result[2], result[3], result[0])
        conn.close()
        return customer

    def get_coffee_from_order(self):
        query = """
                    SELECT * FROM coffees WHERE coffees.id == ?;
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        result = cursor.execute(query, (self.coffee.id,)).fetchall()[0]
        customer = Coffee(result[1], result[2], result[3], result[0])
        conn.close()
        return customer

    def __repr__(self):
        return f"<{type(self).__name__} id={self.id} Customer={repr(self.customer)} Coffee={repr(self.coffee)} Quantity={self.quantity} Total Price={self.total_price}/>"


Coffee.drop_table()
Customer.drop_table()
Order.drop_table()
ice_late = Coffee("Ice Late", "Milky", 5.65)
ice_late.save()
americano = Coffee("Americano", "Hot Black", 3.39)
americano.save()
expresso = Coffee("Expresso", "Strong", 3.31)
expresso.save()

davit = Customer("Davit", "Tabidze", 34)
davit.save()
tsotne = Customer("Tsotne", "Tabidze", 30)
tsotne.save()
johnwick = Customer("John", "Wick", 44)
johnwick.save()
order_1 = Order(davit, ice_late, 3)
order_1.save()
order_2 = Order(davit, expresso, 1)
order_2.save()

order_3 = Order(tsotne, ice_late, 2)
order_3.save()

order_4 = Order(johnwick, americano, 1)
order_4.save()
print("GET CUSTOMER FROM ORDER")
print(order_4.get_customer_from_order())
print(order_3.get_customer_from_order())
print("GET COFFEE FROM ORDER")
print(order_2.get_coffee_from_order())
print("GET ALL ORDERS OF THE COFFEE")
all_orders = ice_late.all_orders_for_coffee()
print("")
print(all_orders)
