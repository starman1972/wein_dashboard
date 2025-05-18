# app.py
import streamlit as st
import pandas as pd

# --- Tab-Module importieren ---
# Werden jetzt erst nach erfolgreicher Authentifizierung importiert, siehe unten
# from tabs import coop_sortiment, fp_sortiment, matching, gap_analyse

st.set_page_config(layout="wide")

# --- HARTCODIERTES PASSWORT ---
# BITTE ÄNDERE DIESES PASSWORT!
CORRECT_PASSWORD = "Flapo2025!"

# --- Passwort-Authentifizierungsfunktion ---
def check_password():
    """Gibt True zurück, wenn das Passwort korrekt ist, sonst False."""
    if "password_entered" not in st.session_state:
        st.session_state.password_entered = False

    if st.session_state.password_entered:
        return True

    st.title("🔒 Geschütztes Wein Dashboard")
    st.warning("Bitte geben Sie das Zugriffspasswort ein, um fortzufahren.")
    
    with st.form("password_form"):
        password = st.text_input("Passwort", type="password", key="password_input_field")
        submitted = st.form_submit_button("Zugriff")

        if submitted:
            if password == CORRECT_PASSWORD:
                st.session_state.password_entered = True
                st.rerun() 
            else:
                st.error("Das eingegebene Passwort ist nicht korrekt.")
    return False

# --- Hauptlogik der App ---
if check_password():
    # --- Konstanten für Tab-Namen ---
    TAB_COOP = "Coop-Sortiment"
    TAB_FP = "Flaschenpost-Sortiment"
    TAB_MATCHING = "Matching-Analyse"
    TAB_GAP = "Gap-Analyse"

    # --- Tab-Module importieren (JETZT erst, nach erfolgreicher Authentifizierung) ---
    from tabs import coop_sortiment, fp_sortiment, matching, gap_analyse

    # --- Daten laden ---
    @st.cache_data
    def load_coop():
        try:
            df = pd.read_excel("data/coop_weine_kombiniert.xlsx")
            return df
        except FileNotFoundError:
            st.error("FEHLER: Die Datei 'data/coop_weine_kombiniert.xlsx' wurde nicht gefunden.")
            return pd.DataFrame()
        except Exception as e:
            st.error(f"FEHLER beim Laden von 'data/coop_weine_kombiniert.xlsx': {e}")
            return pd.DataFrame()

    @st.cache_data
    def load_fp():
        try:
            df = pd.read_excel("data/flaschenpost_weine.xlsx")
            return df
        except FileNotFoundError:
            st.error("FEHLER: Die Datei 'data/flaschenpost_weine.xlsx' wurde nicht gefunden.")
            return pd.DataFrame()
        except Exception as e:
            st.error(f"FEHLER beim Laden von 'data/flaschenpost_weine.xlsx': {e}")
            return pd.DataFrame()

    @st.cache_data
    def load_matching():
        try:
            df = pd.read_excel("data/manuelle_matches_final2.xlsx")
            return df
        except FileNotFoundError:
            st.error("FEHLER: Die Datei 'data/manuelle_matches_final2.xlsx' wurde nicht gefunden.")
            return pd.DataFrame()
        except Exception as e:
            st.error(f"FEHLER beim Laden von 'data/manuelle_matches_final2.xlsx': {e}")
            return pd.DataFrame()

    # --- Datenbasis laden ---
    coop_df = load_coop()
    fp_df = load_fp() # Wird jetzt im GAP-Tab benötigt
    matching_df = load_matching()

    # --- Navigation ---
    st.sidebar.success("Zugriff gewährt!")
    options_list = [
        TAB_COOP,
        TAB_FP,
        TAB_MATCHING,
        TAB_GAP
    ]
    tab = st.sidebar.radio(
        "Analyse-Bereich wählen",
        options=options_list,
    )

    # --- Tabs anzeigen ---
    if tab == TAB_COOP:
        if coop_df is not None and not coop_df.empty:
            try:
                coop_sortiment.show_coop_sortiment_tab(coop_df)
            except Exception as e:
                st.error(f"Fehler im {TAB_COOP} Tab: {e}")
                import traceback
                st.error(traceback.format_exc())
        else:
            st.warning(f"Keine Daten für {TAB_COOP} verfügbar oder Daten konnten nicht geladen werden.")

    elif tab == TAB_FP:
        if fp_df is not None and not fp_df.empty:
            try:
                fp_sortiment.show_fp_sortiment_tab(fp_df)
            except Exception as e:
                st.error(f"Fehler im {TAB_FP} Tab: {e}")
                import traceback
                st.error(traceback.format_exc())
        else:
            st.warning(f"Keine Daten für {TAB_FP} verfügbar oder Daten konnten nicht geladen werden.")

    elif tab == TAB_MATCHING:
        if matching_df is not None and not matching_df.empty:
            try:
                matching.show_matching_tab(matching_df) 
            except Exception as e:
                st.error(f"Fehler im {TAB_MATCHING} Tab: {e}")
                import traceback
                st.error(traceback.format_exc())
        else:
            st.warning(f"Keine Daten für {TAB_MATCHING} verfügbar oder Daten konnten nicht geladen werden.")

    elif tab == TAB_GAP:
        if coop_df is not None and not coop_df.empty and \
           matching_df is not None and not matching_df.empty and \
           fp_df is not None and not fp_df.empty:
            try:
                gap_analyse.show_gap_analysis_tab(coop_df, matching_df, fp_df)
            except Exception as e:
                st.error(f"Fehler im {TAB_GAP} Tab: {e}")
                import traceback
                st.error(traceback.format_exc())
        else:
            st.warning(f"Unzureichende Daten für {TAB_GAP} verfügbar. Coop-, Matching- und Flaschenpost-Daten werden benötigt.")
    else:
        st.error("Unbekannter Tab ausgewählt. Bitte kontaktieren Sie den Support.")

    st.sidebar.info(
        "Wein-Dashboard für Sortimentsanalysen. "
        "Entwickelt zur Unterstützung interner Entscheidungen."
    )
# Ende von if check_password():