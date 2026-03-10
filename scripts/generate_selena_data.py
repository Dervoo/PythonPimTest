import pandas as pd
import numpy as np
import random

def generate_selena_data():
    num_rows = 100
    markets = ['PL', 'FR', 'KZ']
    categories = ['Piany', 'Kleje', 'Uszczelniacze']
    brands = ['Tytan Professional', 'Quilosa', 'Artelit']
    
    data = []
    duplicate_eans = [f'{random.randint(10**12, 10**13-1)}' for _ in range(10)]
    
    for i in range(num_rows):
        sku = f'SEL-{1000 + i}'
        market = random.choice(markets)
        brand = random.choice(brands)
        
        # Nazwa produktu
        base_name = f"{brand} {random.choice(['Piana 65', 'Klej Fix2', 'Silikon Sanitarny'])}"
        if market == 'FR':
            product_name = f"Mousse {base_name}"
        else:
            product_name = base_name if random.random() > 0.3 else f"  {base_name.upper()}  "
            
        # EAN i duplikaty
        if i < 10: ean = duplicate_eans[i]
        elif i < 20: ean = duplicate_eans[i-10]
        else: ean = f'{random.randint(10**12, 10**13-1)}'
            
        # Gęstość
        density = f"{random.randint(20, 30)} kg/m3" if market == 'FR' else random.randint(20, 30)
        
        # MSDS URL (20% braków)
        url = f"https://selena.com/msds/{sku}.pdf" if random.random() > 0.2 else ""
        
        # --- KLUCZOWA ZMIANA: BŁĄD TAKSONOMICZNY ---
        if market == 'FR' and "Mousse" in product_name:
            # Wstawiamy BŁĘDNĄ kategorię w pliku INITIAL, aby pokazać proces mapowania
            category = "Unmapped_FR" 
        else:
            category = random.choice(categories)
        
        data.append([sku, product_name, ean, market, density, url, category])
        
    df = pd.DataFrame(data, columns=['SKU', 'Product_Name', 'EAN', 'Market', 'Density_kg_m3', 'Safety_Sheet_URL', 'Category'])
    df.to_csv('data/selena_legacy_data.csv', index=False)
    print("Zaktualizowano plik źródłowy z widocznymi błędami taksonomii (Unmapped_FR).")

if __name__ == "__main__":
    generate_selena_data()
