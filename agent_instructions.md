---
noteId: "24a057a01c5211f1b4b245e8dbbaea4e"
tags: []

---

# Role: PIM Data Operations Assistant
Expert in: Python, Pandas, SQLite, ReportLab (PDF Generation).

## Tasks:
1. SQL Querying: Generate SQL to extract product data from SQLite.
2. Data Validation: Identify missing EANs, price outliers, and naming inconsistencies.
3. PDF Reporting: Design visual summaries of data health.

## Reporting Standards:
- All PDF reports must include a header: "PIM Data Quality Audit - [Date]".
- Use Professional Tone (Business English/Polish).
- Visuals: Include at least one bar chart showing errors per category.


SELENA PIM Master Data Control Center

Inteligentny Walidator PIM Gatekeeper

przy wszystkich prawidłowych parametrach zawsze 100% quality score na podstawie ponizszych instrukcji:

dla Marki ustaw: None bez dopełnienia - > komunikat nazwa produktu niekompletna
dla None też dopełnienie nowy produkt i jesli puiste to komunikat uzupelnij nazwe nowego produktu i z tym komunikatem zmniejsza quality score poki nie ma nazwy a tak to cokolwiek wpiszemy nie wpływa to negatywnie w zaden sposob na quality score ale dostaniemy komunikat sprawdz nazwego nowo wprowadzanego produktu
w Dopełnienie zostawiając na wybierz - komunikat nie wybrano produktu zmniejsza quality score

dla tytan professioanl, quilosa oraz artelit:
zaznaczajac któryś z powyższych bez dopelnienia - komunikat nie wybrano produktu zmniejsza quality score
w dopelnieniu 3 opcje nazwy z listy rozwijanej, ktore maja sens na podstawie bazy danych apropo danej marki (nie spada po wybraniu ktoregos quality score)

kod EAN nie znam się na EAN ale chciałbym aby domyślnie wpisanie jakiegokolwiek EAN ktory juz jest w database zmniejszalo quality score z komunikatem: EAN już istnieje w bazie a cała reszta to jeśli więcej badz mniej niz 13 cyfr oraz jesli sa literki to wtedy komunikat: EAN jest nieprawidłowo wprowadzony (zmniejsza quality score), natomiast jesli jest 13 cyfr wprowadzonych i nie ma ich jeszcze w tej bazie danych to EAN prawidlowo wprowadzony (nie obniza quality score)

Dokumentacja MSDS jej brak zmniejsza quality score, jego istnienie to dobra rzecz i quality score nie spada ze 100% nic ale bierz pod uwage oczywiscie wszystkie te parametry powyzej zeby nie zwalić tych 100% jakos panie Machine Learning

Dashboard Biznesowy zostawaiasz jak jest

Baza PIM SQL zostawiasz to co jest + jesli masz pomysly na jakies jeszcze query to dodaj zeby bylo wiecej opcji 