import sqlite3

DB_URL = "app.db"


class Customer:
    @classmethod
    def drop_table(cls):
        query = """
                    DROP TABLE IF EXISTS customers;
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute(query)

    @classmethod
    def create_table(cls):
        query = """
                    CREATE TABLE IF NOT EXISTS customers(
                        id INTEGER PRIMARY KEY,
                        fname TEXT NOT NULL,
                        lname TEXT NOT NULL,
                        age INTEGER NOT NULL
                    );
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.close()

    def __init__(self, fname, lname, age, id=None):
        self.fname = fname
        self.lname = lname
        self.age = age
        self.id = id

    def save(self):
        Customer.create_table()
        query = """
                    INSERT INTO customers(fname,lname,age) VALUES(?,?,?);
                """
        conn = sqlite3.connect(DB_URL)
        cursor = conn.cursor()
        result = cursor.execute(query, (self.fname, self.lname, self.age))
        conn.commit()
        self.id = result.lastrowid
        conn.close()

    def orders(self, new_order=None):
        from classes.order import Order

        pass

    def coffees(self, new_coffee=None):
        from classes.coffee import Coffee

        pass

    def __repr__(self):
        return f"<{type(self).__name__} id={self.id} Name={self.fname} LastName={self.lname} age={self.age}/>"
