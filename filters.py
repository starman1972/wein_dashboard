import streamlit as st

def apply_global_filters(data):
    # Sidebar-Widgets bauen → filter_params (dict) zurückgeben
    # (z.B. Jahrgang, Preis-Spanne, etc.)
    jahre = sorted(data['coop']["Jahrgang"].dropna().unique())
    jahrgang_sel = st.sidebar.multiselect("Jahrgang", jahre, default=jahre)
    return {'jahrgang': jahrgang_sel}