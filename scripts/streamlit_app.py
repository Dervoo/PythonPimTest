import streamlit as st
import pandas as pd
import sqlite3
import os
import sys

# Dodajemy folder scripts do path, aby moc zaimportowac gatekeepera
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from pim_gatekeeper import PIMGatekeeper
except ImportError:
    # Fallback dla uruchamiania z roznych poziomow katalogow
    sys.path.append(os.path.join(os.getcwd(), 'scripts'))
    from scripts.pim_gatekeeper import PIMGatekeeper

# Konfiguracja strony
st.set_page_config(page_title="Selena PIM - Gatekeeper Center", layout="wide", page_icon="🛡️")

# Sciezki
DB_PATH = 'pim_database.db'
CLEAN_DATA_CSV = 'data/selena_final_master_data.csv'

def get_db_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

@st.cache_data
def load_clean_data():
    if os.path.exists(CLEAN_DATA_CSV):
        return pd.read_csv(CLEAN_DATA_CSV)
    return pd.DataFrame()

# Inicjalizacja Gatekeepera
gatekeeper = PIMGatekeeper()

# --- UI ---
st.title("🛡️ SELENA PIM Master Data Control Center")
st.markdown("### *Inteligentny Walidator PIM Gatekeeper & ML Analysis*")

df_clean = load_clean_data()
app_mode = st.sidebar.selectbox("Nawigacja", ["Dashboard Biznesowy", "PIM Gatekeeper (Validation)", "Baza PIM (SQL)"])

if app_mode == "Dashboard Biznesowy":
    st.header("📊 Dashboard Biznesowy - Analityka Cenowa i Jakosciowa")
    
    if not df_clean.empty:
        # KPI Cards
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Wszystkie SKU", len(df_clean))
        msds_rate = df_clean['Has_MSDS'].astype(bool).mean() if 'Has_MSDS' in df_clean.columns else 0
        c2.metric("E-com Ready (MSDS)", f"{msds_rate*100:.1f}%")
        
        avg_price = df_clean['Price'].mean() if 'Price' in df_clean.columns else 0
        c3.metric("Sredni Price", f"{avg_price:.2f} PLN")
        c4.metric("Status Bazy", "ZWALIDOWANO")
        
        st.divider()
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.subheader("Srednie Ceny per Kategoria (Dane SQL)")
            conn = get_db_connection()
            try:
                df_prices = pd.read_sql_query("SELECT * FROM View_Price_Analytics", conn)
                if not df_prices.empty:
                    st.bar_chart(df_prices.set_index('Category_Name')['Avg_Price'])
                else:
                    st.info("Baza SQL nie zawiera jeszcze danych analitycznych.")
            except:
                st.info("Uruchom skrypt update_sql_queries.py, aby aktywowac widoki SQL.")
            conn.close()
        
        with col_right:
            st.subheader("Rozklad Produktow per Rynek")
            st.bar_chart(df_clean['Market'].value_counts())
            
        st.subheader("Podglad Master Data (Top 50)")
        st.dataframe(df_clean.head(50), use_container_width=True)
    else:
        st.error("Brak danych w data/selena_final_master_data.csv. Uruchom skrypty przygotowujace dane.")

