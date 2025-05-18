import pandas as pd

def load_all_data():
    # Lies alle Excel-Files ein, prüfe auf relevante Spalten, korrigiere ggf. Typen/Codes!
    data = {}
    data['coop'] = pd.read_excel("data/coop_weine_kombiniert.xlsx")
    data['fp'] = pd.read_excel("data/flaschenpost_weine.xlsx")
    data['lieferanten'] = pd.read_excel("data/lieferanten.xlsx")
    data['matching'] = pd.read_excel("data/manuelle_matches_final2.xlsx")
    try:
        data['umsatz'] = pd.read_excel("data/umsatzdaten.xlsx")
    except:
        data['umsatz'] = pd.DataFrame()
    return data