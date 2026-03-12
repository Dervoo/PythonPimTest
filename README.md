# 🏭 Selena FM - Case Study: PIM Data Operations & Integration
### Junior Data Steward Portfolio Project

---

## [PL] Opis Projektu
Ten projekt demonstruje proces **integracji i czyszczenia danych produktowych** po fuzji z nowym podmiotem (ACDIS France) oraz wejścia na rynek Kazachstanu. Jako PIM Specialist, moim zadaniem było doprowadzenie "brudnego" eksportu z systemów ERP do stanu **Master Data Ready (100% Quality)**.

## [EN] Project Description
This project demonstrates the process of **product data integration and cleansing** following a merger with a new entity (ACDIS France) and market entry into Kazakhstan. As a PIM Specialist, my task was to transform "dirty" ERP system exports into a **Master Data Ready (100% Quality)** state.

---

## 📊 1. Business Impact Summary / Podsumowanie Biznesowe
**[PL]:** Przed moją interwencją, baza zawierała krytyczne błędy blokujące sprzedaż:
*   **⚠️ 20% produktów zablokowanych**: Brak kart MSDS uniemożliwiał sprzedaż e-commerce.
*   **⚠️ 10% duplikatów EAN**: Błędy uniemożliwiały poprawne zarządzanie stanami.
*   **⚠️ Chaos Taksonomiczny**: Niespójne nazewnictwo (Mousse vs Piany).

**[EN]:** Before my intervention, the database contained critical errors blocking sales:
*   **⚠️ 20% products blocked**: Missing MSDS sheets prevented e-commerce listings.
*   **⚠️ 10% EAN duplicates**: Errors hindered correct inventory management.
*   **⚠️ Taxonomic Chaos**: Inconsistent naming conventions (Mousse vs Foams).

**WYNIK / RESULT:** Odblokowano 100% asortymentu / 100% of assortment unlocked for sales.

---

## 🛠 2. Technical Solutions / Rozwiązania Techniczne
**[PL]:** Z własnej inicjatywy zastąpiłem czasochłonną, manualną pracę w Excelu autorskimi rozwiązaniami, które zaprogramowałem, by działały pod moim nadzorem:
*   **Proaktywna Automatyzacja (Pandas)**: Samodzielnie zaprojektowałem i wdrożyłem algorytm deduplikacji, który wyeliminował błędy ludzkie przy czyszczeniu rekordów.
*   **Autorski Mapping Engine**: Stworzyłem system inteligentnego rozpoznawania francuskiego nazewnictwa, mapujący je na standardy Seleny bez potrzeby ręcznej korekty każdego wiersza.
*   **Architektura Relacyjna (SQLite)**: Zaprojektowałem i zbudowałem bazę danych "Single Source of Truth", zapewniając integralność danych, której nie gwarantowały rozproszone arkusze.

**[EN]:** On my own initiative, I replaced time-consuming manual Excel work with custom solutions I programmed to operate under my expert supervision:
*   **Proactive Automation (Pandas)**: I independently designed and implemented a deduplication algorithm that eliminated human error during record cleansing.
*   **Custom Mapping Engine**: I developed an intelligent recognition system for French terminology, mapping it to Selena standards without requiring manual corrections for every row.
*   **Relational Architecture (SQLite)**: I designed and built a "Single Source of Truth" database, ensuring data integrity that scattered spreadsheets could not provide.

---

## 📂 3. Portfolio Overview / Przegląd Portfolio
*   📁 **[data/](data/)**: Master Data files & visualizations.
*   📁 **[reports/](reports/)**: Professional PDF audits for the Board.
*   📁 **[notebooks/](notebooks/)**: Full data cleansing logic (Jupyter).

---

## 📈 4. Key Metrics (KPI) / Kluczowe Metryki
| Metryka / Metric | Start | Final |
| :--- | :--- | :--- |
| **E-commerce Ready** | 82.0% | **100.0%** |
| **EAN Uniqueness** | 90.0% | **100.0%** |
| **Taxonomy Consistency** | Low | **High** |

---

## 👤 5. Human-in-the-Loop: Expert Oversight / Rola Ekspercka (Klucz do Sukcesu)

**[PL]:** Projekt ten jest koronnym dowodem na to, że **sama maszyna ML nie dawała rady** z poprawnym stworzeniem modelu walidacyjnego bez precyzyjnego nadzoru. Dopiero po skonstruowaniu **zaawansowanych instrukcji o wysokiej dokładności**, Gatekeeper zaczął działać zgodnie ze standardami biznesowymi.

*   **⚠️ Przełamanie Ograniczeń ML**: Zaprojektowałem autorską logikę, która wymusza obecność marki Seleny, co wcześniej było pomijane przez automaty.
*   **💡 Precyzyjna Kalibracja (Logic Fix)**: Skalibrowałem system punktacji tak, aby produkt bez marki, nazwy, EAN i MSDS otrzymywał **0% Quality Score** (wyeliminowanie "punktów za nic").
*   **📱 Integracja Mobilna (Tablet Optimization)**: Wdrożyłem pełną responsywność wykresów (`use_container_width`), optymalizując dashboard pod pracę stewardów w terenie na tabletach.
*   **🔍 UI/UX Validation**: Skorygowałem błędy wizualne w Streamlit – teraz niepoprawny kod EAN jest natychmiast oznaczany czerwonym krzyżykiem (❌) zamiast mylącego zielonego ptaszka.

**[EN]:** This project is ultimate proof that **ML alone was insufficient** to create a proper validation model without precise oversight. Only after constructing **advanced, high-accuracy instructions** did the Gatekeeper meet business standards.

*   **⚠️ Overcoming ML Limits**: I designed custom logic to enforce Selena branding, which was previously overlooked by automated systems.
*   **💡 Precision Calibration (Logic Fix)**: Calibrated the scoring system so that a product without brand, name, EAN, and MSDS receives **0% Quality Score** (eliminating "points for nothing").
*   **📱 Mobile Integration (Tablet Optimization)**: Implemented full chart responsiveness (`use_container_width`), optimizing the dashboard for stewards working in the field on tablets.
*   **🔍 UI/UX Validation**: Corrected visual bugs in Streamlit – incorrect EAN codes are now immediately flagged with a red cross (❌) instead of a misleading green checkmark.

---

## 🚀 6. How to Run / Jak to uruchomić?
```powershell
# Install / Instalacja
py -m pip install pandas fpdf matplotlib openpyxl streamlit scikit-learn

# Process / Przetwarzanie
py scripts/setup_database.py
py scripts/generate_selena_data.py
py scripts/selena_final_fix.py

# Dashboard
py -m streamlit run scripts/streamlit_app.py
```

---
**PIM Data Operations Assistant Portfolio** | *Autor: Bartosz Osiński | *Python, SQL, Excel, Streamlit*
