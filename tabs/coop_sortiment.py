# tabs/coop_sortiment.py

import streamlit as st
# … bisherige Importe oben …
from plot_utils import (
    plot_weintypen_pie_and_table,
    plot_preisklassen_pie_and_table,
    plot_preisverteilung_nach_weintyp,
    plot_top_herkunftslaender,
    plot_frankreich_regionen,
    plot_italien_regionen,
    plot_schweiz_regionen,
    plot_spanien_regionen         # <--- NEU!
)

def show_coop_sortiment_tab(df):
    st.header("Coop-Sortimentsanalyse")

    with st.expander("1. Verteilung der Weintypen", expanded=True):
        plot_weintypen_pie_and_table(df, weintyp_col="Weintyp", titel="Verteilung der Weintypen im coop.ch-Sortiment")
    with st.expander("2. Verteilung der Preisklassen"):
        plot_preisklassen_pie_and_table(df, preis_col="Preis", bins=[0, 20, 50, 100, df["Preis"].max()],
                                        labels=["0–20 CHF", "20–50 CHF", "50–100 CHF", "100+ CHF"],
                                        titel="Verteilung der Preisklassen im coop.ch-Sortiment")
    with st.expander("3. Preisverteilung nach Weintyp"):
        plot_preisverteilung_nach_weintyp(df, preis_col="Preis", weintyp_col="Weintyp", bins=[0, 20, 50, 100, df["Preis"].max()],
                                          labels=["0–20 CHF", "20–50 CHF", "50–100 CHF", "100+ CHF"],
                                          titel="Preisverteilung nach Weintyp im coop.ch-Sortiment")
    with st.expander("4. Top-10 Herkunftsländer"):
        plot_top_herkunftslaender(df, region_col="Region", titel="Top-10 Herkunftsländer im coop.ch-Sortiment")
    with st.expander("5. Regionen Frankreichs"):
        plot_frankreich_regionen(df, region_col="Region", titel="Weinregionen Frankreichs im coop.ch-Sortiment")
    with st.expander("6. Regionen Italiens"):
        plot_italien_regionen(df, region_col="Region", titel="Weinregionen Italiens im coop.ch-Sortiment")
    with st.expander("7. Regionen Schweiz"):
        plot_schweiz_regionen(df, region_col="Region", titel="Weinregionen der Schweiz im coop.ch-Sortiment")
    with st.expander("8. Regionen Spanien"):
        plot_spanien_regionen(df, region_col="Region", titel="Weinregionen Spaniens im coop.ch-Sortiment")