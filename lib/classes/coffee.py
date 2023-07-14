import sqlite3

DB_URL = "app.db"


class Coffee:
    @classmethod
    def drop_table(cls):
        query = """
                    DROP TABLE IF EXISTS coffees;
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute(query)

    @classmethod
    def create_table(cls):
        query = """
                    CREATE TABLE IF NOT EXISTS coffees (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        coffee_type TEXT NOT NULL,
                        price REAL NOT NULL
                    );
                 """

        # make name unchangeable after the first set
        # query += """
        #             CREATE TRIGGER prevent_name_update
        #             BEFORE UPDATE ON coffees
        #             FOR EACH ROW
        #             WHEN OLD.name IS NOT NULL AND NEW.name IS NOT NULL
        #             BEGIN
        #                 SELECT CASE
        #                     WHEN NEW.name != OLD.name THEN
        #                         RAISE (ABORT, 'The name column cannot be updated.')
        #                 END;
        #             END;
        #         """

        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        cursor.executescript(query)
        conn.close()

    def __init__(self, name, coffee_type, price, id=None):
        self.name = name
        self.coffee_type = coffee_type
        self.price = price
        self.id = id

    def save(self):
        Coffee.create_table()
        query = """
                    INSERT INTO coffees(name,coffee_type,price) VALUES(?,?,?);
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        result = cursor.execute(query, (self.name, self.coffee_type, self.price))
        conn.commit()
        self.id = result.lastrowid
        conn.close()

    def customer(self, customer_id):
        from customer import Customer

        query = """
            SELECT * FROM customers WHERE customers.id == ?;
        """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        result = cursor.execute(query, (customer_id,)).fetchone()
        customer = Customer(result[1], result[2], result[3], result[0])
        conn.close()
        return customer

    def all_orders_for_coffee(self):
        from order import Order
        from customer import Customer

        query = """
                    SELECT * FROM orders WHERE orders.coffee_id == ?;
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        results = cursor.execute(query, (self.id,)).fetchall()
        orders = []
        for result in results:
            customer_id = result[1]
            customer = self.customer(customer_id)  # Fetch customer using customer_id
            orders.append(Order(customer, self, result[3], result[4], result[0]))
        conn.close()
        return orders

    def customers(self, new_customer=None):
        from classes.customer import Customer

        pass

    def num_orders(self):
        pass

    def average_price(self):
        pass

    def __repr__(self):
        return f"<{type(self).__name__} id={self.id} Name={self.name} Coffee Type={self.coffee_type} Price={self.price}/>"
