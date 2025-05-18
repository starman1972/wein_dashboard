# Wein Dashboard

**Struktur:**
- app.py: Einstieg; Routing, Filter, Tabaufrufe
- data_loading.py: Import der Quelldaten
- plot_utils.py: Plotlogik
- filters.py: Filter- und Helperfunktionen für globale/Seiten-Filter
- tabs/: Einzelne Analyse-Tabs/modules
- data/: Alle Daten-Excel

**Starten:**
1. installiere requirements.txt
2. Starte mit `streamlit run app.py`
3. Excel-Files in /data müssen exakt wie spezifiziert vorhanden sein

**Neue Analysen?**
- Als Funktions-Modul in plot_utils.py und Aufruf/Integration im passenden tabs/<xyz>.py

**Wartung/Änderung?**
- Sämtliche Spalten-/Dateinamen an einer Stelle in data_loading.py oder den jeweiligen tab.py-Files anpassen.