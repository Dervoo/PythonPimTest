import pandas as pd
import sqlite3
import random

# 1. Wczytanie danych Legacy
df = pd.read_csv('data/selena_legacy_data.csv')
initial_count = len(df)

# Sortujemy tak, aby te z URL były na początku (priorytet przy usuwaniu duplikatów)
df['Has_MSDS'] = df['Safety_Sheet_URL'].notnull()
df = df.sort_values(by=['EAN', 'Has_MSDS'], ascending=[True, False])

# 2. Usuwanie duplikatów po EAN (zostawiamy te z dokumentacją)
df_cleaned = df.drop_duplicates(subset=['EAN'], keep='first')

# 3. Naprawa taksonomii FR
df_cleaned.loc[df_cleaned['Category'] == 'Unmapped_FR', 'Category'] = 'Piany'

# 4. Blokowanie e-commerce dla braków MSDS
df_cleaned['Blocked_for_E-commerce'] = df_cleaned['Safety_Sheet_URL'].isna() | (df_cleaned['Safety_Sheet_URL'] == '')

# Dodajemy kolumnę Price (np. 45.99) dla analityki
df_cleaned['Price'] = 45.99

# 5. Aktualizacja Bazy Danych SQLite
conn = sqlite3.connect('pim_database.db')
cursor = conn.cursor()

# Czyścimy stare dane
cursor.execute('DELETE FROM Products')
cursor.execute('DELETE FROM Quality_Logs')

# Mapowanie kategorii do ID
cat_map = {'Piany': 1, 'Kleje': 2, 'Uszczelniacze': 3}

for _, row in df_cleaned.iterrows():
    cat_id = cat_map.get(row['Category'], 1)
    # Wstawiamy produkt z ceną 45.99
    cursor.execute('''
        INSERT INTO Products (SKU, Name, EAN, Price, Category_ID)
        VALUES (?, ?, ?, ?, ?)
    ''', (row['SKU'], row['Product_Name'], str(row['EAN']), 45.99, cat_id))
    
    # Jeśli zablokowany, dodajemy log jakości
    if row['Blocked_for_E-commerce']:
        cursor.execute("INSERT INTO Quality_Logs (SKU, Error_Type, Date) VALUES (?, ?, '2025-03-11')",
                       (row['SKU'], 'Missing MSDS'))

conn.commit()
conn.close()

# Zapisanie finalnego pliku CSV z nową kolumną Price
df_cleaned.to_csv('data/selena_final_master_data.csv', index=False)
print(f"Sukces: Skonsolidowano {initial_count - len(df_cleaned)} duplikatów. Ceny i logi wgrane do bazy.")
