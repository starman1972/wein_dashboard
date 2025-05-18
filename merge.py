# merge.py
import pandas as pd
import os

# Definiere Dateipfade (relativ zum Skript)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

MATCHING_FILE = os.path.join(DATA_DIR, "manuelle_matches_final2.xlsx")
LIEFERANTEN_FILE = os.path.join(DATA_DIR, "lieferanten.xlsx")
UMSATZ_FILE = os.path.join(DATA_DIR, "umsatzdaten.xlsx")
OUTPUT_FILE = os.path.join(DATA_DIR, "matching_enriched_debug.xlsx") # Debug Output Name

def normalize_sku(sku_series):
    """Normalisiert eine SKU-Serie: konvertiert zu String, entfernt .0, strippt Leerzeichen."""
    # Zuerst sicherstellen, dass es ein String ist und Leerzeichen entfernt werden
    s = sku_series.astype(str).str.strip()
    # Dann versuchen, ".0" am Ende zu entfernen, falls es numerisch war
    def clean_individual_sku(x):
        if pd.isna(x) or x.lower() == 'nan':
            return None
        if x.endswith(".0"):
            try:
                # Versuche, als Float zu interpretieren und dann zu Int, um .0 zu entfernen
                return str(int(float(x)))
            except ValueError:
                # Wenn es nicht als Zahl mit .0 interpretiert werden kann, gib den gestrippten String zurück
                return x
        return x
    return s.apply(clean_individual_sku)


def print_key_debug_info(df, key_col_name, df_name, is_fp_sku_from_matching=False):
    """Hilfsfunktion zur Ausgabe von Debug-Infos für Schlüsselspalten."""
    if key_col_name not in df.columns:
        print(f"DEBUG: Spalte '{key_col_name}' nicht in {df_name} gefunden.")
        return pd.Series(dtype='object')

    # Normalisierung anwenden
    keys_normalized = normalize_sku(df[key_col_name])
    
    print(f"\nDEBUG Info für '{key_col_name}' in {df_name} (normalisiert):")
    print(f"  Anzahl unique Schlüssel (nach Normalisierung): {keys_normalized.nunique()}")
    # Zeige nur nicht-None Werte als Beispiele
    unique_examples = keys_normalized.dropna().unique()
    print(f"  Beispielschlüssel (Top 5): {unique_examples[:5].tolist()}")
    if len(unique_examples) == 0 :
        print(f"  WARNUNG: Keine gültigen Schlüssel in '{key_col_name}' von {df_name} nach Normalisierung gefunden.")
    return keys_normalized


