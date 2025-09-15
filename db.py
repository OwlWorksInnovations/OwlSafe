import sqlite3

# Creates a sqlite3 database with specifed name and tables
def create_db(name: str, table: str, columns: list):
    columns_sql = ", ".join([f"{colum} TEXT NOT NULL" for colum in columns])

    con = sqlite3.connect(f"{name}.db")
    cur = con.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns_sql})")
    con.commit()
    con.close()

# Retruns all rows of specifed table and colum
def read_db(name: str, table: str, colum: str):
    con = sqlite3.connect(f"{name}.db")
    cur = con.cursor()
    cur.execute(f"SELECT id, {colum} from {table}")
    rows = cur.fetchall()
    con.close()

    return rows

# Inserts specifed data into the specifed table and columns
def insert_db(name: str, table: str, colum: str, data: str):
    con = sqlite3.connect(f"{name}.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO {table} ({colum}) VALUES (?)", (data,))
    con.commit()
    con.close()