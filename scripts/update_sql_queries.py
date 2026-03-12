import sqlite3

def update_sql():
    conn = sqlite3.connect('pim_database.db')
    cursor = conn.cursor()

    # 1. Analityka cenowa per kategoria
    cursor.execute('DROP VIEW IF EXISTS View_Price_Analytics')
    cursor.execute('''
    CREATE VIEW View_Price_Analytics AS
    SELECT 
        c.Category_Name,
        COUNT(p.SKU) as Product_Count,
        ROUND(AVG(p.Price), 2) as Avg_Price,
        MIN(p.Price) as Min_Price,
        MAX(p.Price) as Max_Price
    FROM Products p
    JOIN Categories c ON p.Category_ID = c.Category_ID
    GROUP BY c.Category_Name
    ''')

    # 2. Widok produktow o wysokiej wartosci (Top 10% najdrozszych)
    cursor.execute('DROP VIEW IF EXISTS View_Premium_Products')
    cursor.execute('''
    CREATE VIEW View_Premium_Products AS
    SELECT SKU, Name, Price, Category_ID
    FROM Products
    WHERE Price > (SELECT AVG(Price) * 1.5 FROM Products)
    ORDER BY Price DESC
    ''')

    # 3. Podsumowanie bledow jakosciowych
    cursor.execute('DROP VIEW IF EXISTS View_Quality_Summary')
    cursor.execute('''
    CREATE VIEW View_Quality_Summary AS
    SELECT 
        Error_Type,
        COUNT(*) as Total_Errors,
        Date
    FROM Quality_Logs
    GROUP BY Error_Type, Date
    ''')

    conn.commit()
    conn.close()
    print("✅ Baza SQL wzbogacona o nowe widoki analityczne (Price Analytics, Premium Products, Quality Summary).")

if __name__ == "__main__":
    update_sql()
