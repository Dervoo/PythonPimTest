import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt
import datetime
import os
import sys

# Dodajemy folder scripts do path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from pim_gatekeeper import PIMGatekeeper
except ImportError:
    sys.path.append('.')
    from scripts.pim_gatekeeper import PIMGatekeeper

def clean_text(text):
    """Usuwa polskie znaki diakrytyczne dla kompatybilnosci z PDF latin-1."""
    if not isinstance(text, str):
        return str(text)
    mapping = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
        'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
    }
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text

def generate_audit():
    csv_path = 'data/selena_final_master_data.csv'
    if not os.path.exists(csv_path):
        print(f"Blad: Nie znaleziono pliku {csv_path}")
        return

    df = pd.read_csv(csv_path)
    gk = PIMGatekeeper()

    results = []
    for _, row in df.iterrows():
        brand = "None"
        for b in ["Tytan Professional", "Quilosa", "Artelit"]:
            if b in str(row['Product_Name']):
                brand = b
                break
        
        complement = str(row['Product_Name']).replace(str(brand), "").strip() if brand != "None" else str(row['Product_Name'])
        has_msds = str(row['Has_MSDS']).lower() == 'true'
        
        res = gk.validate_product(brand, complement, row['EAN'], has_msds)
        results.append(res)

    df_results = pd.DataFrame(results)
    df['Quality_Score'] = df_results['quality_score']
    df['Messages'] = df_results['messages'].apply(lambda x: "; ".join(x))

    # Wykres
    plt.figure(figsize=(10, 6))
    error_data = df[df['Quality_Score'] < 100]
    if not error_data.empty:
        error_counts = error_data.groupby('Category').size()
        error_counts.plot(kind='bar', color='#e74c3c')
    else:
        plt.text(0.5, 0.5, 'No Quality Issues Found!', ha='center')
        
    plt.title('Errors per Category (Quality Score < 100)')
    plt.ylabel('Number of Products with Issues')
    plt.xlabel('Category')
    plt.xticks(rotation=45)
    plt.tight_layout()
    chart_path = 'data/errors_per_category.png'
    plt.savefig(chart_path)
    plt.close()

    # PDF
    class PDF(FPDF):
        def header(self):
            self.set_font('Helvetica', 'B', 15)
            date_str = "2026-03-12"
            self.cell(0, 10, f'PIM Data Quality Audit - {date_str}', align='C', new_x='LMARGIN', new_y='NEXT')
            self.ln(2)
            self.set_font('Helvetica', 'B', 12)
            self.cell(0, 10, 'SELENA PIM Master Data Control Center', align='C', new_x='LMARGIN', new_y='NEXT')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Helvetica', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', align='C')

        def section(self, title):
            self.set_font('Helvetica', 'B', 12)
            self.set_fill_color(240, 240, 240)
            self.cell(0, 10, title, align='L', fill=True, new_x='LMARGIN', new_y='NEXT')
            self.ln(4)

    pdf = PDF()
    pdf.add_page()

    pdf.section('1. Gatekeeper Inteligentny Walidator - Summary')
    avg_score = df['Quality_Score'].mean()
    pdf.set_font('Helvetica', '', 11)
    status_text = "ZWALIDOWANO" if avg_score > 90 else "WYMAGA UWAGI"
    summary_text = (f"Sredni Quality Score bazy: {avg_score:.2f}%\n"
                    f"Status: {status_text}\n"
                    f"System Gatekeeper sprawdzil {len(df)} rekordow pod katem EAN, MSDS i Taksonomii Marek.")
    pdf.multi_cell(0, 10, clean_text(summary_text))

    pdf.ln(5)
    pdf.section('2. Data Issues per Category')
    if os.path.exists(chart_path):
        pdf.image(chart_path, x=15, w=180)
    
    pdf.ln(5)
    pdf.section('3. Top Quality Issues (Sample)')
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(30, 8, 'SKU', border=1)
    pdf.cell(30, 8, 'Score', border=1)
    pdf.cell(130, 8, 'Issues Found', border=1, new_x='LMARGIN', new_y='NEXT')

    pdf.set_font('Helvetica', '', 8)
    bad_samples = df[df['Quality_Score'] < 100].head(15)
    for _, row in bad_samples.iterrows():
        pdf.cell(30, 8, clean_text(str(row['SKU'])), border=1)
        pdf.cell(30, 8, f"{row['Quality_Score']}%", border=1)
        msg = clean_text(str(row['Messages'])[:85])
        pdf.cell(130, 8, msg, border=1, new_x='LMARGIN', new_y='NEXT')

    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    output_pdf = 'reports/Selena_Data_Audit.pdf'
    pdf.output(output_pdf)
    print(f"✅ Raport wygenerowany: {output_pdf}")

if __name__ == "__main__":
    generate_audit()
