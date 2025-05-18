# tabs/matching.py
import streamlit as st
import pandas as pd # Wichtig für pd.to_numeric und pd.NA
from plot_utils import (
    plot_matching_overview_gemini,
    plot_percent_price_comparison_gemini1,
    plot_price_outlier_table_enhanced,
    plot_matched_performance_analysis,
    plot_sweet_spot_analysis
)

def show_matching_tab(df_input): # df_input ist dein angereichertes matching_df
    st.header("Matching-/Preisvergleich Coop ⇆ Flaschenpost")

    # --- Zentrale Spaltenerstellung / -umbenennung ---
    df = df_input.copy() # Arbeite immer mit einer Kopie

    # Numerische Konvertierungen (Beispiel, anpassen an die Spalten, die es brauchen)
    cols_to_convert_numeric = ["Coop_Preis", "FP_Preis", "NPS_FP", "Fuzzy_Score"]
    for col_conv in cols_to_convert_numeric:
        if col_conv in df.columns:
            df[col_conv] = pd.to_numeric(df[col_conv], errors='coerce')
        # else:
            # st.warning(f"Hinweis: Spalte '{col_conv}' für numerische Konvertierung nicht im DataFrame.")


    # Erstellung der abgeleiteten Spalten mit kurzen Namen
    if "Coop_Preis" in df.columns and "FP_Preis" in df.columns:
        # Stelle sicher, dass die Preisspalten für Berechnungen gültig sind
        # und keine Division durch Null oder Operationen auf NaNs erfolgen
        temp_df_for_calc = df.dropna(subset=["Coop_Preis", "FP_Preis"])
        if not temp_df_for_calc.empty:
            temp_df_for_calc = temp_df_for_calc[temp_df_for_calc["FP_Preis"] > 0]
        
        if not temp_df_for_calc.empty:
            # Berechne auf dem gefilterten temp_df_for_calc und weise dem originalen df zu
            # Dies handhabt Indizes korrekt, wenn Zeilen gedroppt wurden
            df["Diff_CHF"] = pd.NA
            df["Diff_%"] = pd.NA
            
            diff_chf_series = temp_df_for_calc["Coop_Preis"] - temp_df_for_calc["FP_Preis"]
            diff_pct_series = (diff_chf_series / temp_df_for_calc["FP_Preis"]) * 100
            
            df.loc[diff_chf_series.index, "Diff_CHF"] = diff_chf_series.round(2)
            df.loc[diff_pct_series.index, "Diff_%"] = diff_pct_series.round(1)
        else:
            df["Diff_CHF"] = pd.NA
            df["Diff_%"] = pd.NA
    else:
        st.warning("Spalten 'Coop_Preis' oder 'FP_Preis' fehlen. Preisdifferenzen können nicht berechnet werden.")
        df["Diff_CHF"] = pd.NA # Füge leere Spalten hinzu, damit spätere Funktionen nicht brechen
        df["Diff_%"] = pd.NA


    if "Fuzzy_Score" in df.columns:
        df["Score"] = df["Fuzzy_Score"].apply(lambda x: round(x, 1) if pd.notna(x) and x != -1 else (-1 if x == -1 else pd.NA))
    else:
        # st.warning("Spalte 'Fuzzy_Score' fehlt. 'Score' kann nicht erstellt werden.")
        df["Score"] = pd.NA # Füge leere Spalte hinzu


    # Ab hier verwenden alle Plot-Funktionen das modifizierte `df`
    # mit den Spalten "Diff_CHF", "Diff_%", "Score"

    with st.expander("1. Matching-Score & Status-Überblick", expanded=True):
        plot_matching_overview_gemini(df) # Übergib das modifizierte df

    with st.expander("2. Prozentuale Preisdifferenz – Ausreisser, Verteilung, Insights"):
        # Diese Funktion muss angepasst werden, um "Diff_%" und "Score" zu verwenden
        plot_percent_price_comparison_gemini1(df) 

    with st.expander("3. Outlier-Tabelle / Sortierbare Preisdifferenzen"):
        plot_price_outlier_table_enhanced(
            df=df, # Übergib das modifizierte df
            fuzzy_col_internal="Fuzzy_Score", # Interner Name bleibt, aber "Score" wird von der Funktion verwendet
            # Die Parameter für Preisdifferenz- und Score-Spalten in plot_price_outlier_table_enhanced
            # müssen jetzt auf "Diff_CHF", "Diff_%", "Score" angepasst werden, falls sie dort anders heißen.
            # Oder, wenn die Funktion die Spalten selbst erstellt, kann diese Logik dort bleiben.
            # Der Einfachheit halber gehen wir davon aus, dass plot_price_outlier_table_enhanced
            # jetzt die Spalten "Diff_CHF", "Diff_%" und "Score" aus dem übergebenen df erwartet.
            default_extra_columns=["Coop_Produzent", "FP_Produzent"]
        )

    with st.expander("4. Performance-Analyse gematchter Weine (Umsatz & Lieferanten)"):
        plot_matched_performance_analysis(
            df_enriched_matches=df, # Übergib das modifizierte df
            nps_col="NPS_FP",
            lieferant_col="FP_Lieferant",
            fp_name_col="FP_Name",
            coop_name_col="Coop_Name",
            preis_diff_pct_col="Diff_%" # Erwartet jetzt "Diff_%"
        )
    
    with st.expander("5. Sweet Spot & Pricing Opportunity Analyse"):
        plot_sweet_spot_analysis(
            df_enriched_matches=df, # Übergib das modifizierte df
            nps_col="NPS_FP",
            preis_diff_pct_col="Diff_%", # Erwartet jetzt "Diff_%"
            fp_name_col="FP_Name",
            coop_name_col="Coop_Name",
            fp_preis_col="FP_Preis",
            coop_preis_col="Coop_Preis",
            score_col="Score" # Erwartet jetzt "Score"
        )