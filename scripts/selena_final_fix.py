import pandas as pd
import sqlite3
import re

# 1. Wczytanie danych wejściowych
df = pd.read_csv('selena_legacy_data.csv')

print(f"Startowa liczba rekordów: {len(df)}")

# --- ZADANIE 1: ACDIS Integration (Mapowanie Kategorii) ---
mask_fr_mousse = (df['Market'] == 'FR') & (df['Product_Name'].str.contains('Mousse', case=False))
df.loc[mask_fr_mousse, 'Category'] = 'Piany'
print(f"Zaktualizowano kategorię dla {mask_fr_mousse.sum()} produktów z rynku FR.")

# --- ZADANIE 2: Deduplikacja (Konsolidacja 10 par EAN) ---
# Sortujemy tak, aby zachować rekordy z wypełnionym URL (lepsza jakość)
df = df.sort_values(by=['EAN', 'Safety_Sheet_URL'], ascending=[True, False])
initial_count = len(df)
df_cleaned = df.drop_duplicates(subset=['EAN'], keep='first')
deduplicated_count = initial_count - len(df_cleaned)
print(f"Skonsolidowano {deduplicated_count} duplikatów EAN (wybrano rekordy z dokumentacją).")

# --- Dodatkowe czyszczenie techniczne ---
df_cleaned['Product_Name'] = df_cleaned['Product_Name'].str.strip()
df_cleaned['Blocked_for_E-commerce'] = df_cleaned['Safety_Sheet_URL'].isna() | (df_cleaned['Safety_Sheet_URL'] == '')

# 2. Aktualizacja Bazy Danych SQLite (Relacyjna struktura)
conn = sqlite3.connect('pim_database.db')
cursor = conn.cursor()

# Czyścimy stare dane przed importem nowych
cursor.execute('DELETE FROM Products')

# Mapowanie kategorii do ID (uproszczone dla demo)
cat_map = {'Piany': 1, 'Kleje': 2, 'Uszczelniacze': 3, 'Beauty': 4} # Beauty zostało z poprzedniego testu

for _, row in df_cleaned.iterrows():
    cat_id = cat_map.get(row['Category'], 1) # domyślnie Piany
    cursor.execute('''
        INSERT INTO Products (SKU, Name, EAN, Price, Category_ID)
        VALUES (?, ?, ?, ?, ?)
    ''', (row['SKU'], row['Product_Name'], row['EAN'], 0.0, cat_id))

conn.commit()
conn.close()

# Zapisanie finalnego pliku CSV
df_cleaned.to_csv('selena_final_master_data.csv', index=False)
print("Finalna baza Master Data zapisana i wgrana do SQL.")
