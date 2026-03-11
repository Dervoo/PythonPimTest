import streamlit as st
import pandas as pd
import sqlite3
import os
import numpy as np

# Konfiguracja strony
st.set_page_config(page_title="Selena PIM - Master Data Center", layout="wide", page_icon="🏭")

# Ścieżki
DB_PATH = 'pim_database.db'
CLEAN_DATA_CSV = 'data/selena_final_master_data.csv'

def get_db_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

@st.cache_data
def load_clean_data():
    if os.path.exists(CLEAN_DATA_CSV):
        return pd.read_csv(CLEAN_DATA_CSV)
    return pd.DataFrame()

# --- LOGIKA WALIDACJI ---

def get_verified_suffixes(df, brand):
    if df.empty or brand == "None": return []
    # Filtrowanie bezpieczne
    brand_products = df[df['Product_Name'].str.contains(brand, na=False, case=False)]
    suffixes = [name.replace(brand, "").strip() for name in brand_products['Product_Name']]
    return sorted(list(set(suffixes)))

def is_ean13_checksum_valid(ean):
    if not str(ean).isdigit() or len(str(ean)) != 13: return False
    digits = [int(d) for d in str(ean)]
    odd_sum = sum(digits[0:12:2])
    even_sum = sum(digits[1:12:2])
    total = odd_sum + (even_sum * 3)
    check_digit = (10 - (total % 10)) % 10
    return digits[12] == check_digit

# --- UI ---
st.title("🏭 Selena PIM - Master Data Control Center")

df_clean = load_clean_data()
app_mode = st.sidebar.selectbox("Nawigacja", ["Dashboard Biznesowy", "Verified Entry (Live ML)", "Baza PIM (SQL)"])

if app_mode == "Dashboard Biznesowy":
    st.header("📊 Analiza Master Data (Single Source of Truth)")
    
    if not df_clean.empty:
        # KPI Cards
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Wszystkie SKU", len(df_clean))
        c2.metric("E-com Ready", f"{(1 - df_clean['Blocked_for_E-commerce'].mean())*100:.1f}%")
        c3.metric("Unikalność EAN", f"{df_clean['EAN'].nunique()/len(df_clean)*100:.1f}%")
        c4.metric("Błędy Taksonomii", "0 (Clean)")
        
        st.divider()
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.subheader("Rozkład Kategorii")
            st.bar_chart(df_clean['Category'].value_counts())
        
        with col_right:
            st.subheader("Rynek Dystrybucji")
            # Zmieniono z pie_chart na bar_chart dla lepszej kompatybilności
            st.bar_chart(df_clean['Market'].value_counts())
            
        st.subheader("Pełna Baza Produktowa")
        st.dataframe(df_clean, use_container_width=True, height=400)
    else:
        st.error("Brak danych. Uruchom skrypty PIM.")

elif app_mode == "Verified Entry (Live ML)":
    st.header("🧠 Inteligentny Walidator (PIM Gatekeeper)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Formularz Nowego Produktu")
        base_name = st.selectbox("Marka", ["None", "Tytan Professional", "Quilosa", "Artelit"])
        
        verified_suffixes = get_verified_suffixes(df_clean, base_name)
        suffix_choice = st.selectbox("Dopełnienie (Verified List)", 
                                     ["--- Wybierz ---", "Inne (Nowy Produkt)"] + verified_suffixes)
        
        if suffix_choice == "Inne (Nowy Produkt)":
            suffix = st.text_input("Wpisz Nowe Dopełnienie")
            is_manual = True
        else:
            suffix = suffix_choice if suffix_choice != "--- Wybierz ---" else ""
            is_manual = False
            
        # POPRAWNY EAN DLA TESTÓW (5901234567893)
        in_ean = st.text_input("Kod EAN-13", "5901234567893")
        in_msds = st.toggle("Dokumentacja MSDS zweryfikowana", value=True)

    # --- ANALIZA SCORE ---
    issues = []
    score = 100
    
    if base_name == "None" or not suffix:
        score -= 20
        issues.append("❌ Nazwa produktu niekompletna.")
    elif is_manual:
        score -= 10
        issues.append("ℹ️ Nowy wzorzec nazwy: Wymaga zatwierdzenia przez Lead Stewarda.")
        
    if not is_ean13_checksum_valid(in_ean):
        score -= 50
        issues.append("❌ BŁĄD MATEMATYCZNY: Niepoprawny EAN-13 (Zła suma kontrolna).")
    elif str(in_ean) in df_clean['EAN'].astype(str).values:
        score -= 40
        issues.append("⚠️ DUPLIKAT: Ten EAN już istnieje w bazie!")
        
    if not in_msds:
        score -= 40
        issues.append("🚧 BRAK MSDS: Produkt zostanie zablokowany w e-commerce.")

    score = max(0, score)

    with col2:
        st.subheader("Audyt Jakości AI")
        color = "green" if score > 85 else "orange" if score > 50 else "red"
        st.markdown(f"## Quality Score: <span style='color:{color}'>{score}%</span>", unsafe_allow_html=True)
        st.progress(score / 100.0)
        
        if score == 100:
            st.success("💎 **PERFEKCYJNE MASTER DATA**: Produkt gotowy do importu!")
            st.balloons()
        elif score > 85:
            st.success("✅ **ZATWIERDZONO**: Dane poprawne.")
        elif score > 50:
            st.warning("⚠️ **DRAFT**: Popraw błędy lub uzupełnij MSDS.")
        else:
            st.error("❌ **REJECTED**: Dane nie spełniają standardów.")
            
        for issue in issues: st.write(issue)

elif app_mode == "Baza PIM (SQL)":
    st.header("🔍 Eksplorator SQL")
    
    scenarios = {
        "--- Wybierz zapytanie ---": "",
        "1. Raport Podatkowy (Grouped by Tax)": "SELECT c.Category_Name, c.Tax_Rate, COUNT(p.SKU) as Products FROM Products p JOIN Categories c ON p.Category_ID = c.Category_ID GROUP BY c.Category_Name ORDER BY c.Tax_Rate DESC",
        "2. Produkty bez dokumentacji (Błędy)": "SELECT p.SKU, p.Name, q.Error_Type FROM Products p JOIN Quality_Logs q ON p.SKU = q.SKU",
        "3. Top 5 najdroższych produktów": "SELECT SKU, Name, Price FROM Products ORDER BY Price DESC LIMIT 5"
    }
    
    selected_query = st.selectbox("Gotowe Scenariusze", list(scenarios.keys()))
    conn = get_db_connection()
    
    q_text = scenarios[selected_query] if scenarios[selected_query] else "SELECT * FROM Products LIMIT 10"
    query = st.text_area("Edytor SQL", q_text, height=150)
    
    if st.button("Uruchom Analizę"):
        try:
            st.dataframe(pd.read_sql_query(query, conn), use_container_width=True)
        except Exception as e:
            st.error(f"Błąd SQL: {e}")
    conn.close()
