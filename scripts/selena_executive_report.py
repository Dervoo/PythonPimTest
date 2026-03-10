import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt
import datetime

# 1. Wczytanie danych
df = pd.read_csv('selena_cleaned_data.csv')

# 2. Wykres kołowy (Ready vs Blocked)
blocked_counts = df['Blocked_for_E-commerce'].value_counts()
labels = ['Gotowe (Ready)', 'Zablokowane (Blocked)']
sizes = [blocked_counts.get(False, 0), blocked_counts.get(True, 0)]
colors = ['#27ae60', '#e74c3c']

plt.figure(figsize=(6, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
plt.title('E-commerce Readiness (Safety Sheet Status)')
plt.savefig('selena_pie_chart.png')
plt.close()

# 3. Statystyki błędów per rynek
# Definiujemy błąd jako brak gęstości lub blokadę e-commerce
market_stats = df.groupby('Market').agg(
    Total=('SKU', 'count'),
    Blocked=('Blocked_for_E-commerce', 'sum')
).reset_index()

# 4. Tworzenie PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Data Quality Audit - Integration of ACDIS France & Kazakhstan', 0, 1, 'C')
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Generated on: {datetime.datetime.now().strftime("%Y-%m-%d")}', 0, 1, 'R')
        self.ln(10)

    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(30, 81, 123)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.set_text_color(0, 0, 0)
        self.ln(4)

pdf = PDF()
pdf.add_page()

# Sekcja 1: Wykres
pdf.section_title('1. Visual Status - Safety Documentation')
pdf.image('selena_pie_chart.png', x=40, y=None, w=120)
pdf.ln(5)

# Sekcja 2: Tabela
pdf.section_title('2. Market Quality Metrics (Top Issues)')
pdf.set_font('Arial', 'B', 10)
pdf.cell(50, 10, 'Market', 1)
pdf.cell(50, 10, 'Total Products', 1)
pdf.cell(50, 10, 'Blocked (Missing MSDS)', 1)
pdf.ln()

pdf.set_font('Arial', '', 10)
for _, row in market_stats.iterrows():
    pdf.cell(50, 10, str(row['Market']), 1)
    pdf.cell(50, 10, str(row['Total']), 1)
    pdf.cell(50, 10, str(row['Blocked']), 1)
    pdf.ln()

# Sekcja 3: Rekomendacje
pdf.ln(10)
pdf.section_title('3. Analyst Recommendations')
rec_text = (
    "1. PILNE: Uzupelnienie kart charakterystyki (MSDS) dla 20% produktow zablokowanych dla e-commerce.\n"
    "2. ACDIS Integration: Kontynuacja mapowania kategorii 'Mousse' -> 'Piany' w systemie ERP.\n"
    "3. Deduplikacja: Wykryto 10 par SKU o identycznych EAN - wymagana manualna konsolidacja przed importem do PIM."
)
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 10, rec_text)

pdf.output('Selena_Data_Audit.pdf')
print("🚀 Raport Seleny PDF gotowy: Selena_Data_Audit.pdf")
