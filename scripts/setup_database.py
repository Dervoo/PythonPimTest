import sqlite3
import pandas as pd
import os

def setup_db():
    conn = sqlite3.connect('pim_database.db')
    cursor = conn.cursor()

    # 1. Czyszczenie starych tabel
    cursor.execute('DROP TABLE IF EXISTS Quality_Logs')
    cursor.execute('DROP TABLE IF EXISTS Products')
    cursor.execute('DROP TABLE IF EXISTS Categories')

    # 2. Tworzenie tabel
    cursor.execute('''
    CREATE TABLE Categories (
        Category_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Category_Name TEXT NOT NULL,
        Tax_Rate REAL
    )''')

    cursor.execute('''
    CREATE TABLE Products (
        SKU TEXT PRIMARY KEY,
        Name TEXT,
        EAN TEXT,
        Price REAL,
        Category_ID INTEGER,
        FOREIGN KEY (Category_ID) REFERENCES Categories(Category_ID)
    )''')

    cursor.execute('''
    CREATE TABLE Quality_Logs (
        Log_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        SKU TEXT,
        Error_Type TEXT,
        Date TEXT,
        FOREIGN KEY (SKU) REFERENCES Products(SKU)
    )''')

    # 3. Dane podstawowe - Kategorie
    categories = [('Piany', 0.23), ('Kleje', 0.08), ('Uszczelniacze', 0.23), ('Unmapped_FR', 0.23)]
    cursor.executemany('INSERT INTO Categories (Category_Name, Tax_Rate) VALUES (?, ?)', categories)
    conn.commit()

    # 4. Import danych z CSV (Master Data)
    if os.path.exists('data/selena_final_master_data.csv'):
        df = pd.read_csv('data/selena_final_master_data.csv')
        
        # Pobieramy ID kategorii z bazy
        cursor.execute("SELECT Category_Name, Category_ID FROM Categories")
        cat_map = dict(cursor.fetchall())

        for _, row in df.iterrows():
            cat_id = cat_map.get(row['Category'], cat_map['Unmapped_FR'])
            # Wstawianie produktu z ceną
            cursor.execute("INSERT INTO Products (SKU, Name, EAN, Price, Category_ID) VALUES (?, ?, ?, ?, ?)",
                           (row['SKU'], row['Product_Name'], str(row['EAN']), row['Price'], cat_id))
            
            # Generowanie logów błędów dla produktów zablokowanych (dla analityki)
            if row['Blocked_for_E-commerce']:
                cursor.execute("INSERT INTO Quality_Logs (SKU, Error_Type, Date) VALUES (?, ?, '2025-03-11')",
                               (row['SKU'], 'Missing MSDS'))

    conn.commit()
    conn.close()
    print("Baza danych zaktualizowana: Dane z CSV i logi błędów zostały poprawnie wgrane.")

if __name__ == "__main__":
    setup_db()
