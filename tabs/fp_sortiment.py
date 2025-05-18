# tabs/fp_sortiment.py

import streamlit as st
from plot_utils import (
    plot_weintypen_pie_and_table,
    plot_preisklassen_pie_and_table,
    plot_preisverteilung_nach_weintyp,
    plot_top_herkunftslaender_fp,    # <-- ACHTUNG, Flaschenpost-spezifische Funktion!
    plot_italien_regionen_fp,
    plot_frankreich_regionen_fp,
    plot_spanien_regionen_fp,
    plot_schweiz_regionen_fp,
    # Falls du schon FP-spezifische Regionenfunktionen hast, hier importieren:
    # plot_frankreich_regionen_fp,
    # plot_italien_regionen_fp,
    # plot_schweiz_regionen_fp,
    # plot_spanien_regionen_fp
)

def show_fp_sortiment_tab(df):
    st.header("Flaschenpost-Sortimentsanalyse")

    with st.expander("1. Verteilung der Weintypen", expanded=True):
        plot_weintypen_pie_and_table(
            df, 
            weintyp_col="Weintyp", 
            titel="Verteilung der Weintypen im Flaschenpost-Sortiment"
        )

    with st.expander("2. Verteilung der Preisklassen"):
        plot_preisklassen_pie_and_table(
            df, 
            preis_col="Preis", 
            bins=[0, 20, 50, 100, df["Preis"].max()],
            labels=["0–20 CHF", "20–50 CHF", "50–100 CHF", "100+ CHF"],
            titel="Verteilung der Preisklassen im Flaschenpost-Sortiment"
        )

    with st.expander("3. Preisverteilung nach Weintyp"):
        plot_preisverteilung_nach_weintyp(
            df,
            preis_col="Preis",
            weintyp_col="Weintyp",
            bins=[0, 20, 50, 100, df["Preis"].max()],
            labels=["0–20 CHF", "20–50 CHF", "50–100 CHF", "100+ CHF"],
            titel="Preisverteilung nach Weintyp im Flaschenpost-Sortiment"
        )

    with st.expander("4. Top-10 Herkunftsländer"):
        plot_top_herkunftslaender_fp(
            df, 
            herkunft_col="Herkunft", 
            titel="Top-10 Herkunftsländer im Flaschenpost-Sortiment"
        )

    with st.expander("6. Regionen Italiens"):
        plot_italien_regionen_fp(
            df, herkunft_col="Herkunft", titel="Weinregionen Italiens im Flaschenpost-Sortiment"
        )

    with st.expander("5. Regionen Frankreichs"):
        plot_frankreich_regionen_fp(
            df, herkunft_col="Herkunft", titel="Weinregionen Frankreichs im Flaschenpost-Sortiment"
        )

    with st.expander("8. Regionen Spanien"):
        plot_spanien_regionen_fp(
            df, herkunft_col="Herkunft", titel="Weinregionen Spaniens im Flaschenpost-Sortiment"
        )

    with st.expander("7. Regionen Schweiz"):
        plot_schweiz_regionen_fp(
            df, herkunft_col="Herkunft", titel="Weinregionen der Schweiz im Flaschenpost-Sortiment"
        )


    # Jetzt hier analog, sobald spezialisierte Mapping/Regions-Funktionen für Flaschenpost bereitstehen:
    # with st.expander("5. Regionen Frankreichs"):
    #     plot_frankreich_regionen_fp(df, ...)
    # with st.expander("6. Regionen Italiens"):
    #     plot_italien_regionen_fp(df, ...)
    # with st.expander("7. Regionen Schweiz"):
    #     plot_schweiz_regionen_fp(df, ...)
    # with st.expander("8. Regionen Spanien"):
    #     plot_spanien_regionen_fp(df, ...)