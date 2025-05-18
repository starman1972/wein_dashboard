# tabs/gap_analyse.py
import streamlit as st
from plot_utils import (
    plot_gap_analysis_table,
    plot_gaps_weintyp_comparison,
    plot_gaps_preisklassen_comparison,
    plot_gaps_preis_nach_weintyp_comparison,
    plot_gaps_herkunftslaender_comparison,
    plot_gaps_frankreich_regionen_comparison,
    plot_gaps_italien_regionen_comparison,
    plot_gaps_schweiz_regionen_comparison,
    plot_gaps_spanien_regionen_comparison,
    plot_gaps_produzenten_comparison, 
    plot_top_produzenten_in_gaps,
    plot_coop_produzenten_nicht_in_fp
)
import pandas as pd
import re 
import unicodedata 

def show_gap_analysis_tab(df_coop_original: pd.DataFrame, df_matching_enriched: pd.DataFrame, df_fp_weine: pd.DataFrame):
    st.header("GAP-Analyse: Coop-Sortiment vs. Flaschenpost")

    with st.expander("Übersicht und Detailtabelle der Sortimentslücken (Coop-Weine nicht bei FP)", expanded=True):
        st.markdown("""
        Diese Tabelle identifiziert Weine aus dem Coop-Sortiment, für die kein passendes Gegenstück 
        im Flaschenpost-Sortiment gefunden wurde (basierend auf dem `Match_Status` 'Kein Match' 
        in der Datei `manuelle_matches_final2.xlsx`).
        """)
        columns_to_display_in_gap_table = ["Name", "Produzent", "Preis", "Weintyp", "Region", "URL"]
        status_value_indicating_no_match = "Kein Match"
        df_gaps_result = pd.DataFrame() 
        try:
            df_gaps_result = plot_gap_analysis_table(
                df_coop_full=df_coop_original, df_matching=df_matching_enriched,
                coop_id_col_in_coop_df="URL", coop_id_col_in_matching_df="Coop_URL",
                match_status_col_in_matching_df="Match_Status", non_match_status_value=status_value_indicating_no_match,
                gap_display_columns=columns_to_display_in_gap_table
            )
        except Exception as e: 
            st.error(f"Fehler bei Erstellung der GAP-Analyse Tabelle: {e}")
            # import traceback # Für Details
            # st.error(traceback.format_exc())


    # --- Analysen der Gaps (Expander 1-11) ---
    if df_gaps_result is not None and not df_gaps_result.empty:
        with st.expander("1. Vergleich: Weintyp-Verteilung (Lücken vs. Coop-Gesamt)", expanded=True):
            try: plot_gaps_weintyp_comparison(df_gaps=df_gaps_result, df_coop_original=df_coop_original, weintyp_col="Weintyp")
            except Exception as e: st.error(f"Fehler bei Weintyp-Vergleichsanalyse der Gaps: {e}")
        
        with st.expander("2. Vergleich: Preisklassen-Verteilung (Lücken vs. Coop-Gesamt)", expanded=False):
            try:
                max_preis_gaps = df_gaps_result["Preis"].max() if not df_gaps_result.empty and "Preis" in df_gaps_result else 200
                max_preis_coop = df_coop_original["Preis"].max() if not df_coop_original.empty and "Preis" in df_coop_original else 200
                overall_max_preis = max(max_preis_gaps, max_preis_coop, 101.0)
                bins_definition = [0, 20, 50, 100, overall_max_preis]
                labels_definition = ["0–20 CHF", "20–50 CHF", "50–100 CHF"]
                if overall_max_preis <= 100: 
                    labels_definition = labels_definition[:3] # Nur bis 50-100 CHF
                    bins_definition = bins_definition[:4]     # Entsprechend die Bins kürzen
                else: 
                    labels_definition.append(f"100–{int(round(overall_max_preis))} CHF")
                plot_gaps_preisklassen_comparison(df_gaps=df_gaps_result, df_coop_original=df_coop_original, preis_col="Preis", bins=bins_definition, labels=labels_definition)
            except Exception as e: st.error(f"Fehler bei Preisklassen-Vergleichsanalyse der Gaps: {e}")

        with st.expander("3. Vergleich: Preisverteilung nach Weintyp (Lücken vs. Coop-Gesamt)", expanded=False):
            try:
                max_preis_gaps = df_gaps_result["Preis"].max() if not df_gaps_result.empty and "Preis" in df_gaps_result else 200
                max_preis_coop = df_coop_original["Preis"].max() if not df_coop_original.empty and "Preis" in df_coop_original else 200
                overall_max_preis = max(max_preis_gaps, max_preis_coop, 101.0)
                bins_definition = [0, 20, 50, 100, overall_max_preis]
                labels_definition = ["0–20 CHF", "20–50 CHF", "50–100 CHF"]
                if overall_max_preis <= 100: 
                    if len(labels_definition) > 3 : labels_definition = labels_definition[:3]
                    if len(bins_definition) > 4: bins_definition = bins_definition[:4]
                else: 
                    labels_definition.append(f"100–{int(round(overall_max_preis))} CHF")
                plot_gaps_preis_nach_weintyp_comparison(df_gaps=df_gaps_result, df_coop_original=df_coop_original, preis_col="Preis", weintyp_col="Weintyp", bins=bins_definition, labels=labels_definition)
            except Exception as e: st.error(f"Fehler bei Preisverteilung nach Weintyp (Gaps Vergleich): {e}")

        with st.expander("4. Vergleich: Top Herkunftsländer (Lücken vs. Coop-Gesamt)", expanded=False):
            try: plot_gaps_herkunftslaender_comparison(df_gaps=df_gaps_result, df_coop_original=df_coop_original, region_col_coop="Region", top_n=10)
            except Exception as e: st.error(f"Fehler bei Herkunftsländer-Vergleichsanalyse der Gaps: {e}")

        with st.expander("5. Vergleich: Regionen Frankreichs (Lücken vs. Coop-Gesamt)", expanded=False):
            try: plot_gaps_frankreich_regionen_comparison(df_gaps=df_gaps_result, df_coop_original=df_coop_original, region_col="Region")
            except Exception as e: st.error(f"Fehler bei Frankreich-Regionen-Vergleichsanalyse der Gaps: {e}")

        with st.expander("6. Vergleich: Regionen Italiens (Lücken vs. Coop-Gesamt)", expanded=False):
            try: plot_gaps_italien_regionen_comparison(df_gaps=df_gaps_result, df_coop_original=df_coop_original, region_col="Region")
            except Exception as e: st.error(f"Fehler bei Italien-Regionen-Vergleichsanalyse der Gaps: {e}")

        with st.expander("7. Vergleich: Regionen der Schweiz (Lücken vs. Coop-Gesamt)", expanded=False):
            try: plot_gaps_schweiz_regionen_comparison(df_gaps=df_gaps_result, df_coop_original=df_coop_original, region_col="Region")
            except Exception as e: st.error(f"Fehler bei Schweiz-Regionen-Vergleichsanalyse der Gaps: {e}")

        with st.expander("8. Vergleich: Regionen Spaniens (Lücken vs. Coop-Gesamt)", expanded=False):
            try: plot_gaps_spanien_regionen_comparison(df_gaps=df_gaps_result, df_coop_original=df_coop_original, region_col="Region")
            except Exception as e: st.error(f"Fehler bei Spanien-Regionen-Vergleichsanalyse der Gaps: {e}")
        
        # Expander 9 (relative Produzentenanalyse)
        with st.expander("9. Vergleich: Top Coop-Produzenten (Lücken vs. Coop-Gesamt)", expanded=False):
            try:
                plot_gaps_produzenten_comparison(
                    df_matching_all_coop=df_matching_enriched, coop_produzent_col="Coop_Produzent",
                    match_status_col="Match_Status", non_match_status_value="Kein Match", top_n=15) # top_n=30 war in plot_utils, hier 15 für Konsistenz
            except Exception as e: st.error(f"Fehler bei relativer Produzenten-Analyse der Gaps: {e}")

        # Expander 10 (absolute Produzentenanalyse der Gaps)
        with st.expander("10. Top Coop-Produzenten in den Sortimentslücken (absolute Anzahl)", expanded=False):
            try:
                plot_top_produzenten_in_gaps(
                    df_matching_all_coop=df_matching_enriched, coop_produzent_col="Coop_Produzent",
                    match_status_col="Match_Status", non_match_status_value="Kein Match", top_n=30)
            except Exception as e: st.error(f"Fehler bei Top-Produzenten-Analyse der Gaps (absolut): {e}")
        
        with st.expander("11. Coop-Produzenten von Lücken, die NICHT bei Flaschenpost gelistet sind", expanded=False):
            try:
                plot_coop_produzenten_nicht_in_fp(
                    df_matching_all_coop=df_matching_enriched, df_fp_original=df_fp_weine,
                    coop_produzent_col_matching="Coop_Produzent", fp_produzent_col_original="Produzent",
                    match_status_col="Match_Status", non_match_status_value="Kein Match", top_n=30)
            except Exception as e: st.error(f"Fehler bei Analyse 'Coop-Produzenten nicht bei FP': {e}")
    
    # Dieser Block wird ausgeführt, wenn es KEINE Gaps gibt ODER wenn df_gaps_result None ist (z.B. Fehler oben)
    # Der Syntaxfehler war wahrscheinlich hier, weil der elif-Block nicht korrekt auf den if-Block folgte.
    elif df_gaps_result is not None and df_gaps_result.empty:
        st.info("Keine Sortimentslücken identifiziert, daher können keine Detailanalysen der Lücken angezeigt werden.")
    # Kein expliziter else-Block für df_gaps_result is None nötig, da Fehler schon oben behandelt werden sollten.

    # --- FAZIT / ZUSAMMENFASSUNG ---
    # Dieser Block sollte NACH der if/elif Struktur für df_gaps_result stehen.
    st.markdown("---")
    st.header("Zusammenfassende Einordnung der GAP-Analyse")

    # Stelle sicher, dass df_gaps_result hier definitiv initialisiert ist (sollte es sein)
    # aber eine zusätzliche Prüfung schadet nicht, um Fehler im Fazittext zu vermeiden.
    if 'df_gaps_result' in locals() and df_gaps_result is not None:
        num_gaps_value = len(df_gaps_result)
    else:
        # Fallback, falls df_gaps_result aus irgendeinem Grund nicht definiert oder None ist
        # Dies könnte passieren, wenn plot_gap_analysis_table frühzeitig abbricht und kein DF zurückgibt
        # (obwohl es das jetzt tun sollte).
        st.warning("Basisdaten für die Anzahl der Lücken konnten nicht ermittelt werden für das Fazit.")
        num_gaps_value = "[Anzahl nicht verfügbar]"


    fazit_text = f"""
    Diese umfassende GAP-Analyse hat die Weine beleuchtet, die im Coop-Online-Sortiment geführt werden, 
    jedoch aktuell kein direktes Äquivalent im Flaschenpost-Sortiment haben (basierend auf dem aktuellen Matching).
    Insgesamt wurden **{num_gaps_value} solcher Sortimentslücken** identifiziert.

    **Kernaussagen aus den Strukturanalysen:**
    Die Vergleiche der Lücken mit dem Coop-Gesamtsortiment (nach Weintyp, Preisklasse, Herkunft, etc.) zeigen mehrheitlich,
    dass die *Struktur* dieser Lücken der allgemeinen Zusammensetzung des Coop-Sortiments ähnelt. 
    Dies deutet darauf hin, dass die Lücken sich breit über verschiedene Kategorien verteilen, 
    anstatt dass Flaschenpost ganze Hauptsegmente, die Coop stark besetzt, systematisch fehlen. 
    Starke prozentuale Abweichungen in der Struktur der Lücken waren selten, was auf eine granulare Natur vieler dieser Lücken hindeutet.

    **Strategischer Nutzen für Flaschenpost:**
    Der primäre Wert dieser Analyse liegt weniger in den aufgedeckten strukturellen Unterschieden als vielmehr in den **spezifischen, qualitativen Erkenntnismöglichkeiten**:

    1.  **Die Detailtabelle der {num_gaps_value} Lücken:**
        *   Diese Tabelle ist das zentrale Werkzeug, um gezielt nach **spezifischen Weinen, Marken oder Attributen** zu suchen, die für Flaschenpost strategisch relevant sein könnten. 
        *   Nutzen Sie die Filterfunktionen, um beispielsweise Lücken in hochpreisigen Segmenten, Nischenregionen oder von bestimmten Produzenten zu identifizieren. Hier könnten sich gezielte Ergänzungspotenziale für das Flaschenpost-Sortiment verbergen.

    2.  **Potenzielle neue Produzentenbeziehungen:**
        *   Die Analyse der "Coop-Produzenten von Lücken, die NICHT bei Flaschenpost gelistet sind" (siehe entsprechender Analysebereich oben) liefert konkrete Hinweise auf Marken, die das Flaschenpost-Angebot möglicherweise einzigartig ergänzen könnten und zu denen eventuell noch keine Lieferantenbeziehung besteht.

    **Wichtiger Kontext – Unterschiedliche Sortimentsgrößen:**
    Es ist entscheidend zu berücksichtigen, dass Flaschenpost mit über 24.000 SKUs ein Vielfaches des Coop-Sortiments (ca. 3.500 SKUs) anbietet. 
    Diese GAP-Analyse fokussiert darauf, *welche spezifischen Akzente Coop setzt*, die bei Flaschenpost aktuell fehlen. 
    Die identifizierten Lücken sind somit primär als **Impulsgeber für gezielte strategische Überlegungen** zu verstehen und nicht als Indikator für eine generelle Unterversorgung.

    **Empfohlene nächste Schritte für den Nutzer:**
    *   **Explorative Analyse der Detailtabelle:** Identifizieren Sie konkrete Weine oder Weingruppen innerhalb der Lücken, die einer genaueren Prüfung wert sind.
    *   **Bewertung der "Nur-Coop"-Produzenten:** Prüfen Sie die Relevanz der im entsprechenden Analysebereich gelisteten Produzenten für das Flaschenpost-Portfolio.
    *   **Integration der Erkenntnisse:** Nutzen Sie die gewonnenen Einblicke für interne Sortimentsdiskussionen und zur weiteren Schärfung der Marktpositionierung.
    """
    st.markdown(fazit_text)