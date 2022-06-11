import sqlite3


class DB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_table_all_secid(self, name_table):
        self.cursor.execute(f'''CREATE TABLE {name_table} (
        id     INTEGER PRIMARY KEY AUTOINCREMENT,
        secid   TEXT,
        price   INTEGER,
        date    DATE
        )''')
        return self.conn.commit()

    def add_secid(self, name_table, secid, price, date):
        self.cursor.execute(f"INSERT INTO {name_table} (secid,price,date) VALUES (?,?,?)", (secid, price, date,))
        return self.conn.commit()