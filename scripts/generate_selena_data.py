import pandas as pd
import numpy as np
import random

def generate_selena_data():
    num_rows = 100
    markets = ['PL', 'FR', 'KZ']
    categories = ['Piany', 'Kleje', 'Uszczelniacze']
    brands = ['Tytan Professional', 'Quilosa', 'Artelit']
    
    data = []
    
    # Lista 10 EAN-ów do duplikacji
    duplicate_eans = [f'{random.randint(10**12, 10**13-1)}' for _ in range(10)]
    
    for i in range(num_rows):
        sku = f'SEL-{1000 + i}'
        market = random.choice(markets)
        brand = random.choice(brands)
        
        # Nazwa z błędami
        base_name = f"{brand} {random.choice(['Piana 65', 'Klej Fix2', 'Silikon Sanitarny'])}"
        if random.random() < 0.4:
            product_name = f"  {base_name.upper()}  "
        elif market == 'FR':
            product_name = f"Mousse {base_name}" # Francuskie nazewnictwo
        else:
            product_name = base_name
            
        # EAN i duplikaty
        if i < 10:
            ean = duplicate_eans[i]
        elif i < 20: # Duplikaty tych samych produktów pod innymi SKU
            ean = duplicate_eans[i-10]
        else:
            ean = f'{random.randint(10**12, 10**13-1)}'
            
        # Gęstość (Density)
        if market == 'FR':
            density = f"{random.randint(20, 30)} kg/m3" if random.random() > 0.2 else "brak"
        else:
            density = random.randint(20, 30) if random.random() > 0.1 else "brak"
            
        # Safety Sheet URL (brak u 20%)
        url = f"https://selena.com/msds/{sku}.pdf" if random.random() > 0.2 else ""
        
        # Kategoria (celowo pomieszana)
        category = random.choice(categories)
        
        data.append([sku, product_name, ean, market, density, url, category])
        
    df = pd.DataFrame(data, columns=['SKU', 'Product_Name', 'EAN', 'Market', 'Density_kg_m3', 'Safety_Sheet_URL', 'Category'])
    df.to_csv('selena_legacy_data.csv', index=False)
    print("Wygenerowano plik: selena_legacy_data.csv")

if __name__ == "__main__":
    generate_selena_data()
