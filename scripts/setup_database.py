import sqlite3
import pandas as pd

def setup_db():
    conn = sqlite3.connect('pim_database.db')
    cursor = conn.cursor()

    # 1. Tworzenie tabel
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Categories (
        Category_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Category_Name TEXT NOT NULL,
        Tax_Rate REAL
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        SKU TEXT PRIMARY KEY,
        Name TEXT,
        EAN TEXT,
        Price REAL,
        Category_ID INTEGER,
        FOREIGN KEY (Category_ID) REFERENCES Categories(Category_ID)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Quality_Logs (
        Log_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        SKU TEXT,
        Error_Type TEXT,
        Date TEXT,
        FOREIGN KEY (SKU) REFERENCES Products(SKU)
    )''')

    # 2. Przykładowe dane do Kategorii
    categories = [('Electronics', 0.23), ('Home & Kitchen', 0.08), ('Beauty', 0.23), ('Sports', 0.23)]
    cursor.executemany('INSERT INTO Categories (Category_Name, Tax_Rate) VALUES (?, ?)', categories)

    conn.commit()
    conn.close()
    print("Baza danych pim_database.db została zainicjowana z relacyjną strukturą.")

if __name__ == "__main__":
    setup_db()