def merge_data():
    print(f"Lade Matching-Daten aus: {MATCHING_FILE}")
    try:
        # Lade alle SKU-Spalten als String, um Pandas' Typinferenz zu steuern
        dtype_spec = {'FP_Sku': str} # Spezifisch für FP_Sku
        df_matching = pd.read_excel(MATCHING_FILE, dtype=dtype_spec)
    except FileNotFoundError:
        print(f"FEHLER: Datei nicht gefunden: {MATCHING_FILE}")
        return

    # --- Lieferanten-Merge ---
    df_merged_lieferanten = df_matching.copy()
    df_merged_lieferanten['FP_Lieferant'] = pd.NA # Besser als None für Pandas

    print(f"\nLade Lieferanten-Daten aus: {LIEFERANTEN_FILE}")
    try:
        df_lieferanten = pd.read_excel(LIEFERANTEN_FILE, dtype={'Sku': str}) # SKU als String laden
        if 'Sku' not in df_lieferanten.columns:
            print(f"WARNUNG: Spalte 'Sku' nicht in {LIEFERANTEN_FILE} gefunden. Überspringe Lieferanten-Merge.")
        elif 'Lieferant' not in df_lieferanten.columns:
            print(f"WARNUNG: Spalte 'Lieferant' nicht in {LIEFERANTEN_FILE} gefunden. Überspringe Lieferanten-Merge.")
        else:
            matching_fp_sku_norm_l = print_key_debug_info(df_matching, 'FP_Sku', 'df_matching (für Lieferanten)', is_fp_sku_from_matching=True)
            lieferanten_sku_norm = print_key_debug_info(df_lieferanten, 'Sku', 'df_lieferanten')

            common_keys_lieferant = set(matching_fp_sku_norm_l.dropna()).intersection(set(lieferanten_sku_norm.dropna()))
            print(f"  Anzahl gemeinsamer SKUs für Lieferanten-Merge (nach Normalisierung): {len(common_keys_lieferant)}")
            if not common_keys_lieferant:
                print(f"  WARNUNG: Keine gemeinsamen SKUs zwischen df_matching['FP_Sku'] und df_lieferanten['Sku'] gefunden!")
            else:
                print(f"  Beispiel gemeinsamer SKUs (Top 5): {list(common_keys_lieferant)[:5]}")

            df_matching_temp_lieferant = df_matching.copy()
            df_matching_temp_lieferant['FP_Sku_join'] = normalize_sku(df_matching_temp_lieferant['FP_Sku'])
            
            df_lieferanten_temp = df_lieferanten.copy()
            df_lieferanten_temp['Sku_join'] = normalize_sku(df_lieferanten_temp['Sku'])

            print("Merge Matching-Daten mit Lieferanten-Daten...")
            df_merged_lieferanten_result = pd.merge(
                df_matching_temp_lieferant,
                df_lieferanten_temp[['Sku_join', 'Lieferant']],
                left_on='FP_Sku_join',
                right_on='Sku_join',
                how='left'
            )
            # Überschreibe die FP_Lieferant Spalte im Original df_merged_lieferanten
            # um die Struktur beizubehalten und nur die gematchten Werte zu aktualisieren
            if 'Lieferant' in df_merged_lieferanten_result.columns:
                 df_merged_lieferanten['FP_Lieferant'] = df_merged_lieferanten_result['Lieferant']

            # Aufräumen ist nicht mehr nötig, da wir mit Kopien gearbeitet haben oder direkt die Spalten gemerged haben
            # und die Zielspalte FP_Lieferant direkt befüllt wird.
            print(f"  Anzahl Zeilen nach Lieferanten-Merge: {len(df_merged_lieferanten)}")
            successful_lieferant_merges = df_merged_lieferanten['FP_Lieferant'].notna().sum()
            print(f"  Anzahl erfolgreich gemergter Lieferanten: {successful_lieferant_merges}")
            if successful_lieferant_merges == 0 and len(df_merged_lieferanten) > 0 and common_keys_lieferant:
                print(f"  HINWEIS: Gemeinsame SKUs gefunden, aber keine Lieferantenwerte zugeordnet. Möglicherweise sind 'Lieferant'-Werte in {LIEFERANTEN_FILE} für diese SKUs leer.")


    except FileNotFoundError:
        print(f"WARNUNG: Datei nicht gefunden: {LIEFERANTEN_FILE}. Überspringe Lieferanten-Merge.")
    
    df_merged_final = df_merged_lieferanten.copy()

    # --- Umsatz-Merge ---
    df_merged_final['NPS_FP'] = pd.NA # Besser als None

    print(f"\nLade Umsatz-Daten aus: {UMSATZ_FILE}")
    try:
        df_umsatz = pd.read_excel(UMSATZ_FILE, dtype={'SKU': str}) # SKU als String laden
        if 'SKU' not in df_umsatz.columns:
            print(f"WARNUNG: Spalte 'SKU' nicht in {UMSATZ_FILE} gefunden. Überspringe Umsatz-Merge.")
        elif 'net_product_sales' not in df_umsatz.columns:
            print(f"WARNUNG: Spalte 'net_product_sales' nicht in {UMSATZ_FILE} gefunden. Überspringe Umsatz-Merge.")
        else:
            matching_fp_sku_norm_u = print_key_debug_info(df_merged_final, 'FP_Sku', 'df_merged_final (für Umsatz)', is_fp_sku_from_matching=True)
            umsatz_sku_norm = print_key_debug_info(df_umsatz, 'SKU', 'df_umsatz')

            common_keys_umsatz = set(matching_fp_sku_norm_u.dropna()).intersection(set(umsatz_sku_norm.dropna()))
            print(f"  Anzahl gemeinsamer SKUs für Umsatz-Merge (nach Normalisierung): {len(common_keys_umsatz)}")
            if not common_keys_umsatz:
                print(f"  WARNUNG: Keine gemeinsamen SKUs zwischen df_merged_final['FP_Sku'] und df_umsatz['SKU'] gefunden!")
            else:
                print(f"  Beispiel gemeinsamer SKUs (Top 5): {list(common_keys_umsatz)[:5]}")

            df_merged_final_temp_umsatz = df_merged_final.copy()
            df_merged_final_temp_umsatz['FP_Sku_join'] = normalize_sku(df_merged_final_temp_umsatz['FP_Sku'])
            
            df_umsatz_temp = df_umsatz.copy()
            df_umsatz_temp['SKU_join'] = normalize_sku(df_umsatz_temp['SKU'])
            
            print("Merge mit Umsatz-Daten...")
            df_merged_final_result = pd.merge(
                df_merged_final_temp_umsatz,
                df_umsatz_temp[['SKU_join', 'net_product_sales']],
                left_on='FP_Sku_join',
                right_on='SKU_join',
                how='left'
            )

            if 'net_product_sales' in df_merged_final_result.columns:
                df_merged_final['NPS_FP'] = df_merged_final_result['net_product_sales']

            print(f"  Anzahl Zeilen nach Umsatz-Merge: {len(df_merged_final)}")
            successful_umsatz_merges = df_merged_final['NPS_FP'].notna().sum()
            print(f"  Anzahl erfolgreich gemergter Umsatzdaten: {successful_umsatz_merges}")
            if successful_umsatz_merges == 0 and len(df_merged_final) > 0 and common_keys_umsatz:
                 print(f"  HINWEIS: Gemeinsame SKUs gefunden, aber keine Umsatzwerte zugeordnet. Möglicherweise sind 'net_product_sales'-Werte in {UMSATZ_FILE} für diese SKUs leer.")

    except FileNotFoundError:
        print(f"WARNUNG: Datei nicht gefunden: {UMSATZ_FILE}. Überspringe Umsatz-Merge.")

    print("\nSpalten im finalen DataFrame:")
    print(df_merged_final.columns.tolist())

    print(f"\nSpeichere angereicherte Daten nach: {OUTPUT_FILE}")
    try:
        df_merged_final.to_excel(OUTPUT_FILE, index=False)
        print("Merge erfolgreich abgeschlossen!")
        print(f"Die Datei '{os.path.basename(OUTPUT_FILE)}' wurde im Ordner '{os.path.dirname(OUTPUT_FILE)}' gespeichert.")
    except Exception as e:
        print(f"FEHLER beim Speichern der Datei: {e}")

if __name__ == "__main__":
    merge_data()