elif app_mode == "PIM Gatekeeper (Validation)":
    st.header("🧠 Inteligentny Walidator PIM Gatekeeper")
    st.info("System Machine Learning weryfikuje dane w czasie rzeczywistym zgodnie z instrukcjami Gatekeepera.")
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("Wprowadzanie Danych")
        # Wybor Marki
        brand_options = ["None", "Tytan Professional", "Quilosa", "Artelit"]
        brand_choice = st.selectbox("Marka", brand_options)
        
        # Wybor Dopelnienia - Dodano "Wpisz wlasna nazwe" zgodnie z instrukcja
        complements = ["Wybierz", "Klej do luster", "Piana 65 wysokowydajna", "Silikon Sanitarny", "Klej Montazowy", "Wpisz wlasna nazwe"]
        complement_choice = st.selectbox("Dopelnienie (Nazwa Produktu)", complements)
        
        final_complement = complement_choice
        # Logika dynamicznego pola tekstowego
        if complement_choice == "Wpisz wlasna nazwe":
            final_complement = st.text_input("Wpisz wlasna nazwe produktu", "")
            if not final_complement:
                final_complement = "" # To spowoduje obnizenie score przez Gatekeepera
        
        # EAN
        ean_input = st.text_input("Kod EAN (13 cyfr)", value="5901234567893")
        
        # MSDS
        msds_input = st.toggle("Dokumentacja MSDS Dostepna", value=True)
        
        st.divider()
        st.write("**Zasady Gatekeepera:**")
        st.write("- Wybranie 'Wpisz wlasna nazwe' bez wpisania nazwy obniza score.")
        st.write("- Marka 'None' zawsze dostaje komunikat o niekompletnej nazwie.")

    # --- URUCHOMIENIE WALIDACJI ---
    validation = gatekeeper.validate_product(
        brand=brand_choice if brand_choice != "None" else None,
        complement=final_complement,
        ean=ean_input,
        has_msds=msds_input
    )
    
    score = validation['quality_score']
    messages = validation['messages']

    with col2:
        st.subheader("Raport Jakosci (AI Audit)")
        
        score_color = "#e74c3c" if score < 60 else "#f39c12" if score < 95 else "#27ae60"
        st.markdown(f"""
            <div style='background-color:#f0f2f6; padding:20px; border-radius:10px; border-left: 10px solid {score_color};'>
                <h1 style='color:{score_color}; text-align:center;'>Quality Score: {score}%</h1>
            </div>
        """, unsafe_allow_html=True)
        st.progress(score / 100.0)
        
        if score == 100:
            st.success("💎 **PERFEKCYJNE MASTER DATA**: Produkt spełnia wszystkie wymogi Gatekeepera!")
            st.balloons()
        
        st.subheader("Komunikaty Gatekeepera:")
        for msg in messages:
            if "Brak Marki" in msg and brand_choice == "None" and complement_choice == "Wpisz wlasna nazwe":
                st.warning(f"⚠️ {msg}")
            elif "prawidlowo" in msg.lower() or "Sprawdz" in msg:
                st.info(f"✅ {msg}")
            else:
                st.error(f"❌ {msg}")

elif app_mode == "Baza PIM (SQL)":
    st.header("🔍 Eksplorator Bazy SQL (Nowe Zapytania)")
    
    scenarios = {
        "--- Wybierz zapytanie analityczne ---": "",
        "1. Analiza Cenowa (View_Price_Analytics)": "SELECT * FROM View_Price_Analytics",
        "2. Produkty Premium (View_Premium_Products)": "SELECT * FROM View_Premium_Products",
        "3. Podsumowanie bledow (View_Quality_Summary)": "SELECT * FROM View_Quality_Summary",
        "4. Lista Produktow (Top 50)": "SELECT SKU, Name, Price, Category_ID FROM Products LIMIT 50"
    }
    
    selected_query = st.selectbox("Scenariusze Biznesowe", list(scenarios.keys()))
    conn = get_db_connection()
    
    q_text = scenarios[selected_query] if scenarios[selected_query] else "SELECT * FROM View_Price_Analytics"
    query = st.text_area("Edytor SQL", q_text, height=120)
    
    if st.button("Uruchom SQL"):
        try:
            res_df = pd.read_sql_query(query, conn)
            st.dataframe(res_df, use_container_width=True)
            if "Avg_Price" in res_df.columns and "Category_Name" in res_df.columns:
                st.subheader("Wizualizacja Cenowa")
                st.bar_chart(res_df.set_index('Category_Name')['Avg_Price'])
        except Exception as e:
            st.error(f"Blad SQL: {e}")
    conn.close()
