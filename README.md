# 🏭 Selena FM - Case Study: PIM Data Operations & Integration
### Junior Data Steward Portfolio Project

Ten projekt demonstruje proces **integracji i czyszczenia danych produktowych** po fuzji z nowym podmiotem (ACDIS France) oraz wejścia na rynek Kazachstanu. Jako PIM Specialist, moim zadaniem było doprowadzenie "brudnego" eksportu z systemów ERP do stanu **Master Data Ready (100% Quality)**.

---

## 📊 1. Business Impact Summary (Dlaczego to ważne?)
Przed moją interwencją, baza zawierała krytyczne błędy blokujące sprzedaż i skalowanie:
*   **⚠️ 20% produktów zablokowanych**: Brak kart charakterystyki (MSDS) uniemożliwiał wystawienie chemii budowlanej w e-commerce.
*   **⚠️ 10% duplikatów EAN**: Błędne przypisania uniemożliwiały poprawne zarządzanie stanami magazynowymi.
*   **⚠️ Chaos Taksonomiczny**: Rynek francuski używał niespójnego nazewnictwa (Mousse vs Piany), co psuło filtry w sklepie online.

**WYNIK:** Odblokowano **100% asortymentu do sprzedaży** i skonsolidowano bazę do **jedynego źródła prawdy (Single Source of Truth)**.

---

## 🛠 2. Moje Rozwiązania Techniczne (Zadania PIM)
W projekcie wykorzystałem nowoczesne narzędzia zamiast manualnej pracy w Excelu:

### ✅ Automatyczna Deduplikacja (Pandas)
Zaimplementowałem algorytm, który automatycznie wykrył duplikaty po kodzie EAN i wybrał rekordy o najwyższej jakości (te, które posiadały już uzupełnione linki do dokumentacji).

### ✅ Mapowanie Międzynarodowe (ACDIS FR)
Stworzyłem regułę mapowania, która automatycznie rozpoznaje francuskie nazewnictwo ("Mousse") i mapuje je do poprawnej kategorii "Piany" w centralnej bazie Seleny.

### ✅ Recovery System (MSDS)
Napisałem skrypt, który zidentyfikował brakujące linki do dokumentacji bezpieczeństwa i automatycznie je uzupełnił z serwera, odblokowując produkty do sprzedaży e-commerce.

### ✅ Architektura Relacyjna (SQLite)
Zaprojektowałem strukturę bazy danych z podziałem na Produkty, Kategorie i Logi Jakości, co zapewnia skalowalność systemu PIM.

---

## 📂 3. Przegląd Portfolio (Co znajdziesz w repo?)
*   📁 **[data/](data/)**: Pliki Master Data i wizualizacje procesów.
*   📁 **[reports/](reports/)**: Profesjonalne audyty PDF – gotowe do prezentacji zarządowi.
*   📁 **[notebooks/](notebooks/)**: Pełna ścieżka logiczna czyszczenia danych (Jupyter).

### 🔍 Porównanie Arkuszy Excel (Kluczowy Dowód)
Oto bezpośrednie zestawienie bazy danych **Przed** i **Po** mojej interwencji. 
**Ważne:** Cały proces został poddany manualnej weryfikacji (Human Verification) w celu potwierdzenia poprawności algorytmów mapowania i deduplikacji.

1.  📉 **[Selena_Legacy_Data_INITIAL.xlsx](Selena_Legacy_Data_INITIAL.xlsx)**: Surowy eksport z ERP (Widoczne duplikaty EAN, błędy 'Unmapped_FR' oraz braki dokumentacji).
2.  📈 **[Selena_Master_Data_FINAL.xlsx](Selena_Master_Data_FINAL.xlsx)**: Czysta baza Master Data (Zweryfikowana przez Data Stewarda, 100% spójności, gotowa do importu).

---

## 📈 4. Kluczowe Metryki (KPI)
| Metryka | Stan Początkowy | Stan Końcowy |
| :--- | :--- | :--- |
| **Gotowość E-commerce** | 82.0% | **100.0%** |
| **Unikalność EAN** | 90.0% | **100.0%** |
| **Spójność Taksonomii** | Niska (Błędy FR) | **Wysoka (Pełne mapowanie)** |

---

## 🚀 4. Jak to uruchomić?

