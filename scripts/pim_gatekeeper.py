import sqlite3
import pandas as pd
import re

class PIMGatekeeper:
    def __init__(self, db_path='pim_database.db'):
        self.db_path = db_path
        self.quality_score = 100
        self.messages = []
        self.existing_eans = self._load_existing_eans()

    def _load_existing_eans(self):
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT EAN FROM Products", conn)
            conn.close()
            return set(df['EAN'].astype(str).str.replace(r'\.0$', '', regex=True).tolist())
        except Exception as e:
            return set()

    def validate_product(self, brand, complement, ean, has_msds):
        self.quality_score = 100
        self.messages = []

        # 1. Walidacja Marki i Dopelnienia (Bez polskich znakow dla PDF)
        if brand is None or brand == "None":
            self.messages.append("Nazwa produktu niekompletna (Brak Marki)")
            if not complement or complement == "" or complement == "Wybierz":
                self.messages.append("Uzupelnij nazwe nowego produktu")
                self.quality_score -= 20
        elif brand in ["Tytan Professional", "Quilosa", "Artelit"]:
            if not complement or complement == "Wybierz" or complement == "":
                self.messages.append(f"Nie wybrano produktu dla marki {brand}")
                self.quality_score -= 15
            else:
                self.messages.append(f"Sprawdz nazwe nowo wprowadzanego produktu ({brand} {complement})")
        
        if complement == "Wybierz":
            if not any("Nie wybrano produktu" in msg for msg in self.messages):
                self.messages.append("Nie wybrano produktu")
                self.quality_score -= 10

        # 2. Walidacja EAN
        ean_str = str(ean).strip().replace('.0', '')
        if ean_str in self.existing_eans:
            self.messages.append("EAN juz istnieje w bazie")
            self.quality_score -= 25
        elif not (len(ean_str) == 13 and ean_str.isdigit()):
            self.messages.append("EAN jest nieprawidlowo wprowadzony")
            self.quality_score -= 15
        else:
            self.messages.append("EAN prawidlowo wprowadzony")

        # 3. Walidacja MSDS
        if not has_msds or has_msds == "False" or has_msds is False:
            self.messages.append("Brak dokumentacji MSDS")
            self.quality_score -= 20

        self.quality_score = max(0, self.quality_score)
        
        return {
            "quality_score": self.quality_score,
            "messages": self.messages,
            "status": "Green" if self.quality_score == 100 else "Yellow" if self.quality_score > 70 else "Red"
        }
