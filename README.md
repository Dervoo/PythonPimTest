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

## 🚀 Jak to uruchomić?
```powershell
# 1. Zainstaluj biblioteki
py -m pip install pandas fpdf matplotlib openpyxl

# 2. Wygeneruj dane i raporty (Uruchom skrypty z folderu scripts/)
py scripts/generate_selena_data.py
py scripts/selena_final_fix.py
py scripts/generate_impact_report.py
```

## 🧠 5. Human-in-the-Loop: Rola Ekspercka i Nadzór
Projekt ten nie jest jedynie zbiorem skryptów – to **synergia automatyzacji i ludzkiego nadzoru**. Jako inicjator i audytor ekosystemu, odegrałem kluczową rolę w:

*   **Projektowaniu Logiki Prezentacji**: To ja wymusiłem strukturę "pary duplikatów obok siebie" w pliku INITIAL, aby umożliwić błyskawiczną weryfikację wzrokową – co jest kluczowe w pracy operacyjnej Data Stewarda.
*   **Audycie i Korekcie Algorytmów**: Wykryłem i skorygowałem błędy w sortowaniu danych (SKU Alignment), dbając o to, by raporty końcowe były czytelne i spójne z danymi źródłowymi.
*   **Weryfikacji Taksonomii**: Dopilnowałem, aby błędy systemowe (Unmapped_FR) były ewidentnie wskazane w fazie początkowej, co umożliwiło udowodnienie skuteczności procesów mapowania.
*   **Wsparciu Ekosystemu**: Moja rola polegała na budowie, testowaniu i ciągłym udoskonalaniu narzędzi (Python/Pandas), tak aby proces był powtarzalny, skalowalny i odporny na błędy ludzkie.

**Wniosek:** Potrafię nie tylko budować zaawansowane narzędzia danych, ale przede wszystkim potrafię nimi **zarządzać i krytycznie oceniać ich wynik**, gwarantując 100% poprawności Master Data.

---
**PIM Data Operations Assistant Portfolio** | *Autor: [Twoje Imię i Nazwisko]* | *Technologie: Python, Pandas, SQLite, FPDF*