### Krok 1: Instalacja wymaganych bibliotek
Aby uruchomić pełną analitykę i dashboard, zainstaluj zależności:
```powershell
py -m pip install pandas fpdf matplotlib openpyxl streamlit scikit-learn
```

### Krok 2: Generowanie danych i raportów (Silnik PIM)
Uruchom skrypty przetwarzające dane:
```powershell
py scripts/setup_database.py
py scripts/generate_selena_data.py
py scripts/selena_final_fix.py
py scripts/generate_impact_report.py
```

### Krok 3: Interaktywny Dashboard (BI & Live ML)
Uruchom nowoczesny dashboard z modułem Machine Learning:
```powershell
# Jeśli 'streamlit' nie jest w PATH, użyj modułu python:
py -m streamlit run scripts/streamlit_app.py
```

---

## 🧠 5. Inteligentny Dashboard (Co znajdziesz w środku?)
Stworzony dashboard w **Streamlit** to centrum dowodzenia Data Stewarda:
*   **Verified Entry (Live ML)**: System ekspercki z walidacją sumy kontrolnej EAN-13 i sprawdzaniem unikalności w bazie w czasie rzeczywistym.
*   **Business Intelligence**: Karty KPI pokazujące gotowość e-commerce, rozkład kategorii i rynków.
*   **SQL Explorer**: Biblioteka gotowych scenariuszy analitycznych (podatki, braki MSDS, ceny).

---

## 👤 6. Human-in-the-Loop: Rola Ekspercka i Nadzór (Klucz do Sukcesu)
Projekt ten jest koronnym dowodem na to, że **sama maszyna ML nie dawała rady** z poprawnym stworzeniem modelu walidacyjnego bez precyzyjnego nadzoru. Dopiero po skonstruowaniu **zaawansowanych instrukcji o wysokiej dokładności** i iteracyjnym "dokarmianiu" systemu wiedzą dziedzinową, Gatekeeper zaczął działać zgodnie z rygorystycznymi standardami biznesowymi.

Jako Data Steward i Architekt Systemu, odegrałem kluczową rolę w eliminacji błędów, których algorytmy "pudełkowe" nie potrafiły wychwycić:

*   **⚠️ Przełamanie Ograniczeń ML**: Standardowe modele klasyfikacji nie rozumiały niuansów brandingu Seleny. Musiałem zaprojektować autorską logikę "Gatekeepera", która twardo egzekwuje obecność marki (Tytan, Quilosa, Artelit) i blokuje niekompletne rekordy, co wcześniej było pomijane przez automaty.
*   **💡 Precyzyjna Kalibracja Komunikatów**: Wprowadziłem inteligentne stopniowanie alertów. Przykład: Gdy użytkownik wybiera opcję "Wpisz własną nazwę" przy braku marki (None), system nie blokuje pracy błędem (Red), lecz wyświetla **ostrzeżenie (Yellow)**. To efekt mojej decyzji biznesowej o zachowaniu elastyczności procesu przy jednoczesnym monitoringu jakości.
*   **Korekta Logiki Walidacji**: Wykryłem, że pierwotny model błędnie podnosił jakość przy braku dokumentacji MSDS. Wymusiłem rygorystyczną zasadę: "Brak MSDS = Obniżenie Score o 20% i Status Draft".
*   **Walidacja Matematyczna (EAN-13)**: Zakwestionowałem akceptowanie dowolnych 13 cyfr. Dzięki temu zaimplementowano algorytm weryfikacji unikalności EAN względem bazy Master Data w czasie rzeczywistym.
*   **Zapewnienie Spójności Danych (PIM Dictionary)**: Zainicjowałem stworzenie dynamicznego słownika dopełnień nazw. Zamiast wolnego tekstu, system wymusza teraz zweryfikowane wzorce, co eliminuje błędy literowe (np. "Pianka" vs "Piana").

**Wniosek:** Projekt pokazuje moją zdolność do **zarządzania AI jako narzędziem**, krytycznej oceny wyników maszynowych i dostarczania technologii, która realnie spełnia wymogi biznesowe dzięki precyzyjnemu "Human Steering".

---
**PIM Data Operations Assistant Portfolio** | *Autor: Bartosz Osiński | *Technologie: Python, Pandas, SQLite, Streamlit, Scikit-learn*

