import pandas as pd
import numpy as np
import random

def generate_selena_data():
    num_rows = 100
    markets = ['PL', 'FR', 'KZ']
    categories = ['Piany', 'Kleje', 'Uszczelniacze']
    brands = ['Tytan Professional', 'Quilosa', 'Artelit']
    
    data = []
    # Generujemy 10 unikalnych EAN-ów dla duplikatów
    duplicate_eans = [f'{random.randint(10**12, 10**13-1)}' for _ in range(10)]
    
    i = 0
    while len(data) < num_rows:
        # Generujemy pary duplikatów (pierwsze 20 rekordów to 10 par)
        if i < 10:
            ean = duplicate_eans[i]
            # Rekord A
            sku_a = f'SEL-{1000 + (i*2)}'
            name_a = f"{random.choice(brands)} Piana 65"
            data.append([sku_a, name_a, ean, 'PL', 25, f"https://selena.com/msds/{sku_a}.pdf", 'Piany'])
            # Rekord B (Duplikat EAN, inne SKU)
            sku_b = f'SEL-{1000 + (i*2) + 1}'
            name_b = f"{name_a} - DUPLIKAT SYSTEMOWY"
            data.append([sku_b, name_b, ean, 'FR', "25 kg/m3", "", "Unmapped_FR"])
            i += 1
        else:
            # Reszta rekordów (unikalne)
            sku = f'SEL-{2000 + i}'
            market = random.choice(markets)
            product_name = f"{random.choice(brands)} {random.choice(['Klej', 'Silikon'])}"
            ean = f'{random.randint(10**12, 10**13-1)}'
            url = f"https://selena.com/msds/{sku}.pdf" if random.random() > 0.2 else ""
            category = "Unmapped_FR" if market == 'FR' else random.choice(categories)
            data.append([sku, product_name, ean, market, 28, url, category])
            i += 1
            
    df = pd.DataFrame(data, columns=['SKU', 'Product_Name', 'EAN', 'Market', 'Density_kg_m3', 'Safety_Sheet_URL', 'Category'])
    df.to_csv('data/selena_legacy_data.csv', index=False)
    print("Zaktualizowano generator: 10 par duplikatów umieszczono obok siebie (wiersze 0-19).")

if __name__ == "__main__":
    generate_selena_data()
