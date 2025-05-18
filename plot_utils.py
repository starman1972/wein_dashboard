import streamlit as st
import pandas as pd
import plotly.express as px

def plot_weintypen_pie_and_table(
    df: pd.DataFrame,
    weintyp_col: str = "Weintyp",
    titel: str = "Verteilung der Weintypen im Sortiment",
    chart_height: int = 500
):
    """
    Zeigt Pie-Chart (Kreisdiagramm) und Weintypen-Tabelle nebeneinander an,
    mit CI-konformen Farben, richtiger Reihenfolge, Prozentangaben, Download-Option und Totalsumme.
    Spezieller Hinweis: "Nur 75 cl Flaschen berücksichtigt".
    """
    # Reihenfolge und Farben einmalig vorgeben
    order = ["Rotwein", "Weisswein", "Roséwein", "Schaumwein"]
    farben = {
        "Rotwein": "#8B0000",
        "Weisswein": "#FADA5E",
        "Roséwein": "#F6ADC6",
        "Schaumwein": "#E6E6FA"
    }
    # Value Counts sortieren wie oben
    weintyp_anteile = df[weintyp_col].value_counts().reindex(order, fill_value=0)
    gesamt = weintyp_anteile.sum()
    percent = (weintyp_anteile / gesamt * 100).round(1)
    
    st.subheader(titel)
    st.info("Hinweis: Nur 75 cl Flaschen berücksichtigt.")

    col1, col2 = st.columns([1.4, 1])

    with col1:
        fig = px.pie(
            names=weintyp_anteile.index,
            values=weintyp_anteile.values,
            hole=0.3,
            color=weintyp_anteile.index,
            color_discrete_map=farben
        )
        fig.update_traces(textfont_size=16)
        fig.update_layout(
            height=chart_height,
            margin=dict(t=35, l=0, r=0, b=0),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.18,
                xanchor="center",
                x=0.5,
                font=dict(size=15)
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Tabelle aufbauen inkl. Total als letzte Zeile
        table_df = pd.DataFrame({
            "Weintyp": weintyp_anteile.index,
            "Anzahl": weintyp_anteile.values,
            "Anteil %": percent.values
        })
        # Totalsumme hinzufügen
        total_row = pd.DataFrame({
            "Weintyp": ["Total"],
            "Anzahl": [gesamt],
            "Anteil %": [percent.sum().round(1)]
        })
        table_df = pd.concat([table_df, total_row], ignore_index=True)

        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )
        # Download-Button für Tabelle
        st.download_button(
            label="Tabelle als CSV herunterladen",
            data=table_df.to_csv(index=False).encode("utf-8"),
            file_name=f"weintypen_{pd.Timestamp.now().date()}.csv",
            mime="text/csv"
        )

    st.caption(f"Total: {gesamt} Weine | Stand: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")

import streamlit as st
import pandas as pd
import plotly.express as px

def plot_preisklassen_pie_and_table(
    df: pd.DataFrame,
    preis_col: str = "Preis",
    bins = [0, 20, 50, 100, 9999],
    labels = ["0–20 CHF", "20–50 CHF", "50–100 CHF", "100+ CHF"],
    titel: str = "Verteilung der Preisklassen im Sortiment",
    chart_height: int = 500
):
    """
    Zeigt Piechart und Tabelle der Preisklassen-Verteilung nebeneinander, 
    mit kontrastreichen Farben, Totalsumme und Download-Möglichkeit.
    Farben: Dunkles Blau → kräftiges Blau → Petrol → Dunkelgrau.
    """
    # Preisklasse bauen
    df = df.copy()
    df["Preisklasse"] = pd.cut(df[preis_col], bins=bins, labels=labels, include_lowest=True)

    preisklassen_anzahl = df["Preisklasse"].value_counts().reindex(labels, fill_value=0)
    total_weine = preisklassen_anzahl.sum()
    prozent = (preisklassen_anzahl / total_weine * 100).round(1)

    # Farbpalette: Kräftig, kein hellblau!
    farben = ["#104E8B", "#1874CD", "#42A5A2", "#252525"]  # dunkelblau – mittelblau – petrol – dunkelgrau 

    st.subheader(titel)
    col1, col2 = st.columns([1.3, 1])

    with col1:
        fig = px.pie(
            names=preisklassen_anzahl.index,
            values=preisklassen_anzahl.values,
            hole=0.35,
            color=preisklassen_anzahl.index,
            color_discrete_sequence=farben
        )
        fig.update_traces(textfont_size=16)
        fig.update_layout(
            height=chart_height,
            margin=dict(t=30, l=0, r=0, b=0),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.18,
                xanchor="center",
                x=0.52,
                font=dict(size=15)
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Tabelle inkl. Prozent und Total
        table_df = pd.DataFrame({
            "Preisklasse": preisklassen_anzahl.index,
            "Anzahl": preisklassen_anzahl.values,
            "Anteil %": prozent.values
        })
        # Totalsumme rein
        total_row = pd.DataFrame({
            "Preisklasse": ["Total"],
            "Anzahl": [total_weine],
            "Anteil %": [prozent.sum().round(1)]
        })
        table_df = pd.concat([table_df, total_row], ignore_index=True)
        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )
        st.download_button(
            label="Tabelle als CSV herunterladen",
            data=table_df.to_csv(index=False).encode("utf-8"),
            file_name=f"preisklassen_{pd.Timestamp.now().date()}.csv",
            mime="text/csv"
        )
    st.caption(f"Total: {total_weine} Weine | Stand: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def plot_preisverteilung_nach_weintyp(
    df: pd.DataFrame,
    preis_col: str = "Preis",
    weintyp_col: str = "Weintyp",
    bins = [0, 20, 50, 100, 9999],
    labels = ["0–20 CHF", "20–50 CHF", "50–100 CHF", "100+ CHF"],
    titel: str = "Preisverteilung nach Weintyp im Sortiment",
    chart_height: int = 500,
):
    """
    Zeigt gestapeltes Balkendiagramm (Preisklasse x Weintyp, absolute & Prozentzahlen) + Tabelle mit Total und Download.
    Farben identisch zum Pie-Chart der Weintypen.
    """

    # CI-konforme Farben und Reihenfolge beachten!
    order = ["Rotwein", "Weisswein", "Roséwein", "Schaumwein"]
    farben = {
        "Rotwein": "#8B0000",
        "Weisswein": "#FADA5E",
        "Roséwein": "#F6ADC6",
        "Schaumwein": "#E6E6FA",
    }

    # Preisklassen-Kategorie anlegen
    df = df.copy()
    df["Preisklasse"] = pd.cut(df[preis_col], bins=bins, labels=labels, include_lowest=True)
    # Pivot: Preisklasse (Index) x Weintyp (Columns), Reihenfolge wie im Pie!
    pivot_table = df.pivot_table(index="Preisklasse", columns=weintyp_col, aggfunc="size", fill_value=0)
    for typ in order:
        if typ not in pivot_table.columns:
            pivot_table[typ] = 0  # Fehlende Sparten auf 0 (für spätere Sortierung)
    pivot_table = pivot_table[order].reindex(labels, fill_value=0)

    st.subheader(titel)
    st.caption("Nur 75 cl Flaschen berücksichtigt.")

    col1, col2 = st.columns([1.5, 1])

    with col1:
        totals = pivot_table.sum(axis=1)
        fig = go.Figure()
        for i, weintyp in enumerate(order):
            y = pivot_table[weintyp]
            proz = [v/tot*100 if tot > 0 else 0 for v, tot in zip(y.values, totals.values)]
            customtxt = [f"{int(v)}<br>({p:.1f}%)" if v > 0 else "" for v, p in zip(y.values, proz)]
            fig.add_bar(
                x=pivot_table.index,
                y=y.values,
                name=weintyp,
                marker_color=farben[weintyp],
                text=customtxt,
                textposition="auto",
                hovertemplate=f'{weintyp}: %{{y}}<br>%{{text}}<extra></extra>'
            )
        fig.update_layout(
            barmode="stack",
            height=chart_height,
            xaxis_title="Preisklasse",
            yaxis_title="Anzahl Weine",
            plot_bgcolor="#ffffff",    # Reinweiß, wie Hintergrund"
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.0,
                xanchor="center",
                x=0.5,
                font=dict(size=15)
            ),
            margin=dict(t=30, l=0, r=0, b=0),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Tabelle: alle Zellwerte als "n (x.x%)"
        table_rows = []
        gesamt_total = 0
        for preisklasse in pivot_table.index:
            row = [preisklasse]
            total = pivot_table.loc[preisklasse].sum()
            gesamt_total += total
            for weintyp in order:
                anz = pivot_table.loc[preisklasse, weintyp]
                proz = (anz / total * 100) if total > 0 else 0
                row.append(f"{int(anz)} ({proz:.1f}%)")
            row.append(total)
            table_rows.append(row)
        # Totalsummen-Reihe:
        sum_row = ["Total"]
        tổng = pivot_table.sum()
        total_sum = tổng.sum()
        for weintyp in order:
            wert = tổng[weintyp]
            proz = wert / total_sum * 100 if total_sum else 0
            sum_row.append(f"{int(wert)} ({proz:.1f}%)")
        sum_row.append(total_sum)
        table_rows.append(sum_row)
        col_names = ["Preisklasse"] + order + ["Total"]
        table_df = pd.DataFrame(table_rows, columns=col_names)

        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )
        st.download_button(
            label="Tabelle als CSV herunterladen",
            data=table_df.to_csv(index=False).encode("utf-8"),
            file_name=f"preisverteilung_weintyp_{pd.Timestamp.now().date()}.csv",
            mime="text/csv"
        )
    st.caption(f"Total: {total_sum} Weine | Stand: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")


import streamlit as st
import pandas as pd
import plotly.express as px

def plot_top_herkunftslaender(
    df: pd.DataFrame,
    region_col: str = "Region",
    titel: str = "Top-10 Herkunftsländer im Sortiment",
    chart_height: int = 450
):
    """
    Zeigt die Top-10 Herkunftsländer als Balkendiagramm und Tabelle nebeneinander.
    Kräftige Farben, Totalzeile, Download. Regionenspaltung wie im Originalscript.
    """
    # Land aus "Region" extrahieren (wie im Script)
    df = df.copy()
    df["Land"] = df[region_col].apply(lambda x: str(x).split(",")[0].strip() if "," in str(x) else str(x))
    top_laender = df["Land"].value_counts().head(10)
    total_weine = top_laender.sum()
    prozent = (top_laender / total_weine * 100).round(1)

    st.subheader(titel)
    col1, col2 = st.columns([1.5, 1])

    with col1:
        # Kräftiges Blaugrau für Business-Look, kein Hellblau
        bar_color = "#2B4C7E"
        fig = px.bar(
            x=top_laender.index,
            y=top_laender.values,
            text=top_laender.values,
            color_discrete_sequence=[bar_color]
        )
        fig.update_traces(textposition="outside", textfont_size=14)
        fig.update_layout(
            height=chart_height,
            plot_bgcolor="#ffffff",  # konsistent weiß
            paper_bgcolor="#ffffff",
            xaxis_title="Land",
            yaxis_title="Anzahl Weine",
            xaxis_tickangle=-45,
            margin=dict(t=35, r=15, l=5, b=60)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        table_df = pd.DataFrame({
            "Land": top_laender.index,
            "Anzahl": top_laender.values,
            "Anteil %": prozent.values
        })
        # Totalsumme hinzufügen
        total_row = pd.DataFrame({
            "Land": ["Total"],
            "Anzahl": [total_weine],
            "Anteil %": [prozent.sum().round(1)]
        })
        table_df = pd.concat([table_df, total_row], ignore_index=True)

        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )
        st.download_button(
            label="Tabelle als CSV herunterladen",
            data=table_df.to_csv(index=False).encode("utf-8"),
            file_name=f"top10_laender_{pd.Timestamp.now().date()}.csv",
            mime="text/csv"
        )
    st.caption(f"Top 10 machen {100*total_weine/df.shape[0]:.1f}% des Sortiments aus | Stand: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")


import streamlit as st
import pandas as pd
import plotly.express as px
import unicodedata

def plot_frankreich_regionen(
    df: pd.DataFrame,
    region_col: str = "Region",
    titel: str = "Weinregionen Frankreichs im Sortiment",
    chart_height: int = 450
):
    """
    Zeigt die Regionen Frankreichs als Balkendiagramm und Tabelle nebeneinander (inkl. Normalisierung und Mapping).
    Farblich consistent, Totalreihe, Downloadbutton.
    """
    # Subregionen-Logik (wie in deinem Skript)
    def normalize_string(text):
        text = str(text).lower()
        text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
        text = text.replace('–', '-').replace(' ', '-')
        return text

    subregion_mapping = {
        # Burgund
        "maconnais": "Burgund",
        "chablis": "Burgund",
        "beaujolais": "Burgund",
        "cote-de-beaune": "Burgund",
        "cote-de-nuits": "Burgund",
        "cote-chalon": "Burgund",
        "coteaux-du-lyonnais": "Burgund",
        "bouzeron": "Burgund",
        "givry": "Burgund",
        "mercurey": "Burgund",
        "montagny": "Burgund",
        "rully": "Burgund",
        "cote-d-or": "Burgund",
        "irancy": "Burgund",
        "pouilly-fuisse": "Burgund",
        "saint-veran": "Burgund",
        "vire-clesse": "Burgund",
        "saint-bris": "Burgund",
        # Bordeaux
        "fronsac": "Bordeaux",
        "saint-emilion": "Bordeaux",
        "pomerol": "Bordeaux",
        "margaux": "Bordeaux",
        "pauillac": "Bordeaux",
        "saint-julien": "Bordeaux",
        "saint-estephe": "Bordeaux",
        "graves": "Bordeaux",
        "medoc": "Bordeaux",
        "castillon": "Bordeaux",
        "listrac": "Bordeaux",
        "moulis": "Bordeaux",
        "entre-deux-mers": "Bordeaux",
        "sauternes": "Bordeaux",
        "barsac": "Bordeaux",
        "canon-fronsac": "Bordeaux",
        # Rhône
        "hermitage": "Rhône",
        "chateauneuf-du-pape": "Rhône",
        "cornas": "Rhône",
        "saint-joseph": "Rhône",
        "gigondas": "Rhône",
        "cote-rotie": "Rhône",
        "vacqueyras": "Rhône",
        "crozes-hermitage": "Rhône",
        "rasteau": "Rhône",
        "lirac": "Rhône",
        "condrieu": "Rhône",
        "luberon": "Rhône",
        "cote-du-luberon": "Rhône",
        # Andere
        "keine-subregion": "Andere",
        "ubrige-regionen-eu": "Andere"
    }

    def categorize_region(subregion_normalized):
        if "burgund" in subregion_normalized:
            return "Burgund"
        elif "bordeaux" in subregion_normalized:
            return "Bordeaux"
        elif "rhone" in subregion_normalized:
            return "Rhône"
        return subregion_mapping.get(subregion_normalized, subregion_normalized.capitalize())

    df = df.copy()
    # Land aus Region
    df["Land"] = df[region_col].apply(lambda x: str(x).split(",")[0].strip() if "," in str(x) else str(x))
    # Subregion
    df["Subregion"] = df[region_col].apply(lambda x: str(x).split(",")[1].strip() if "," in str(x) else "Keine Subregion")
    # Nur Frankreich
    df_fr = df[df["Land"] == "Frankreich"].copy()
    df_fr["Subregion_normalized"] = df_fr["Subregion"].apply(normalize_string)
    df_fr["Region_plot"] = df_fr["Subregion_normalized"].apply(categorize_region)
    regionen_fr = df_fr["Region_plot"].value_counts()
    total_weine = regionen_fr.sum()
    prozent = (regionen_fr / total_weine * 100).round(1)

    st.subheader(titel)
    st.caption("Nur 75 cl Flaschen berücksichtigt.")

    col1, col2 = st.columns([1.5, 1])

    with col1:
        bar_color = "#2B4C7E"  # CI-blau wie überall sonst
        fig = px.bar(
            x=regionen_fr.index,
            y=regionen_fr.values,
            text=regionen_fr.values,
            color_discrete_sequence=[bar_color]
        )
        fig.update_traces(textposition="outside", textfont_size=13)
        fig.update_layout(
            height=chart_height,
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            xaxis_title="Region",
            yaxis_title="Anzahl Weine",
            xaxis_tickangle=-35,
            margin=dict(t=35, r=15, l=5, b=60)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        table_df = pd.DataFrame({
            "Region": regionen_fr.index,
            "Anzahl": regionen_fr.values,
            "Anteil %": prozent.values
        })
        total_row = pd.DataFrame({
            "Region": ["Total"],
            "Anzahl": [total_weine],
            "Anteil %": [prozent.sum().round(1)]
        })
        table_df = pd.concat([table_df, total_row], ignore_index=True)

        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )
        st.download_button(
            label="Tabelle als CSV herunterladen",
            data=table_df.to_csv(index=False).encode("utf-8"),
            file_name=f"frankreich_regionen_{pd.Timestamp.now().date()}.csv",
            mime="text/csv"
        )
    st.caption(f"Total: {total_weine} Frankreich-Weine | Stand: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")


import streamlit as st
import pandas as pd
import plotly.express as px
import unicodedata

def plot_italien_regionen(
    df: pd.DataFrame,
    region_col: str = "Region",
    titel: str = "Weinregionen Italiens im Sortiment",
    chart_height: int = 450
):
    """
    Zeigt die Regionen Italiens als Balkendiagramm und Tabelle nebeneinander.
    Mapping/Normalisierung sowie Tabellendarstellung und Download im gewohnten Stil.
    """
    # Subregionen-Logik
    def normalize_string(text):
        text = str(text).lower()
        text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
        text = text.replace('–', '-').replace(' ', '-')
        return text

    subregion_mapping = {
        "lombardei/veltlin": "Lombardei",
        "keine-subregion": "Andere",
        "ubrige-regionen-eu": "Andere",
        "brda": "Andere",
        "abruzzen-und-apulien": "Andere"
    }

    def categorize_region(subregion_normalized):
        if subregion_normalized in subregion_mapping:
            return subregion_mapping[subregion_normalized]
        return subregion_normalized.capitalize()

    df = df.copy()
    # Land extrahieren (wie bei Frankreich)
    df["Land"] = df[region_col].apply(lambda x: str(x).split(",")[0].strip() if "," in str(x) else str(x))
    df["Subregion"] = df[region_col].apply(lambda x: str(x).split(",")[1].strip() if "," in str(x) else "Keine Subregion")
    # Nur Italien
    df_it = df[df["Land"] == "Italien"].copy()
    df_it["Subregion_normalized"] = df_it["Subregion"].apply(normalize_string)
    df_it["Region_plot"] = df_it["Subregion_normalized"].apply(categorize_region)
    regionen_it = df_it["Region_plot"].value_counts()
    total_weine = regionen_it.sum()
    prozent = (regionen_it / total_weine * 100).round(1)

    st.subheader(titel)
    st.caption("Nur 75 cl Flaschen berücksichtigt.")

    col1, col2 = st.columns([1.5, 1])

    with col1:
        bar_color = "#2B4C7E"  # Gleiches CI-Blau wie überall
        fig = px.bar(
            x=regionen_it.index,
            y=regionen_it.values,
            text=regionen_it.values,
            color_discrete_sequence=[bar_color]
        )
        fig.update_traces(textposition="outside", textfont_size=13)
        fig.update_layout(
            height=chart_height,
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            xaxis_title="Region",
            yaxis_title="Anzahl Weine",
            xaxis_tickangle=-35,
            margin=dict(t=35, r=15, l=5, b=60)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        table_df = pd.DataFrame({
            "Region": regionen_it.index,
            "Anzahl": regionen_it.values,
            "Anteil %": prozent.values
        })
        total_row = pd.DataFrame({
            "Region": ["Total"],
            "Anzahl": [total_weine],
            "Anteil %": [prozent.sum().round(1)]
        })
        table_df = pd.concat([table_df, total_row], ignore_index=True)
        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )
        st.download_button(
            label="Tabelle als CSV herunterladen",
            data=table_df.to_csv(index=False).encode("utf-8"),
            file_name=f"italien_regionen_{pd.Timestamp.now().date()}.csv",
            mime="text/csv"
        )
    st.caption(f"Total: {total_weine} Italien-Weine | Stand: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")


import streamlit as st
import pandas as pd
import plotly.express as px
import unicodedata

def plot_schweiz_regionen(
    df: pd.DataFrame,
    region_col: str = "Region",
    titel: str = "Weinregionen der Schweiz im Sortiment",
    chart_height: int = 450
):
    """
    Zeigt die Regionen der Schweiz als Balkendiagramm und Tabelle nebeneinander.
    Spezial- und Normalisierungslogik wie im Quellskript.
    """
    def normalize_string(text):
        text = str(text).lower()
        text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
        text = text.replace('–', '-').replace(' ', '-')
        return text

    subregion_mapping = {
        "bodensee": "Ostschweiz",
        "ubrige-schweiz": "Andere"
    }

    def categorize_region(subregion_normalized):
        if subregion_normalized in subregion_mapping:
            return subregion_mapping[subregion_normalized]
        # Schreibweisen angleichen
        if subregion_normalized == "wallis":
            return "Wallis"
        elif subregion_normalized == "waadt":
            return "Waadt"
        elif subregion_normalized == "tessin":
            return "Tessin"
        elif subregion_normalized == "drei-seen-region":
            return "Drei-Seen-Region"
        elif subregion_normalized == "genf":
            return "Genf"
        elif subregion_normalized == "basel/aargau":
            return "Basel/Aargau"
        elif subregion_normalized == "zurich":
            return "Zürich"
        elif subregion_normalized == "schaffhausen":
            return "Schaffhausen"
        elif subregion_normalized == "graubunden":
            return "Graubünden"
        elif subregion_normalized == "ostschweiz":
            return "Ostschweiz"
        elif subregion_normalized == "thurgau":
            return "Thurgau"
        elif subregion_normalized == "st.-gallen":
            return "St. Gallen"
        return subregion_normalized.capitalize()

    df = df.copy()
    df["Land"] = df[region_col].apply(lambda x: str(x).split(",")[0].strip() if "," in str(x) else str(x))
    df["Subregion"] = df[region_col].apply(lambda x: str(x).split(",")[1].strip() if "," in str(x) else "Keine Subregion")
    df_ch = df[df["Land"] == "Schweiz"].copy()
    df_ch["Subregion_normalized"] = df_ch["Subregion"].apply(normalize_string)
    df_ch["Region_plot"] = df_ch["Subregion_normalized"].apply(categorize_region)
    regionen_ch = df_ch["Region_plot"].value_counts()
    total_weine = regionen_ch.sum()
    prozent = (regionen_ch / total_weine * 100).round(1)

    st.subheader(titel)
    st.caption("Nur 75 cl Flaschen berücksichtigt.")

    col1, col2 = st.columns([1.5, 1])

    with col1:
        bar_color = "#2B4C7E"
        fig = px.bar(
            x=regionen_ch.index,
            y=regionen_ch.values,
            text=regionen_ch.values,
            color_discrete_sequence=[bar_color]
        )
        fig.update_traces(textposition="outside", textfont_size=13)
        fig.update_layout(
            height=chart_height,
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            xaxis_title="Region",
            yaxis_title="Anzahl Weine",
            xaxis_tickangle=-35,
            margin=dict(t=35, r=15, l=5, b=60)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        table_df = pd.DataFrame({
            "Region": regionen_ch.index,
            "Anzahl": regionen_ch.values,
            "Anteil %": prozent.values
        })
        total_row = pd.DataFrame({
            "Region": ["Total"],
            "Anzahl": [total_weine],
            "Anteil %": [prozent.sum().round(1)]
        })
        table_df = pd.concat([table_df, total_row], ignore_index=True)
        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )
        st.download_button(
            label="Tabelle als CSV herunterladen",
            data=table_df.to_csv(index=False).encode("utf-8"),
            file_name=f"schweiz_regionen_{pd.Timestamp.now().date()}.csv",
            mime="text/csv"
        )
    st.caption(f"Total: {total_weine} Schweiz-Weine | Stand: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")


import streamlit as st
import pandas as pd
import plotly.express as px
import unicodedata
import re

def plot_spanien_regionen(
    df: pd.DataFrame,
    region_col: str = "Region",
    titel: str = "Weinregionen Spaniens im Sortiment",
    chart_height: int = 450
):
    """
    Zeigt die Regionen Spaniens als Balkendiagramm und Tabelle nebeneinander.
    Inklusive Normalisierung/Mappings und Download, wie alle anderen Regionenanalysen.
    """
    def normalize_string(text):
        text = str(text).lower()
        text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
        text = text.replace('–', '-').replace(' ', '-')
        text = re.sub(r'-+', '-', text)
        text = re.sub(r'--+', '-', text)
        return text

    subregion_mapping = {
        "priorat": "Katalonien",
        "ribera-del-duero": "Castilla y León",
        "rueda": "Castilla y León",
        "toro": "Castilla y León",
        "kastilien-leon": "Castilla y León",
        "cigales": "Castilla y León",
        "requena": "Valencia",
        "yecla-do": "Murcia",
        "kastilien-la-mancha": "Castilla-La Mancha",
        "mentrida-do-(toledo)": "Castilla-La Mancha",
        "dehesa-del-carrizal-do": "Castilla-La Mancha",
        "kastilien-l-a-mancha": "Castilla-La Mancha",
        "alava": "Rioja",
        "mallorca": "Balearen",
        "ubriges-spanien": "Andere",
        "keine-subregion": "Andere"
    }

    def categorize_region(subregion_normalized):
        if subregion_normalized in subregion_mapping:
            return subregion_mapping[subregion_normalized]
        if subregion_normalized == "teneriffa":
            return "Teneriffa"
        elif subregion_normalized == "navarra":
            return "Navarra"
        elif subregion_normalized == "galicien":
            return "Galicien"
        elif subregion_normalized == "somontano":
            return "Somontano"
        elif subregion_normalized == "jerez":
            return "Jerez"
        return subregion_normalized.capitalize()

    df = df.copy()
    df["Land"] = df[region_col].apply(lambda x: str(x).split(",")[0].strip() if "," in str(x) else str(x))
    df["Subregion"] = df[region_col].apply(lambda x: str(x).split(",")[1].strip() if "," in str(x) else "Keine Subregion")
    df_es = df[df["Land"] == "Spanien"].copy()
    df_es["Subregion_normalized"] = df_es["Subregion"].apply(normalize_string)
    df_es["Region_plot"] = df_es["Subregion_normalized"].apply(categorize_region)
    regionen_es = df_es["Region_plot"].value_counts()
    total_weine = regionen_es.sum()
    prozent = (regionen_es / total_weine * 100).round(1)

    st.subheader(titel)
    st.caption("Nur 75 cl Flaschen berücksichtigt.")

    col1, col2 = st.columns([1.5, 1])

    with col1:
        bar_color = "#2B4C7E"
        fig = px.bar(
            x=regionen_es.index,
            y=regionen_es.values,
            text=regionen_es.values,
            color_discrete_sequence=[bar_color]
        )
        fig.update_traces(textposition="outside", textfont_size=13)
        fig.update_layout(
            height=chart_height,
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            xaxis_title="Region",
            yaxis_title="Anzahl Weine",
            xaxis_tickangle=-35,
            margin=dict(t=35, r=15, l=5, b=60)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        table_df = pd.DataFrame({
            "Region": regionen_es.index,
            "Anzahl": regionen_es.values,
            "Anteil %": prozent.values
        })
        total_row = pd.DataFrame({
            "Region": ["Total"],
            "Anzahl": [total_weine],
            "Anteil %": [prozent.sum().round(1)]
        })
        table_df = pd.concat([table_df, total_row], ignore_index=True)
        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )
        st.download_button(
            label="Tabelle als CSV herunterladen",
            data=table_df.to_csv(index=False).encode("utf-8"),
            file_name=f"spanien_regionen_{pd.Timestamp.now().date()}.csv",
            mime="text/csv"
        )
    st.caption(f"Total: {total_weine} Spanien-Weine | Stand: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")


import streamlit as st
import pandas as pd
import plotly.express as px

def plot_top_herkunftslaender_fp(
    df: pd.DataFrame,
    herkunft_col: str = "Herkunft",
    titel: str = "Top-10 Herkunftsländer im Flaschenpost-Sortiment",
    chart_height: int = 450
):
    """
    Zeigt die Top-10 Herkunftsländer für Flaschenpost, Land aus 'Herkunft' vor ">", mit Tabelle & Download.
    """
    # Land extrahieren (alles vor >)
    df = df.copy()
    df["Land"] = df[herkunft_col].apply(lambda x: str(x).split(">")[0].strip() if ">" in str(x) else str(x).strip())
    top_laender = df["Land"].value_counts().head(10)
    total_weine = top_laender.sum()
    prozent = (top_laender / total_weine * 100).round(1)

    st.subheader(titel)
    col1, col2 = st.columns([1.5, 1])

    with col1:
        bar_color = "#2B4C7E" # CI-Konform, satter Blauton
        fig = px.bar(
            x=top_laender.index,
            y=top_laender.values,
            text=top_laender.values,
            color_discrete_sequence=[bar_color]
        )
        fig.update_traces(textposition="outside", textfont_size=14)
        fig.update_layout(
            height=chart_height,
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            xaxis_title="Land",
            yaxis_title="Anzahl Weine",
            xaxis_tickangle=-45,
            margin=dict(t=35, r=15, l=5, b=60)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        table_df = pd.DataFrame({
            "Land": top_laender.index,
            "Anzahl": top_laender.values,
            "Anteil %": prozent.values
        })
        total_row = pd.DataFrame({
            "Land": ["Total"],
            "Anzahl": [total_weine],
            "Anteil %": [prozent.sum().round(1)]
        })
        table_df = pd.concat([table_df, total_row], ignore_index=True)
        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )
        st.download_button(
            label="Tabelle als CSV herunterladen",
            data=table_df.to_csv(index=False).encode("utf-8"),
            file_name=f"top10_herkunft_flaschenpost_{pd.Timestamp.now().date()}.csv",
            mime="text/csv"
        )
    st.caption(f"Top 10 machen {100*total_weine/df.shape[0]:.1f}% des Sortiments aus | Stand: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")


import streamlit as st
import pandas as pd
import plotly.express as px

def plot_italien_regionen_fp(
    df: pd.DataFrame,
    herkunft_col: str = "Herkunft",
    titel: str = "Weinregionen Italiens im Flaschenpost-Sortiment",
    chart_height: int = 450
):
    """
    Italien-Regionen für Flaschenpost.
    Subregion wird aus 'Herkunft' nach erster Ebene 'Italien > ...' extrahiert und gemappt.
    """
    df = df.copy()
    # 1. Land aus Herkunft holen
    df["Land"] = df[herkunft_col].apply(lambda x: str(x).split(">")[0].strip())
    # 2. Nur Italien
    df_italien = df[df["Land"] == "Italien"].copy()
    # 3. Subregion alles nach "Italien >"
    df_italien["Subregion"] = df_italien[herkunft_col].apply(lambda x: ">".join(str(x).split(">")[1:]).strip() if ">" in str(x) else "Keine Subregion")
    # 4. Mapping wie in deinem Skript
    subregion_mapping = {
        "Abruzzen > Chieti": "Abruzzen",
        "Apulien > Gargano": "Apulien",
        "Apulien > Manduria": "Apulien",
        "Apulien > Salento": "Apulien",
        "Emilia-Romagna > Forli-Cesena": "Emilia-Romagna",
        "Friaul > Isonzo": "Friaul",
        "Latium > Castelli Romani": "Latium",
        "Latium > Frascati": "Latium",
        "Ligurien > Portofino": "Ligurien",
        "Lombardei > Bergamo": "Lombardei",
        "Lombardei > Montello": "Lombardei",
        "Lombardei > Pavia": "Lombardei",
        "Lombardei > Veltlin": "Lombardei",
        "Marche > Matelica": "Marche",
        "Marche > Offida": "Marche",
        "Piemont > Alba": "Piemont",
        "Piemont > Alessandria": "Piemont",
        "Piemont > Alta Langa": "Piemont",
        "Piemont > Castelletto": "Piemont",
        "Piemont > Colline": "Piemont",
        "Piemont > Cuneo": "Piemont",
        "Piemont > Langhe": "Piemont",
        "Piemont > Monferrato": "Piemont",
        "Piemont > Monforte d'Alba": "Piemont",
        "Piemont > Vezza d’Alba": "Piemont",
        "Sizilien > Caltanissetta": "Sizilien",
        "Sizilien > Noto": "Sizilien",
        "Sizilien > West-Sizilien": "Sizilien",
        "Veneto > Asolo": "Venetien",
        "Veneto > Colli Euganei": "Venetien",
        "Veneto > Valdobbiadine": "Venetien",
        "Keine Subregion": "Andere",
    }
    df_italien["Hauptregion"] = df_italien["Subregion"].apply(lambda x: subregion_mapping.get(x, x.split(">")[0].strip()))
    regionen_italien = df_italien["Hauptregion"].value_counts()
    total_weine = regionen_italien.sum()
    prozent = (regionen_italien / total_weine * 100).round(1)

    st.subheader(titel)
    col1, col2 = st.columns([1.5, 1])

    with col1:
        bar_color = "#2B4C7E"
        fig = px.bar(
            x=regionen_italien.index,
            y=regionen_italien.values,
            text=regionen_italien.values,
            color_discrete_sequence=[bar_color]
        )
        fig.update_traces(textposition="outside", textfont_size=13)
        fig.update_layout(
            height=chart_height,
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            xaxis_title="Region",
            yaxis_title="Anzahl Weine",
            xaxis_tickangle=-35,
            margin=dict(t=35, r=15, l=5, b=60)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        table_df = pd.DataFrame({
            "Region": regionen_italien.index,
            "Anzahl": regionen_italien.values,
            "Anteil %": prozent.values
        })
        total_row = pd.DataFrame({
            "Region": ["Total"],
            "Anzahl": [total_weine],
            "Anteil %": [prozent.sum().round(1)]
        })
        table_df = pd.concat([table_df, total_row], ignore_index=True)
        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )
        st.download_button(
            label="Tabelle als CSV herunterladen",
            data=table_df.to_csv(index=False).encode("utf-8"),
            file_name=f"italien_regionen_fp_{pd.Timestamp.now().date()}.csv",
            mime="text/csv"
        )
    st.caption(f"Total: {total_weine} Italien-Weine | Stand: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")


import streamlit as st
import pandas as pd
import plotly.express as px

def plot_frankreich_regionen_fp(
    df: pd.DataFrame,
    herkunft_col: str = "Herkunft",
    titel: str = "Weinregionen Frankreichs im Flaschenpost-Sortiment",
    chart_height: int = 450
):
    """
    Regionen Frankreichs für Flaschenpost, Subregion aus 'Herkunft' nach 'Frankreich > ...', Mapping wie geliefert.
    """
    df = df.copy()
    df["Land"] = df[herkunft_col].apply(lambda x: str(x).split(">")[0].strip())
    df_frankreich = df[df["Land"] == "Frankreich"].copy()
    df_frankreich["Subregion"] = df_frankreich[herkunft_col].apply(
        lambda x: ">".join(str(x).split(">")[1:]).strip() if ">" in str(x) else "Keine Subregion"
    )
    subregion_mapping = {
        # Bordeaux (alle Subregionen zusammenfassen)
        "Bordeaux > Barsac": "Bordeaux",
        "Bordeaux > Canon-Fronsac": "Bordeaux",
        "Bordeaux > Côtes de Blaye": "Bordeaux",
        "Bordeaux > Côtes de Bourg": "Bordeaux",
        "Bordeaux > Côtes de Castillon": "Bordeaux",
        "Bordeaux > Côtes de Francs": "Bordeaux",
        "Bordeaux > Entre-Deux-Mers": "Bordeaux",
        "Bordeaux > Fronsac": "Bordeaux",
        "Bordeaux > Graves": "Bordeaux",
        "Bordeaux > Haut-Médoc": "Bordeaux",
        "Bordeaux > Lalande-de-Pomerol": "Bordeaux",
        "Bordeaux > Margaux (Médoc)": "Bordeaux",
        "Bordeaux > Moulis & Listrac (Médoc)": "Bordeaux",
        "Bordeaux > Pauillac (Médoc)": "Bordeaux",
        "Bordeaux > Pessac-Léognan": "Bordeaux",
        "Bordeaux > Pomerol": "Bordeaux",
        "Bordeaux > Premières Côtes de Bordeaux": "Bordeaux",
        "Bordeaux > Sauternes": "Bordeaux",
        "Bordeaux > St-Emilion": "Bordeaux",
        "Bordeaux > St-Estèphe (Médoc)": "Bordeaux",
        "Bordeaux > St-Julien (Médoc)": "Bordeaux",
        "Bordeaux > Übriges Médoc": "Bordeaux",
        # Burgund
        "Burgund > Beaujolais": "Burgund",
        "Burgund > Beaujolais > Saint-Amour": "Burgund",
        "Burgund > Chablis": "Burgund",
        "Burgund > Côte Chalonnaise (Côte d'Or)": "Burgund",
        "Burgund > Côte de Beaune (Côte d'Or)": "Burgund",
        "Burgund > Côte de Beaune (Côte d'Or) > Volnay": "Burgund",
        "Burgund > Côte de Nuits (Côte d'Or)": "Burgund",
        "Burgund > Mâcon": "Burgund",
        # Rhône
        "Côtes du Rhône": "Rhône",
        "Côtes du Rhône > Châteauneuf-du-Pape (Südliche Rhône)": "Rhône",
        "Côtes du Rhône > Côtes du Ventoux (Südliche Rhône)": "Rhône",
        "Côtes du Rhône > Grignan-les-Adhémar": "Rhône",
        "Côtes du Rhône > Nördliche Rhône": "Rhône",
        "Côtes du Rhône > Übrige Südliche Rhône": "Rhône",
        # Loire
        "Loire > Anjou-Saumour": "Loire",
        "Loire > Obere Loire": "Loire",
        "Loire > Pays Nantais (Muscadet)": "Loire",
        "Loire > Touraine": "Loire",
        # Südfrankreich (Midi/Provence)
        "Midi - Languedoc-Roussillon": "Südfrankreich",
        "Midi - Languedoc-Roussillon > Corbières": "Südfrankreich",
        "Midi - Languedoc-Roussillon > Coteaux du Languedoc": "Südfrankreich",
        "Midi - Languedoc-Roussillon > Minervois": "Südfrankreich",
        "Midi - Languedoc-Roussillon > Minervois-La-Livinière": "Südfrankreich",
        "Midi - Languedoc-Roussillon > Roussillon": "Südfrankreich",
        "Midi - Languedoc-Roussillon > Terrasses de Béziers": "Südfrankreich",
        "Provence": "Südfrankreich",
        "Provence > Côte d’Azur > L'Isle-sur-la-Sorgue": "Südfrankreich",
        "Okzitanien": "Andere",
        "Okzitanien > Hérault": "Andere",
        "Okzitanien > Sud France": "Andere",
        # Sonstige
        "Champagne": "Champagne",
        "Elsass": "Elsass",
        "Jura": "Jura",
        "Korsika": "Korsika",
        "Savoyen": "Savoyen",
        "Südwesten": "Südwesten",
        "Südwesten > Bergerac": "Südwesten",
        "Südwesten > Béarn & Pyrenäen": "Südwesten",
        "Südwesten > Cahors": "Südwesten",
        "Südwesten > Gaillac": "Südwesten",
        "Keine Subregion": "Andere",
        "Auvergne-Rhône-Alpes": "Andere",
        "Normandie": "Andere"
    }
    df_frankreich["Hauptregion"] = df_frankreich["Subregion"].apply(
        lambda x: subregion_mapping.get(x, x.split(">")[0].strip())
    )
    regionen_frankreich = df_frankreich["Hauptregion"].value_counts()
    total_weine = regionen_frankreich.sum()
    prozent = (regionen_frankreich / total_weine * 100).round(1)

    st.subheader(titel)
    col1, col2 = st.columns([1.5, 1])

    with col1:
        bar_color = "#2B4C7E"
        fig = px.bar(
            x=regionen_frankreich.index,
            y=regionen_frankreich.values,
            text=regionen_frankreich.values,
            color_discrete_sequence=[bar_color]
        )
        fig.update_traces(textposition="outside", textfont_size=13)
        fig.update_layout(
            height=chart_height,
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            xaxis_title="Region",
            yaxis_title="Anzahl Weine",
            xaxis_tickangle=-35,
            margin=dict(t=35, r=15, l=5, b=60)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        table_df = pd.DataFrame({
            "Region": regionen_frankreich.index,
            "Anzahl": regionen_frankreich.values,
            "Anteil %": prozent.values
        })
        total_row = pd.DataFrame({
            "Region": ["Total"],
            "Anzahl": [total_weine],
            "Anteil %": [prozent.sum().round(1)]
        })
        table_df = pd.concat([table_df, total_row], ignore_index=True)
        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )
        st.download_button(
            label="Tabelle als CSV herunterladen",
            data=table_df.to_csv(index=False).encode("utf-8"),
            file_name=f"frankreich_regionen_fp_{pd.Timestamp.now().date()}.csv",
            mime="text/csv"
        )
    st.caption(f"Total: {total_weine} Frankreich-Weine | Stand: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")


import streamlit as st
import pandas as pd
import plotly.express as px

def plot_spanien_regionen_fp(
    df: pd.DataFrame,
    herkunft_col: str = "Herkunft",
    titel: str = "Weinregionen Spaniens im Flaschenpost-Sortiment",
    chart_height: int = 450
):
    """
    Regionen Spanien für Flaschenpost, Subregion aus 'Herkunft' nach 'Spanien > ...', komplexes Mapping wie geliefert.
    """
    df = df.copy()
    df["Land"] = df[herkunft_col].apply(lambda x: str(x).split(">")[0].strip())
    df_spanien = df[df["Land"] == "Spanien"].copy()
    df_spanien["Subregion"] = df_spanien[herkunft_col].apply(
        lambda x: ">".join(str(x).split(">")[1:]).strip() if ">" in str(x) else "Keine Subregion"
    )
    subregion_mapping = {
        "Andalusien": "Andalusien",
        "Balearen": "Balearen",
        "Balearen > Mallorca": "Balearen",
        "Baskenland": "Baskenland",
        "Baskenland > Getariako Txakolina": "Baskenland",
        "Duero-Tal (Castilla y Leon)": "Castilla y León",
        "Duero-Tal (Castilla y Leon) > Bierzo": "Castilla y León",
        "Duero-Tal (Castilla y Leon) > Cigales": "Castilla y León",
        "Duero-Tal (Castilla y Leon) > Ribera del Duero": "Castilla y León",
        "Duero-Tal (Castilla y Leon) > Rueda": "Castilla y León",
        "Duero-Tal (Castilla y Leon) > Toro": "Castilla y León",
        "Extremadura": "Extremadura",
        "Galizien": "Galizien",
        "Galizien > Monterrei": "Galizien",
        "Galizien > Ribeira Sacra": "Galizien",
        "Galizien > Ribeiro": "Galizien",
        "Galizien > Rías Baixas": "Galizien",
        "Galizien > Valdeorras": "Galizien",
        "Kanarische Inseln": "Kanarische Inseln",
        "Kanarische Inseln > Teneriffa": "Kanarische Inseln",
        "Katalonien": "Katalonien",
        "Katalonien > Ampurdán-Costa Brava": "Katalonien",
        "Katalonien > Barcelona": "Katalonien",
        "Katalonien > Castellet i la Gornal": "Katalonien",
        "Katalonien > Cava": "Katalonien",
        "Katalonien > Costers del Segre": "Katalonien",
        "Katalonien > Cónca de Barberà": "Katalonien",
        "Katalonien > Montsant": "Katalonien",
        "Katalonien > Penedès": "Katalonien",
        "Katalonien > Pla de Bages": "Katalonien",
        "Katalonien > Tarragona": "Katalonien",
        "Katalonien > Terra Alta": "Katalonien",
        "Levante": "Levante",
        "Levante > Alicante": "Levante",
        "Levante > Murcia": "Levante",
        "Levante > Valencia": "Levante",
        "Meseta": "Meseta",
        "Meseta > Castilla-La Mancha": "Meseta",
        "Meseta > Madrid": "Meseta",
        "Oberer Ebro": "Oberer Ebro",
        "Oberer Ebro > Aragón": "Oberer Ebro",
        "Oberer Ebro > La Rioja": "Oberer Ebro",
        "Oberer Ebro > La Rioja > Rioja Alavesa": "Oberer Ebro",
        "Oberer Ebro > La Rioja > Rioja Alta": "Oberer Ebro",
        "Oberer Ebro > La Rioja > Rioja Baja": "Oberer Ebro",
        "Oberer Ebro > Navarra": "Oberer Ebro",
        "Somontano": "Somontano",
        "Valtuille": "Castilla y León",
        "Keine Subregion": "Andere"
    }
    df_spanien["Hauptregion"] = df_spanien["Subregion"].map(subregion_mapping).fillna("Andere")
    regionen_spanien = df_spanien["Hauptregion"].value_counts()
    total_weine = regionen_spanien.sum()
    prozent = (regionen_spanien / total_weine * 100).round(1)

    st.subheader(titel)
    col1, col2 = st.columns([1.5, 1])

    with col1:
        bar_color = "#2B4C7E"
        fig = px.bar(
            x=regionen_spanien.index,
            y=regionen_spanien.values,
            text=regionen_spanien.values,
            color_discrete_sequence=[bar_color]
        )
        fig.update_traces(textposition="outside", textfont_size=13)
        fig.update_layout(
            height=chart_height,
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            xaxis_title="Region",
            yaxis_title="Anzahl Weine",
            xaxis_tickangle=-35,
            margin=dict(t=35, r=15, l=5, b=60)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        table_df = pd.DataFrame({
            "Region": regionen_spanien.index,
            "Anzahl": regionen_spanien.values,
            "Anteil %": prozent.values
        })
        total_row = pd.DataFrame({
            "Region": ["Total"],
            "Anzahl": [total_weine],
            "Anteil %": [prozent.sum().round(1)]
        })
        table_df = pd.concat([table_df, total_row], ignore_index=True)
        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )
        st.download_button(
            label="Tabelle als CSV herunterladen",
            data=table_df.to_csv(index=False).encode("utf-8"),
            file_name=f"spanien_regionen_fp_{pd.Timestamp.now().date()}.csv",
            mime="text/csv"
        )
    st.caption(f"Total: {total_weine} Spanien-Weine | Stand: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")


import streamlit as st
import pandas as pd
import plotly.express as px

def plot_schweiz_regionen_fp(
    df: pd.DataFrame,
    herkunft_col: str = "Herkunft",
    titel: str = "Weinregionen der Schweiz im Flaschenpost-Sortiment",
    chart_height: int = 450
):
    """
    Regionen Schweiz für Flaschenpost. Subregion nach 'Schweiz > ...', Mapping wie geliefert.
    """
    df = df.copy()
    df["Land"] = df[herkunft_col].apply(lambda x: str(x).split(">")[0].strip())
    df_schweiz = df[df["Land"] == "Schweiz"].copy()
    df_schweiz["Subregion"] = df_schweiz[herkunft_col].apply(
        lambda x: ">".join(str(x).split(">")[1:]).strip() if ">" in str(x) else "Keine Subregion"
    )
    subregion_mapping = {
        "Aargau": "Basel/Aargau",
        "Basel": "Basel/Aargau",
        "Basel > Basel-Landschaft": "Basel/Aargau",
        "Freiburg": "Drei-Seen-Region",
        "Neuenburg": "Drei-Seen-Region",
        "Westschweiz": "Waadt",
        "Waadt": "Waadt",
        "Waadt > Aigle": "Waadt",
        "Waadt > Aigle > Villeneuve": "Waadt",
        "Waadt > Aigle > Yvorne": "Waadt",
        "Waadt > Lavaux-Oron > Bourg-en-Lavaux > Epesses": "Waadt",
        "Waadt > Lavaux-Oron > Bourg-en-Lavaux > Villette": "Waadt",
        "Waadt > Morges > Aubonne": "Waadt",
        "Waadt > Morges > Féchy": "Waadt",
        "Waadt > Nyon > Dully": "Waadt",
        "Waadt > Nyon > Gilly": "Waadt",
        "Waadt > Nyon > Luins": "Waadt",
        "Waadt > Nyon > Tartegnin": "Waadt",
        "Waadt > Puidoux > Dézaley": "Waadt",
        "Bern": "Bern",
        "Bündner Herrschaft": "Graubünden",
        "Genf": "Genf",
        "Luzern": "Luzern",
        "Schaffhausen": "Schaffhausen",
        "Tessin": "Tessin",
        "Wallis": "Wallis",
        "Zürich": "Zürich",
        "Ostschweiz": "Ostschweiz",
        "Keine Subregion": "Andere"
    }
    df_schweiz["Hauptregion"] = df_schweiz["Subregion"].map(subregion_mapping).fillna("Andere")
    regionen_schweiz = df_schweiz["Hauptregion"].value_counts()
    total_weine = regionen_schweiz.sum()
    prozent = (regionen_schweiz / total_weine * 100).round(1)

    st.subheader(titel)
    col1, col2 = st.columns([1.5, 1])

    with col1:
        bar_color = "#2B4C7E"
        fig = px.bar(
            x=regionen_schweiz.index,
            y=regionen_schweiz.values,
            text=regionen_schweiz.values,
            color_discrete_sequence=[bar_color]
        )
        fig.update_traces(textposition="outside", textfont_size=13)
        fig.update_layout(
            height=chart_height,
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            xaxis_title="Region",
            yaxis_title="Anzahl Weine",
            xaxis_tickangle=-35,
            margin=dict(t=35, r=15, l=5, b=60)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        table_df = pd.DataFrame({
            "Region": regionen_schweiz.index,
            "Anzahl": regionen_schweiz.values,
            "Anteil %": prozent.values
        })
        total_row = pd.DataFrame({
            "Region": ["Total"],
            "Anzahl": [total_weine],
            "Anteil %": [prozent.sum().round(1)]
        })
        table_df = pd.concat([table_df, total_row], ignore_index=True)
        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )
        st.download_button(
            label="Tabelle als CSV herunterladen",
            data=table_df.to_csv(index=False).encode("utf-8"),
            file_name=f"schweiz_regionen_fp_{pd.Timestamp.now().date()}.csv",
            mime="text/csv"
        )
    st.caption(f"Total: {total_weine} Schweiz-Weine | Stand: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")



def plot_matching_overview_gemini(df: pd.DataFrame):
    st.header("Übersicht: Produkt-Matching")
    st.caption("Wie gut finden wir passende Wein-Paare zwischen Coop und Flaschenpost?")

    # --- Block 1: Kern-KPIs und kurze Einführung in die Matching-Logik ---
    col1_intro, col2_kpis = st.columns([1.5, 2]) # Linke Spalte für Text, rechte für KPIs

    with col1_intro:
        st.subheader("So funktioniert unser Matching:")
        st.markdown("""
        Unser Ziel ist es, identische oder sehr ähnliche Weine zu finden. Dafür kombinieren wir:
        *   **Klare Vorfilter:** Nur Weine mit gleichem Jahrgang, Typ und ähnlichem Preis werden überhaupt betrachtet.
        *   **Intelligenter Textabgleich (Fuzzy-Score):** Produktnamen werden normalisiert (z.B. "Domaine Lafage" wird zu "lafage") und dann auf Ähnlichkeit geprüft (Score 0-100).
        *   **Experten-Matches:** Manuell bestätigte Paare (Score -1) haben höchste Priorität.
        """)
        st.info("Ein **Score von >50** gilt als automatischer Match-Kandidat. Details weiter unten.")


    with col2_kpis:
        st.subheader("Matching-Kennzahlen im Überblick")
        # Berechnungen
        anzahl_coop_weine = len(df)
        auto_mask = (df["Fuzzy_Score"] > 0)
        n_auto = auto_mask.sum()
        manu_mask = (df["Fuzzy_Score"] == -1)
        n_manuell = manu_mask.sum()
        n_match = n_auto + n_manuell
        matchquote_gesamt = (n_match / anzahl_coop_weine * 100) if anzahl_coop_weine > 0 else 0
        
        # KPIs in zwei Reihen für bessere Lesbarkeit, wenn viele Metriken
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)

        row1_col1.metric("Coop-SKUs analysiert", f"{anzahl_coop_weine}")
        row1_col2.metric("Matchquote Gesamt", f"{matchquote_gesamt:.1f}%")
        row2_col1.metric("Automatische Matches (Score >0)", f"{n_auto}",
                         help="Anzahl automatisch gefundener Paare basierend auf Textähnlichkeit (Score > 0).")
        row2_col2.metric("Manuelle Matches (Score -1)", f"{n_manuell}",
                         help="Anzahl von Experten bestätigter Paare.")
    st.markdown("---")

    # --- Block 2: Detailanalyse der automatischen Matches (Histogramm + Score-Klassen) ---
    st.subheader("Analyse der automatischen Matches (Score > 0)")
    df_auto = df[auto_mask].copy()

    if not df_auto.empty:
        col_hist, col_score_table = st.columns([1.8, 1.2]) # Histogramm breiter

        with col_hist:
            st.markdown("##### Verteilung der Fuzzy-Scores")
            fig_hist = px.histogram(
                df_auto, x="Fuzzy_Score", nbins=20,
                color_discrete_sequence=["#0072B2"] # Ein anderer Blauton
            )
            fig_hist.update_layout(
                xaxis_title="Fuzzy-Score (0-100)",
                yaxis_title="Anzahl Matches",
                plot_bgcolor="#F9F9F9", # Leichter Hintergrund für den Plot
                bargap=0.1,
                height=350 # Feste Höhe, kann angepasst werden
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        with col_score_table:
            st.markdown("##### Matches nach Score-Klasse")
            bins_orig = [0, 40, 60, 80, 90, 95, 100]
            labels_orig = ["(0, 40]", "(40, 60]", "(60, 80]", "(80, 90]", "(90, 95]", "(95, 100]"]

            if df_auto["Fuzzy_Score"].notna().all():
                df_auto.loc[:, "Score_Klasse"] = pd.cut(
                    df_auto["Fuzzy_Score"],
                    bins=bins_orig,
                    labels=labels_orig,
                    include_lowest=True,
                    right=True
                )
                score_tab_series = df_auto["Score_Klasse"].value_counts(sort=False).reindex(labels_orig, fill_value=0)
                
                # Tabelle mit Prozentanteilen für bessere Vergleichbarkeit
                score_tab_df = pd.DataFrame({
                    "Score-Klasse": score_tab_series.index,
                    "Anzahl": score_tab_series.values,
                    "Anteil (%)": (score_tab_series.values / score_tab_series.sum() * 100 if score_tab_series.sum() > 0 else 0)
                })
                score_tab_df["Anteil (%)"] = score_tab_df["Anteil (%)"].round(1)
                
                st.dataframe(
                    score_tab_df.set_index("Score-Klasse"),
                    use_container_width=True,
                    height=310 # Etwas weniger Höhe als Plot
                )
                st.caption("Zeigt, wie sich Matches auf Score-Bereiche verteilen. Höher = bessere Ähnlichkeit.")
            else:
                st.warning("Score-Klassen nicht darstellbar (fehlende Scores).")
    else:
        st.info("Keine automatischen Matches für eine Detailanalyse vorhanden.")
    st.markdown("---")

    # --- Block 3: Manuelle Matches und optional tiefere Erklärung ---
    col_manual_info, col_expander_placeholder = st.columns(2)

    with col_manual_info:
        st.subheader("Manuelle Matches (Score = -1)")
        st.success(f"**{n_manuell} Produkte** wurden von unseren Weinexperten manuell und mit höchster Sicherheit gematcht.")
        st.markdown("""
        Diese Matches sind besonders wertvoll, da sie:
        *   Komplexe Fälle abdecken, die Algorithmen schwer erfassen.
        *   Eine zusätzliche Qualitätssicherung darstellen.
        """)

    with col_expander_placeholder: # Platzhalter für zukünftige Erweiterungen oder andere Infos
        st.empty() # Hält die Spaltenstruktur, kann später befüllt werden
        # Alternativ: Hier könnte der Expander für sehr detaillierte Infos sein, falls doch benötigt
        # with st.expander("Tiefergehende Details zum Matching-Algorithmus (für Experten)"):
        #    st.markdown("Hier die sehr technischen Details...")

    st.sidebar.subheader("Filter & Optionen") # Beispiel für Sidebar-Nutzung
    st.sidebar.info("Hier könnten zukünftig Filter für diese Matching-Übersicht platziert werden (z.B. nach Weintyp, Region etc.).")


# --- Beispielhafter Aufruf ---
if __name__ == "__main__":
    np.random.seed(42)
    num_samples = 250
    fuzzy_scores_sample = np.random.choice(
        list(range(51, 101)) + [-1]*25, # Mehr hohe Scores und einige manuelle
        num_samples,
        p=[0.9/50]*50 + [0.1] # Wahrscheinlichkeiten anpassen
    )
    # Sorge dafür, dass die Summe der p-Werte 1 ist
    num_auto_scores = 50
    prob_manual = 0.15 # 15% manuelle Matches
    prob_per_auto_score = (1 - prob_manual) / num_auto_scores

    fuzzy_scores_sample = np.random.choice(
        list(range(51, 101)) + [-1],
        num_samples,
        p=[prob_per_auto_score]*num_auto_scores + [prob_manual]
    )


    sample_data = {'Fuzzy_Score': fuzzy_scores_sample}
    dummy_df_main = pd.DataFrame(sample_data)

    st.title("Streamlit Dashboard Demo")
    plot_matching_overview(dummy_df_main)



def plot_percent_price_comparison(df: pd.DataFrame):
    """
    Prozentuale Preisdifferenzen Coop vs Flaschenpost
    - Histogramm
    - KPIs (Mittelwert, Median, Anteil >±X%)
    """
    mask = (df["Fuzzy_Score"] > 0) | (df["Fuzzy_Score"] == -1)
    df_vgl = df[mask].copy()

    df_vgl["Coop_Preis"] = df_vgl["Coop_Preis"].astype(float)
    df_vgl["FP_Preis"] = df_vgl["FP_Preis"].astype(float)
    df_vgl = df_vgl[df_vgl["FP_Preis"] > 0] # Schutz gegen Division durch Null

    df_vgl["Perc_Diff"] = (df_vgl["Coop_Preis"] - df_vgl["FP_Preis"]) / df_vgl["FP_Preis"] * 100

    n_total = len(df_vgl)
    n_coop_5guenstiger = (df_vgl["Perc_Diff"] < -5).sum()
    n_fp_5guenstiger = (df_vgl["Perc_Diff"] > 5).sum()
    n_fast_gleich = ((df_vgl["Perc_Diff"] >= -2) & (df_vgl["Perc_Diff"] <= 2)).sum()
    median_diff = df_vgl["Perc_Diff"].median()
    mean_diff = df_vgl["Perc_Diff"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Vergleichbare Weine", n_total)
    col2.metric("Coop >5% günstiger", n_coop_5guenstiger, f"{n_coop_5guenstiger/n_total:.1%}")
    col3.metric("FP >5% günstiger", n_fp_5guenstiger, f"{n_fp_5guenstiger/n_total:.1%}")
    col4.metric("Median Preisdiff.", f"{median_diff:.1f} %")

    st.caption("*Preisdifferenz: (Coop − FP) / FP. Negativ = Coop günstiger, Positiv = Flaschenpost günstiger.*")

    st.write("### Histogramm der prozentualen Preisdifferenzen")
    fig = px.histogram(
        df_vgl, x="Perc_Diff", nbins=31,
        color_discrete_sequence=["#2B4C7E"])
    fig.update_layout(
        xaxis_title="Preis-Differenz (% Coop minus FP)",
        yaxis_title="Anzahl Weine",
        plot_bgcolor="#ffffff"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write(f"**Ähnlich gepreist (±2 %)**: {n_fast_gleich} Weine ({n_fast_gleich/n_total:.1%})")



import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def plot_percent_price_comparison_gemini1(df: pd.DataFrame): # Erwartet df mit "Diff_%"
    st.header("Preisvergleich: Coop vs. Flaschenpost (FP)")
    st.caption("Vergleich von Weinen (Fuzzy Score > 0 oder -1).")

    required_cols_for_context = ['Fuzzy_Score', 'Coop_Preis', 'FP_Preis', 'Diff_%']
    if not all(col in df.columns for col in required_cols_for_context):
        missing = [col for col in required_cols_for_context if col not in df.columns]
        st.error(f"Fehlende Spalten für Preisdifferenzanalyse: {', '.join(missing)}")
        return

    mask = (df["Fuzzy_Score"] > 0) | (df["Fuzzy_Score"] == -1)
    df_vgl = df[mask].copy()

    # Preisspalten konvertieren (könnte redundant sein, wenn schon in matching.py passiert, schadet aber nicht)
    try:
        df_vgl["Coop_Preis"] = pd.to_numeric(df_vgl["Coop_Preis"], errors='coerce')
        df_vgl["FP_Preis"] = pd.to_numeric(df_vgl["FP_Preis"], errors='coerce')
    except Exception as e:
        st.error(f"Fehler bei Konvertierung der Preisspalten: {e}")
        # return # Nicht unbedingt return, wenn Diff_% schon da ist

    # Explizite Konvertierung von Diff_% zu numerisch auf der Kopie df_vgl
    if "Diff_%" in df_vgl.columns:
        df_vgl["Diff_%"] = pd.to_numeric(df_vgl["Diff_%"], errors='coerce')
    else:
        st.error("Spalte 'Diff_%' fehlt im DataFrame df_vgl.") # Sollte nicht passieren, wenn required_cols Check besteht
        return

    # NaNs entfernen, nachdem alle relevanten Spalten numerisch sind oder konvertiert wurden
    df_vgl.dropna(subset=["Coop_Preis", "FP_Preis", "Diff_%"], inplace=True)

    if df_vgl.empty:
        st.warning("Keine gültigen Weinpaare für den Vergleich nach Filterung/dropna.")
        return
    
    n_total = len(df_vgl)
    
    # Median jetzt auf der Spalte "Diff_%" berechnen, NACHDEM sie konvertiert und NaNs entfernt wurden
    if "Diff_%" in df_vgl.columns and pd.api.types.is_numeric_dtype(df_vgl["Diff_%"]) and df_vgl["Diff_%"].notna().any():
        median_diff = df_vgl["Diff_%"].median()
    else:
        # Dieser Fall sollte jetzt seltener auftreten
        st.warning("Spalte 'Diff_%' ist nicht numerisch oder enthält nur NaNs nach der Aufbereitung.")
        median_diff = pd.NA 


    # --- 2. Kategorisierung (bleibt gleich, verwendet jetzt das aufbereitete Diff_%) ---
    bins = [-np.inf, -5, -2, 2, 5, np.inf]
    labels = ["Coop >5% günstiger", "Coop 2–5% günstiger", "Preis ähnlich (±2%)", "FP 2–5% günstiger", "FP >5% günstiger"]
    
    if "Diff_%" in df_vgl.columns and pd.api.types.is_numeric_dtype(df_vgl["Diff_%"]): # Zusätzliche Typprüfung
        df_vgl["kategorie"] = pd.cut(df_vgl["Diff_%"], bins=bins, labels=labels, right=True, include_lowest=True)
        if df_vgl["kategorie"].isnull().any():
            # st.info("Einige Weine hatten Diff_%-Werte außerhalb der Bins oder NaN und wurden 'Unbekannt' zugeordnet.")
            df_vgl["kategorie"].fillna("Unbekannt", inplace=True)
            if "Unbekannt" not in labels and "Unbekannt" in df_vgl["kategorie"].unique():
                labels.append("Unbekannt")
        group_counts = df_vgl["kategorie"].value_counts().reindex(labels, fill_value=0)
    else:
        st.error("Spalte 'Diff_%' für Kategorisierung nicht numerisch oder nicht gefunden.")
        return

    # --- 3. Zusammenfassung / Kernaussage (bleibt gleich) ---
    st.subheader("Zusammenfassung der Ergebnisse")
    dominant_category = group_counts.idxmax() if not group_counts.empty else "N/A"
    dominant_category_count = group_counts.max() if not group_counts.empty else 0
    dominant_category_percent = (dominant_category_count / n_total * 100) if n_total > 0 else 0
    summary_text = f"""
    Insgesamt wurden **{n_total} Weinpaare** verglichen.
    *   Die häufigste Kategorie ist "**{dominant_category}**" mit **{dominant_category_count} Weinen ({dominant_category_percent:.1f}%)**.
    *   Der **Median** der Preisdifferenz beträgt **{median_diff if pd.notna(median_diff) else 'N/A'}%**.
        *   Ein negativer Wert bedeutet, dass Coop im Median günstiger ist.
        *   Ein positiver Wert bedeutet, dass Flaschenpost im Median günstiger ist (Coop teurer).
    """
    st.info(summary_text)

    # --- 4. Layout: KPIs/Erklärungen (links) und Histogramm (rechts) (bleibt gleich) ---
    # (Ich kürze diesen Teil für die Antwort, die Logik ist unverändert und sollte funktionieren,
    #  wenn median_diff und group_counts korrekt sind)
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("Aufteilung nach Preiskategorien")
        st.metric("Vergleichspaare Gesamt", n_total)
        st.markdown("---")
        for label_item in labels: 
            n = group_counts[label_item] if label_item in group_counts else 0
            percent_of_total = (n / n_total * 100) if n_total > 0 else 0
            st.metric(label_item, f"{n} Weine", f"{percent_of_total:.1f}%")
        st.caption("Berechnung: (Coop Preis - FP Preis) / FP Preis * 100%")
        st.markdown("---")
        st.subheader("Was bedeutet der Median?")
        st.markdown(f"""Der **Median** ist ... Median von **{median_diff if pd.notna(median_diff) else 'N/A'}%** ...""") # Sicherstellen, dass median_diff nicht NaN ist für f-string
        st.markdown("---") 
        if st.checkbox("Zeige Datentabelle der Kategorien", key="kategorie_tabelle_checkbox_gemini1_v2"):
             anteile_display = [f"{(group_counts[lbl]/n_total*100 if n_total > 0 else 0):.1f}%" for lbl in labels if lbl in group_counts]
             anzahl_werte = [group_counts[lbl] for lbl in labels if lbl in group_counts]
             kategorie_labels_fuer_tabelle = [lbl for lbl in labels if lbl in group_counts]
             table_data = {"Kategorie": kategorie_labels_fuer_tabelle, "Anzahl": anzahl_werte, "Anteil": anteile_display}
             st.table(pd.DataFrame(table_data))
    with col2:
        st.subheader("Verteilung der Preisdifferenzen")
        if "Diff_%" in df_vgl.columns and pd.api.types.is_numeric_dtype(df_vgl["Diff_%"]) and df_vgl["Diff_%"].notna().any() : # Zusätzliche Prüfung
            fig = px.histogram(df_vgl, x="Diff_%", nbins=max(30,min(n_total//5 if n_total>0 else 30,100)), title="Histogramm der prozentualen Preisdifferenzen", labels={'Diff_%':'Preisdifferenz (%)'}, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.add_vline(x=0, line_dash="solid",line_color="black",annotation_text="Gleicher Preis (0%)",annotation_position="top left")
            if pd.notna(median_diff): fig.add_vline(x=median_diff,line_dash="dash",line_color="red",annotation_text=f"Median: {median_diff:.1f}%",annotation_position="top right")
            fig.update_layout(yaxis_title="Anzahl Weinpaare",plot_bgcolor="#F9F9F9",bargap=0.1)
            st.plotly_chart(fig,use_container_width=True)
            st.caption("""Das Histogramm zeigt ...""")
        else: st.warning("Histogramm kann nicht erstellt werden (Diff_% nicht numerisch oder nur NaNs).")


# --- Beispielhafter Aufruf (bleibt gleich) ---
if __name__ == '__main__':
    # ... (Beispieldaten wie zuvor) ...
    np.random.seed(42); num_samples = 200
    fp_prices_sample = np.random.uniform(5, 50, num_samples)
    coop_prices_sample = fp_prices_sample * (1 + np.random.normal(-1, 8, num_samples) / 100)
    coop_prices_sample = np.round(coop_prices_sample, 2)
    sample_data = {'Fuzzy_Score': np.random.choice([100,95,90,85,-1],num_samples), 'Coop_Preis': coop_prices_sample, 'FP_Preis': fp_prices_sample}
    dummy_df_main = pd.DataFrame(sample_data)
    dummy_df_main["Diff_%"] = ((dummy_df_main['Coop_Preis'] - dummy_df_main['FP_Preis']) / dummy_df_main['FP_Preis']) * 100
    dummy_df_main["Diff_%"] = dummy_df_main["Diff_%"].round(1)
    dummy_df_main.loc[dummy_df_main.sample(frac=0.1).index, 'Diff_%'] = np.nan # Mehr NaNs für Test
    dummy_df_main.loc[dummy_df_main.sample(frac=0.05).index, 'Diff_%'] = "text" # Fehlerhafter Textwert
    st.title("Streamlit Dashboard Demo: Preisdifferenzanalyse")
    plot_percent_price_comparison_gemini1(dummy_df_main)



import streamlit as st
import pandas as pd
import numpy as np

def plot_price_outlier_table_enhanced(
    df: pd.DataFrame,
    fuzzy_col_internal: str = "Fuzzy_Score", 
    coop_preis_col: str = "Coop_Preis",
    fp_preis_col: str = "FP_Preis",
    coop_name_col: str = "Coop_Name",
    fp_name_col: str = "FP_Name",
    coop_produzent_col: str = "Coop_Produzent",
    fp_produzent_col: str = "FP_Produzent",
    coop_url_col: str = "Coop_URL",
    fp_sku_col: str = "FP_Sku",
    fp_lieferant_col: str = "FP_Lieferant",
    nps_fp_col: str = "NPS_FP",
    default_extra_columns: list = None,
    min_score_threshold: float = 0,
):
    st.header("Interaktive Ausreißer-Analyse der Preisdifferenzen")
    st.markdown("""
    Untersuchen Sie hier detailliert die Preisunterschiede und Produktdetails für gematchte Weine.
    Filtern und sortieren Sie, um Potenziale oder Auffälligkeiten zu identifizieren.
    """)

    # --- 1. Datenaufbereitung & initiale Filterung ---
    required_cols_for_calc = [fuzzy_col_internal, coop_preis_col, fp_preis_col, coop_name_col, fp_name_col]
    if not all(col in df.columns for col in required_cols_for_calc):
        missing = [col for col in required_cols_for_calc if col not in df.columns]; st.error(f"Fehlende Kernspalten: {', '.join(missing)}."); return
    
    mask = (df[fuzzy_col_internal] > min_score_threshold) | (df[fuzzy_col_internal] == -1)
    df_filtered = df[mask].copy() 
    
    for col_conv in [coop_preis_col, fp_preis_col, nps_fp_col]:
        if col_conv in df_filtered.columns: df_filtered[col_conv] = pd.to_numeric(df_filtered[col_conv], errors='coerce')
    
    df_filtered = df_filtered.dropna(subset=[coop_preis_col, fp_preis_col])
    if not df_filtered.empty: df_filtered = df_filtered[df_filtered[fp_preis_col] > 0]
    if df_filtered.empty: st.warning("Keine gültigen Vergleichsdaten nach Filterung."); return

    # SKU Normalisierung - KORRIGIERT
    if fp_sku_col in df_filtered.columns:
        def normalize_internal_sku(sku_val):
            if pd.isna(sku_val): 
                return None
            s = str(sku_val).strip() # s HIER DEFINIEREN
            if not s or s.lower() == 'nan': # Dann auf leere Strings oder 'nan' prüfen
                return None
            if s.endswith(".0"):
                try: return str(int(float(s)))
                except ValueError: return s
            return s
        df_filtered[fp_sku_col] = df_filtered[fp_sku_col].apply(normalize_internal_sku)

    df_filtered["Diff_CHF"] = df_filtered[coop_preis_col] - df_filtered[fp_preis_col]
    df_filtered["Diff_%"] = (df_filtered["Diff_CHF"] / df_filtered[fp_preis_col]) * 100
    if fuzzy_col_internal in df_filtered.columns:
        df_filtered["Score"] = df_filtered[fuzzy_col_internal]
    
    for col_round, decimals in [(coop_preis_col,2), (fp_preis_col,2), ("Diff_CHF",2), ("Diff_%",1)]:
        if col_round in df_filtered.columns: df_filtered[col_round] = df_filtered[col_round].round(decimals)
    if "Score" in df_filtered.columns: 
        df_filtered["Score"] = df_filtered["Score"].apply(lambda x: round(x,1) if x!=-1 else -1)
    if nps_fp_col in df_filtered.columns:
        df_filtered[nps_fp_col] = pd.to_numeric(df_filtered[nps_fp_col], errors='coerce').round(0).astype('Int64', errors='ignore')

    if coop_url_col in df_filtered.columns: df_filtered["Coop_URL_Link"] = df_filtered[coop_url_col].astype(str).apply(lambda x: x if pd.notna(x) and x.strip() not in ['','nan','None'] and x.startswith(('http://','https://')) else None)
    else: df_filtered["Coop_URL_Link"] = None
    if fp_sku_col in df_filtered.columns:
        def create_fp_url(norm_sku):
            if pd.notna(norm_sku) and str(norm_sku).strip(): return f"https://www.flaschenpost.ch/wein?search={str(norm_sku).strip()}"
            return None
        df_filtered["FP_URL_Link"] = df_filtered[fp_sku_col].apply(create_fp_url)
    else: df_filtered["FP_URL_Link"] = None
    df_display = df_filtered.copy()

    # --- Sidebar-Filter (Logik bleibt gleich, hier gekürzt) ---
    st.sidebar.subheader("Filter & Tabellenoptionen")
    filter_candidate_cols = (default_extra_columns or []) + [fp_lieferant_col, nps_fp_col]
    for col_name in filter_candidate_cols:
        if col_name in df_display.columns:
            if df_display[col_name].nunique() > 1 and df_display[col_name].nunique() < 50 and not pd.api.types.is_numeric_dtype(df_display[col_name]):
                unique_values=sorted(df_display[col_name].dropna().unique()); default_sel=unique_values if unique_values else []
                selected_values=st.sidebar.multiselect(f"{col_name.replace('_',' ')}",unique_values,default=default_sel,key=f"filter_{col_name}")
                if selected_values:df_display=df_display[df_display[col_name].isin(selected_values)]
            elif pd.api.types.is_numeric_dtype(df_display[col_name]) and df_display[col_name].notna().any():
                series_slider=df_display[col_name].dropna()
                if not series_slider.empty:
                    min_v,max_v=float(series_slider.min()),float(series_slider.max())
                    if min_v < max_v:
                        step_v=0.1 if pd.api.types.is_float_dtype(series_slider)and col_name not in [nps_fp_col,"Score"] else(0.1 if col_name=="Score" else 1.0)
                        if col_name==nps_fp_col and(max_v-min_v>100):step_v=10.0
                        if max_v-min_v>0 and max_v-min_v<step_v:step_v=max_v-min_v
                        sel_range=st.sidebar.slider(f"{col_name.replace('_',' ')}",min_v,max_v,(min_v,max_v),step=float(step_v),key=f"slider_{col_name}")
                        df_display=df_display[df_display[col_name].between(sel_range[0],sel_range[1])]
                    elif min_v==max_v:st.sidebar.caption(f"{col_name.replace('_',' ')}: Nur Wert {min_v}.")
    if "Score" in df_display.columns and pd.api.types.is_numeric_dtype(df_display["Score"])and df_display["Score"].notna().any():
        s_f=df_display["Score"].dropna();min_f,max_f=float(s_f.min()),float(s_f.max())
        if min_f<max_f:sel_f_r=st.sidebar.slider("Score Bereich",min_f,max_f,(min_f,max_f),0.1,key="s_f_spec");df_display=df_display[df_display["Score"].between(sel_f_r[0],sel_f_r[1])]
        elif min_f==max_f:st.sidebar.caption(f"Score: Nur {min_f}.")
    if"Diff_%"in df_display.columns and pd.api.types.is_numeric_dtype(df_display["Diff_%"])and df_display["Diff_%"].notna().any():
        s_p=df_display["Diff_%"].dropna();min_p,max_p=float(s_p.min()),float(s_p.max())
        if min_p<max_p:sel_p_r=st.sidebar.slider("Diff. (%)",min_p,max_p,(min_p,max_p),0.1,key="s_p_spec");df_display=df_display[df_display["Diff_%"].between(sel_p_r[0],sel_p_r[1])]
        elif min_p==max_p:st.sidebar.caption(f"Diff.(%): Nur {min_p}.")


    st.sidebar.markdown("---"); st.sidebar.subheader("Spaltenauswahl für Tabelle")
    core_columns = [coop_name_col, coop_produzent_col, "Coop_URL_Link", fp_name_col, fp_produzent_col, fp_sku_col, "FP_URL_Link", coop_preis_col, fp_preis_col, "Diff_CHF", "Diff_%", "Score", fp_lieferant_col, nps_fp_col]
    actual_default_extra = [c for c in (default_extra_columns or []) if c in df.columns and c not in core_columns]
    pot_disp_cols = core_columns + actual_default_extra
    exist_opts_multi = sorted(list(set(c for c in pot_disp_cols if c in df_display.columns)), key=lambda x: pot_disp_cols.index(x) if x in pot_disp_cols else float('inf'))
    def_sel_cols = [c for c in core_columns if c in df_display.columns] + [c for c in actual_default_extra if c in df_display.columns]
    def_sel_cols = sorted(list(set(def_sel_cols)), key=lambda x: (core_columns + actual_default_extra).index(x) if x in (core_columns + actual_default_extra) else float('inf'))
    selected_columns_for_table = st.sidebar.multiselect("Wähle Spalten:", options=exist_opts_multi, default=def_sel_cols, key="col_sel_sb")

    if df_display.empty: st.info("Nach Filtern: Keine Daten."); return
    if not selected_columns_for_table: st.warning("Spalten auswählen (Sidebar)."); return
    df_to_show = df_display[selected_columns_for_table].copy()

    # --- Top N & Sortierung (Logik bleibt gleich) ---
    col_sort, col_top_n = st.columns(2)
    with col_sort:
        sortable_cols_map = {"Diff_%":"Diff. (%)", "Diff_CHF":"Diff. (CHF)", "Score":"Score", nps_fp_col:"NPS FP"}
        sort_opts = [c for c in sortable_cols_map.keys() if c in df_to_show.columns]
        if not sort_opts and not df_to_show.empty: sort_opts = [c for c in df_to_show.columns if pd.api.types.is_numeric_dtype(df_to_show[c])]
        if sort_opts:
            sort_c = st.selectbox("Sortieren nach:",sort_opts,format_func=lambda x:sortable_cols_map.get(x,x.replace('_',' ')),key="sort_sel")
            sort_d = st.radio("Reihenfolge:",["Absteigend","Aufsteigend"],horizontal=True,key="sort_dir")
            asc = (sort_d=="Aufsteigend")
            if sort_c and sort_c in df_to_show.columns:
                try: df_to_show = df_to_show.sort_values(sort_c,ascending=asc,na_position='last')
                except TypeError: st.error(f"Sortierfehler bei '{sort_c}'.")
    with col_top_n:
        top_n_opt = st.selectbox("Schnellauswahl:",("Alle anzeigen","Top N Coop günstiger","Top N FP günstiger"),key="top_n_sel")
        temp_df_top_n = df_display[selected_columns_for_table].copy()
        if top_n_opt != "Alle anzeigen":
            max_n_s = len(temp_df_top_n)
            n_val_top = st.slider("Anzahl N:",1,int(np.minimum(max_n_s,200)),min(10,max_n_s)if max_n_s>0 else 1,1,key="n_val_top_s")
            if "Diff_%" in temp_df_top_n.columns:
                if top_n_opt=="Top N Coop günstiger":df_to_show=temp_df_top_n.nsmallest(n_val_top,"Diff_%")
                elif top_n_opt=="Top N FP günstiger":df_to_show=temp_df_top_n.nlargest(n_val_top,"Diff_%")
            else:st.warning("'Diff_%' für Top-N nicht da.")
    if top_n_opt == "Alle anzeigen":
        max_n_main_s = len(df_to_show)
        if max_n_main_s > 0:
            val_n,min_n=(min(25,max_n_main_s),min(10,max_n_main_s))if max_n_main_s>0 else(10,1)
            if val_n<min_n:val_n=min_n
            n_show_main=st.slider("Anz.Resultate:",min_n,int(np.minimum(max_n_main_s,1000)),val_n,10,key="main_n_s")
            if n_show_main<len(df_to_show):df_to_show=df_to_show.head(n_show_main)

    # --- 4. Tabelle anzeigen mit Styling und column_config ---
    st.markdown(f"**Angezeigte Matches: {len(df_to_show)}**")

    col_width_narrow = "80px"
    col_width_nps = "100px"
    col_width_standard = "medium"

    column_config = {
        coop_preis_col: st.column_config.NumberColumn(format="%.2f", width=col_width_narrow),
        fp_preis_col: st.column_config.NumberColumn(format="%.2f", width=col_width_narrow),
        "Diff_CHF": st.column_config.NumberColumn(format="%.2f", width=col_width_narrow),
        "Diff_%": st.column_config.NumberColumn(format="%.1f%%", width=col_width_narrow),
        "Score": st.column_config.NumberColumn(format="%.1f", width=col_width_narrow),
        fp_sku_col: st.column_config.TextColumn(width=col_width_narrow),
        nps_fp_col: st.column_config.NumberColumn("NPS FP", format="%.0f", width=col_width_nps),
    }
    if "Coop_URL_Link" in df_to_show.columns:
        column_config["Coop_URL_Link"] = st.column_config.LinkColumn("Coop URL", display_text="Link", width=col_width_narrow)
    if "FP_URL_Link" in df_to_show.columns:
        column_config["FP_URL_Link"] = st.column_config.LinkColumn("FP URL", display_text="Link", width=col_width_narrow)
    
    for col, display_name, width in [
        (coop_name_col, "Coop Name", col_width_standard),
        (fp_name_col, "FP Name", col_width_standard),
        (coop_produzent_col, "Coop Produzent", col_width_standard),
        (fp_produzent_col, "FP Produzent", col_width_standard),
        (fp_lieferant_col, "FP Lieferant", col_width_standard)
    ]:
        if col in df_to_show.columns:
            if pd.api.types.is_numeric_dtype(df_to_show[col]) and col not in column_config:
                 column_config[col] = st.column_config.NumberColumn(display_name.replace("_", " "), width=width)
            elif col not in column_config:
                 column_config[col] = st.column_config.TextColumn(display_name.replace("_", " "), width=width)

    def highlight_price_diff_enhanced(row):
        if "Diff_%" not in row.index: return [''] * len(row)
        val = row["Diff_%"]; color = ''
        if pd.isna(val) or not isinstance(val, (int, float)): return [''] * len(row)
        if val < -10: color = 'background-color: #c3e6cb; color: #155724;'
        elif val > 10: color = 'background-color: #f5c6cb; color: #721c24;'
        elif val < -2: color = 'background-color: #e2f0d9;'
        elif val > 2: color = 'background-color: #fce8e6;'
        return [color if col_name == "Diff_%" else '' for col_name in row.index]

    if not df_to_show.empty:
        st.dataframe(
            df_to_show.style.apply(highlight_price_diff_enhanced, axis=1),
            use_container_width=True, column_config=column_config, hide_index=True
        )
        @st.cache_data
        def convert_df_to_csv(df_export): return df_export.to_csv(index=False).encode("utf-8")
        csv_data = convert_df_to_csv(df_to_show)
        st.download_button("Aktuelle Tabelle als CSV", csv_data, "preisausreisser.csv", "text/csv", key="dl_btn")
    else: st.info("Keine Daten für die aktuelle Auswahl.")
    st.caption("Negative Preisdifferenz (%) = Coop günstiger. Positive Preisdifferenz (%) = Flaschenpost günstiger.")

# --- Beispielhafter Aufruf (bleibt gleich) ---
if __name__ == '__main__':
    num_samples = 50; np.random.seed(42)
    data_main = {'Coop_Name': [f'C-Wein Supertropfen {i}' for i in range(num_samples)], 'Coop_Produzent': [f'C-Winzer {chr(65+i%10)}' for i in range(num_samples)], 'FP_Name': [f'FP-Wein Edelschoppen {i}' for i in range(num_samples)], 'FP_Produzent': [f'FP-Winzer {chr(70+i%10)}' for i in range(num_samples)], 'Coop_Preis': np.random.uniform(5.123, 80.789, num_samples), 'FP_Preis': np.random.uniform(4.456, 75.912, num_samples)},
    data_main['Fuzzy_Score'] = np.random.uniform(40.12, 100.0, num_samples) # Angepasst
    data_main.update({'Coop_URL': [f'https://www.coop.ch/de/p/6.00{i:03d}' if i % 2 == 0 else None for i in range(num_samples)], 'FP_Sku': [f'sku{i*2}' if i%3 !=0 else np.nan for i in range(num_samples)], 'FP_Lieferant': [f'Lieferant {chr(80+i%5)}' if i%2==0 else np.nan for i in range(num_samples)], 'NPS_FP': np.random.uniform(100, 500000, num_samples), 'Match_Status': np.random.choice(['OK', 'Check', 'Neu'], num_samples), 'Coop_Weintyp': np.random.choice(['Rot', 'Weiss'], num_samples)})
    manual_indices = np.random.choice(num_samples, size=int(num_samples*0.1), replace=False); data_main['Fuzzy_Score'][manual_indices] = -1; data_main['Coop_URL'][num_samples-1] = "http://invalid-url"; data_main['FP_Sku'][num_samples-2] = ""
    sample_df_main = pd.DataFrame(data_main); sample_df_main.loc[sample_df_main.sample(frac=0.1).index, 'NPS_FP'] = np.nan
    example_extra_cols = ['Match_Status', 'Coop_Weintyp']
    plot_price_outlier_table_enhanced(sample_df_main, fuzzy_col_internal="Fuzzy_Score", default_extra_columns=example_extra_cols)


import streamlit as st
import pandas as pd
import plotly.express as px

def plot_matched_performance_analysis(
    df_enriched_matches: pd.DataFrame,
    nps_col: str = "NPS_FP",
    lieferant_col: str = "FP_Lieferant",
    fp_name_col: str = "FP_Name",
    coop_name_col: str = "Coop_Name",
    preis_diff_pct_col: str = "Diff_%", # Annahme, dass es so heißt nach der Umbenennung
    top_n_wines: int = 15,
    top_n_lieferanten: int = 10
):
    """
    Analysiert die Performance der gematchten Weine basierend auf Flaschenpost-Umsatz (NPS)
    und der Verteilung auf die Lieferanten.
    """
    st.subheader("Performance-Analyse der gematchten Weine (Basis: Flaschenpost)")
    st.markdown("Diese Analyse zeigt, welche gematchten Weine bei Flaschenpost besonders umsatzstark sind und welche Lieferanten einen großen Anteil an den Matches haben.")

    # Sicherstellen, dass die benötigten Spalten vorhanden und numerisch sind
    required_numeric_cols = [nps_col]
    for col in required_numeric_cols:
        if col not in df_enriched_matches.columns:
            st.warning(f"Benötigte Spalte '{col}' für die Performance-Analyse nicht gefunden. Überspringe Teile der Analyse.")
            return # Oder nur den Teil überspringen, der die Spalte braucht
        try:
            df_enriched_matches[col] = pd.to_numeric(df_enriched_matches[col], errors='coerce')
        except Exception as e:
            st.warning(f"Fehler bei Konvertierung der Spalte '{col}' zu numerisch: {e}. Überspringe Teile der Analyse.")
            return


    # --- 1. Top Gematchte Weine nach Flaschenpost-Umsatz (NPS_FP) ---
    st.markdown("#### Top Gematchte Weine nach Umsatz (Flaschenpost)")

    # Filtere auf Weine mit vorhandenem NPS
    df_wines_with_nps = df_enriched_matches[df_enriched_matches[nps_col].notna()].copy()

    if not df_wines_with_nps.empty:
        top_wines_by_nps = df_wines_with_nps.sort_values(by=nps_col, ascending=False).head(top_n_wines)
        
        # Spalten für die Anzeige auswählen
        cols_to_show_wines = [fp_name_col, coop_name_col, nps_col]
        if preis_diff_pct_col in top_wines_by_nps.columns:
            cols_to_show_wines.append(preis_diff_pct_col)
        
        # Sicherstellen, dass nur vorhandene Spalten ausgewählt werden
        cols_to_show_wines = [col for col in cols_to_show_wines if col in top_wines_by_nps.columns]

        if not cols_to_show_wines:
             st.info("Keine relevanten Spalten für die Top-Wein-Anzeige gefunden.")
        else:
            # Umbenennung für bessere Lesbarkeit in der Tabelle
            display_names_wines = {
                fp_name_col: "Flaschenpost Wein",
                coop_name_col: "Coop Pendant",
                nps_col: "Umsatz FP (NPS)",
                preis_diff_pct_col: "Preisdiff. (%)"
            }
            top_wines_display = top_wines_by_nps[cols_to_show_wines].rename(columns=display_names_wines)

            # Formatierung für die Tabelle
            column_config_wines = {
                "Umsatz FP (NPS)": st.column_config.NumberColumn(format="%.0f")
            }
            if "Preisdiff. (%)" in top_wines_display.columns:
                 column_config_wines["Preisdiff. (%)"] = st.column_config.NumberColumn(format="%.1f%%")


            st.dataframe(top_wines_display, use_container_width=True, hide_index=True, column_config=column_config_wines)
            st.caption(f"Zeigt die Top {top_n_wines} gematchten Weine, sortiert nach ihrem Nettoumsatz (Product Sales) bei Flaschenpost.")

            # Optional: Visualisierung als horizontales Balkendiagramm
            if fp_name_col in top_wines_by_nps.columns and nps_col in top_wines_by_nps.columns and len(top_wines_by_nps) > 1:
                try:
                    fig_top_wines = px.bar(
                        top_wines_by_nps.sort_values(by=nps_col, ascending=True), # Aufsteigend für horizontale Balken von unten nach oben
                        x=nps_col,
                        y=fp_name_col,
                        orientation='h',
                        title=f"Top {top_n_wines} gematchte Weine nach FP Umsatz",
                        labels={nps_col: "Nettoumsatz (NPS) bei FP", fp_name_col: "Flaschenpost Wein"},
                        height = max(400, top_n_wines * 35) # Dynamische Höhe
                    )
                    fig_top_wines.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig_top_wines, use_container_width=True)
                except Exception as e:
                    st.warning(f"Konnte Diagramm für Top-Weine nicht erstellen: {e}")

    else:
        st.info("Keine gematchten Weine mit Umsatzdaten (NPS) für diese Analyse gefunden.")

    st.markdown("---")

    # --- 2. Lieferanten-Analyse der gematchten Weine ---
    st.markdown("#### Lieferanten-Analyse der gematchten Weine (Basis: Flaschenpost)")

    if lieferant_col not in df_enriched_matches.columns or df_enriched_matches[lieferant_col].isna().all():
        st.info(f"Keine Lieferantendaten ('{lieferant_col}') in den gematchten Weinen gefunden oder alle Werte sind leer.")
    else:
        # Lieferanten nach Anzahl gematchter Weine
        lieferanten_by_match_count = df_enriched_matches[lieferant_col].value_counts().nlargest(top_n_lieferanten)
        if not lieferanten_by_match_count.empty:
            st.markdown("##### Top Lieferanten nach Anzahl gematchter Weine")
            try:
                fig_lieferant_count = px.bar(
                    lieferanten_by_match_count,
                    x=lieferanten_by_match_count.index,
                    y=lieferanten_by_match_count.values,
                    title=f"Top {top_n_lieferanten} Lieferanten (Anzahl Matches)",
                    labels={'x': 'Lieferant', 'y': 'Anzahl gematchter Weine'}
                )
                fig_lieferant_count.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_lieferant_count, use_container_width=True)
            except Exception as e:
                 st.warning(f"Konnte Diagramm für Lieferanten (Anzahl) nicht erstellen: {e}")

        else:
            st.write("Keine Daten für Lieferanten nach Anzahl Matches.")


        # Lieferanten nach summiertem NPS_FP der gematchten Weine
        if nps_col in df_enriched_matches.columns and df_enriched_matches[nps_col].notna().any():
            # Filtere auf Zeilen mit Lieferant UND NPS
            df_lieferant_nps = df_enriched_matches[
                df_enriched_matches[lieferant_col].notna() & df_enriched_matches[nps_col].notna()
            ]
            if not df_lieferant_nps.empty:
                lieferanten_by_nps_sum = df_lieferant_nps.groupby(lieferant_col)[nps_col].sum().nlargest(top_n_lieferanten)
                
                if not lieferanten_by_nps_sum.empty:
                    st.markdown("##### Top Lieferanten nach summiertem Umsatz (NPS) der gematchten Weine")
                    try:
                        fig_lieferant_nps = px.bar(
                            lieferanten_by_nps_sum,
                            x=lieferanten_by_nps_sum.index,
                            y=lieferanten_by_nps_sum.values,
                            title=f"Top {top_n_lieferanten} Lieferanten (Summe NPS gematchter Weine)",
                            labels={'x': 'Lieferant', 'y': 'Summe NPS gematchter Weine'}
                        )
                        fig_lieferant_nps.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig_lieferant_nps, use_container_width=True)
                    except Exception as e:
                        st.warning(f"Konnte Diagramm für Lieferanten (NPS) nicht erstellen: {e}")
                else:
                    st.write("Keine Daten für Lieferanten nach Umsatz (NPS).")
            else:
                 st.write("Keine Daten mit Lieferanten und NPS für die Umsatzanalyse pro Lieferant.")

        else:
            st.info(f"Spalte '{nps_col}' nicht vorhanden oder leer, daher keine Umsatzanalyse pro Lieferant möglich.")

# --- Beispielhafter Aufruf (ersetze dies mit deinem DataFrame) ---
if __name__ == '__main__':
    # Erstelle robustere Beispieldaten
    num_samples = 100
    np.random.seed(42)
    data = {
        'Coop_Name': [f'C-Wein XYZ {i}' for i in range(num_samples)],
        'FP_Name': [f'FP-Wein Alpha {i}' for i in range(num_samples)],
        'NPS_FP': np.random.choice([np.nan] + list(np.random.uniform(100, 50000, num_samples - 1)), num_samples, p=[0.1] + [0.9 / (num_samples - 1)] * (num_samples - 1)),
        'FP_Lieferant': np.random.choice([None, 'Lieferant A', 'Lieferant B', 'Lieferant C', 'Lieferant D', 'Lieferant E'], num_samples, p=[0.1, 0.2, 0.2, 0.2, 0.15, 0.15]),
        'Diff_%': np.random.uniform(-20, 20, num_samples).round(1),
        'Fuzzy_Score': np.random.uniform(50,100,num_samples) # Nur als Beispiel, wird hier nicht direkt verwendet
    }
    sample_df = pd.DataFrame(data)

    st.title("Demo: Performance-Analyse gematchter Weine")
    plot_matched_performance_analysis(sample_df)

    st.subheader("Test mit fehlender NPS-Spalte")
    plot_matched_performance_analysis(sample_df.drop(columns=['NPS_FP']))

    st.subheader("Test mit fehlender Lieferanten-Spalte")
    plot_matched_performance_analysis(sample_df.drop(columns=['FP_Lieferant']))



import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np # Für den Beispielaufruf

def plot_sweet_spot_analysis(
    df_enriched_matches: pd.DataFrame,
    nps_col: str = "NPS_FP",
    preis_diff_pct_col: str = "Diff_%",
    score_col: str = "Score",
    fp_name_col: str = "FP_Name",
    coop_name_col: str = "Coop_Name",
    fp_preis_col: str = "FP_Preis",
    coop_preis_col: str = "Coop_Preis"
):
    """
    Identifiziert und visualisiert "Sweet Spots" (Coop teurer, FP hoher Umsatz)
    und "Pricing Opportunities" (FP teurer, FP hoher Umsatz).
    Erwartet, dass die Spalten 'Diff_%' und 'Score' im DataFrame vorhanden sind.
    """
    st.subheader("Sweet Spot & Pricing Opportunity Analyse")
    st.markdown("""
    Diese Analyse hilft, Weine zu identifizieren, bei denen Flaschenpost einen deutlichen Preisvorteil gegenüber Coop hat
    und gleichzeitig einen hohen Umsatz erzielt (Sweet Spots), sowie Weine, bei denen Flaschenpost trotz höherer Preise
    gut verkauft (Pricing Power / Opportunities).
    """)

    required_cols = [nps_col, preis_diff_pct_col, score_col]
    if not all(col in df_enriched_matches.columns for col in required_cols):
        missing_cols = [col for col in required_cols if col not in df_enriched_matches.columns]
        st.warning(f"Benötigte Spalten {missing_cols} nicht im DataFrame für Sweet-Spot-Analyse gefunden. Analyse wird übersprungen.")
        return
        
    for col in [nps_col, preis_diff_pct_col, score_col]:
        if not pd.api.types.is_numeric_dtype(df_enriched_matches[col]):
            try: df_enriched_matches[col] = pd.to_numeric(df_enriched_matches[col], errors='coerce')
            except Exception : st.warning(f"Fehler bei Konvertierung '{col}'."); return # f-string
    
    df_analysis = df_enriched_matches[df_enriched_matches[nps_col].notna() & df_enriched_matches[preis_diff_pct_col].notna()].copy()
    if df_analysis.empty: st.info("Keine Daten für Sweet-Spot-Analyse."); return # Kurze Meldung

    st.sidebar.subheader("Sweet Spot Filter")
    # Slider-Logik (robustere Default- und Step-Berechnung)
    min_nps, max_nps = (float(df_analysis[nps_col].min()), float(df_analysis[nps_col].max())) if df_analysis[nps_col].notna().any() else (0.0, 1000.0)
    default_nps_val = float(df_analysis[nps_col].quantile(0.75)) if min_nps < max_nps and df_analysis[nps_col].notna().any() else min_nps
    step_nps = float(max(1.0, (max_nps - min_nps) / 100 if (max_nps - min_nps) > 0 else 1.0))
    if min_nps >= max_nps: # Fallback, falls min >= max (z.B. nur ein Wert oder keine Daten)
        min_nps = 0.0
        max_nps = default_nps_val + step_nps * 10 if default_nps_val is not None else 100.0
        if max_nps <= min_nps: max_nps = min_nps + step_nps

    nps_threshold = st.sidebar.slider("Mindestumsatz (NPS) FP:", min_nps, max_nps, default_nps_val, step_nps, key="nps_sw")
    coop_teurer_threshold_pct = st.sidebar.slider("Coop mind. X% teurer:",0,100,10,1,"%d%%",key="coop_t_sw")
    fp_teurer_threshold_pct = st.sidebar.slider("FP mind. Y% teurer:",0,100,10,1,"%d%%",key="fp_t_sw")

    df_sweet_spots = df_analysis[(df_analysis[preis_diff_pct_col]<=-coop_teurer_threshold_pct)&(df_analysis[nps_col]>=nps_threshold)]
    df_pricing_opportunities = df_analysis[(df_analysis[preis_diff_pct_col]>=fp_teurer_threshold_pct)&(df_analysis[nps_col]>=nps_threshold)]

    st.markdown("#### Interaktives Streudiagramm: Preisdifferenz vs. Flaschenpost Umsatz")
    df_analysis['Analyse_Kategorie'] = 'Andere'
    df_analysis.loc[df_sweet_spots.index,'Analyse_Kategorie'] = 'Sweet Spot (Coop teurer)'
    df_analysis.loc[df_pricing_opportunities.index,'Analyse_Kategorie'] = 'Pricing Opportunity (FP teurer)'
    
    hover_data_cols = [fp_name_col, coop_name_col, nps_col, preis_diff_pct_col, score_col]
    hover_data_cols = [c for c in hover_data_cols if c in df_analysis.columns]

    fig_scatter = px.scatter(df_analysis,x=preis_diff_pct_col,y=nps_col,color='Analyse_Kategorie',size=nps_col,size_max=30,
        hover_name=fp_name_col if fp_name_col in df_analysis.columns else None, hover_data={c:True for c in hover_data_cols},
        color_discrete_map={'Sweet Spot (Coop teurer)':'#28a745','Pricing Opportunity (FP teurer)':'#ffc107','Andere':'#adb5bd'}, # Angepasste Farben
        labels={preis_diff_pct_col:"Preisdifferenz Coop vs. FP (%) <br> (Negativ = Coop teurer)",nps_col:"Umsatz (NPS) bei Flaschenpost",'Analyse_Kategorie':"Kategorie"},
        title="Preis-Performance Matrix")
    fig_scatter.add_vline(x=-coop_teurer_threshold_pct,line_dash="dash",line_color="#28a745",annotation_text="Sweet Spot Grenze")
    fig_scatter.add_vline(x=fp_teurer_threshold_pct,line_dash="dash",line_color="#ffc107",annotation_text="Opportunity Grenze")
    fig_scatter.add_hline(y=nps_threshold,line_dash="dash",line_color="#007bff",annotation_text="Hoher Umsatz Grenze") # Blau für Umsatz
    fig_scatter.update_layout(height=600, legend_title_text='Analysezonen') 
    st.plotly_chart(fig_scatter,use_container_width=True)

    # --- HIER WIRD DIE ERKLÄRUNG EINGEFÜGT ---
    st.markdown("---") 
    st.subheader("💡 So interpretieren Sie dieses Diagramm:")
    st.markdown("""
    Dieses Diagramm visualisiert die Preis-Performance gematchter Weine im Vergleich zwischen Flaschenpost und Coop, relativ zu ihrem Umsatz (NPS) bei Flaschenpost. Jeder Punkt repräsentiert einen spezifischen Wein.

    **Achsen und Punktgröße:**
    *   **Horizontale Achse (X):** Zeigt die prozentuale Preisdifferenz. Negative Werte (links von Null) bedeuten, dass Coop für diesen Wein teurer ist als Flaschenpost. Positive Werte (rechts) bedeuten, dass Flaschenpost teurer ist.
    *   **Vertikale Achse (Y):** Stellt den bei Flaschenpost generierten Nettoumsatz (NPS) des Weins dar. Je höher ein Punkt, desto umsatzstärker ist der Wein bei uns.
    *   **Größe der Punkte:** Die Fläche der Punkte ist ebenfalls proportional zum Flaschenpost-Umsatz (NPS) des Weins.

    **Strategische Zonen (definiert durch die gestrichelten Linien):**
    Die farbigen Linien teilen das Diagramm in Sektoren, basierend auf den Schwellenwerten, die Sie in der Sidebar für "hohen Umsatz" und "signifikante Preisdifferenz" einstellen können:

    1.  🟢 **Sweet Spots (Grün – typischerweise oben links):**
        *   **Definition:** Weine, bei denen Coop *deutlich teurer* ist als Flaschenpost UND die bei Flaschenpost einen *hohen Umsatz* erzielen.
        *   **Bedeutung:** Hier haben wir einen starken Preisvorteil bei gut laufenden Produkten.
        *   **Mögliche Überlegungen:** Diese Preispositionierung beibehalten oder im Marketing hervorheben.

    2.  🟠 **Pricing Opportunities (Orange – typischerweise oben rechts):**
        *   **Definition:** Weine, bei denen Flaschenpost *deutlich teurer* ist als Coop, die aber dennoch einen *hohen Umsatz* bei uns generieren.
        *   **Bedeutung:** Dies kann auf eine hohe Kundenakzeptanz unseres Preises, Markenstärke, bessere Verfügbarkeit oder andere Servicevorteile hindeuten. Es zeigt potenziell vorhandene "Pricing Power".
        *   **Mögliche Überlegungen:** Analyse, ob der Preis optimal ist, ob ein Risiko der Kundenabwanderung zu Coop besteht oder ob der Mehrwert, den wir bieten, den Preis rechtfertigt.

    3.  ⚪ **Andere (Grau – restliche Bereiche):**
        *   **Definition:** Weine, die entweder einen geringeren Umsatz bei Flaschenpost erzielen oder deren Preisdifferenz zu Coop unterhalb der von Ihnen definierten "deutlichen" Schwellenwerte liegt.
        *   **Mögliche Überlegungen:** Diese Weine bilden das Gros des Sortiments. Einzelne Ausreißer hier können über die "Outlier-Tabelle" genauer untersucht werden.

    **Interaktive Anwendung:**
    *   **Tooltips:** Fahren Sie mit der Maus über einzelne Punkte, um Detailinformationen zum jeweiligen Wein (Name, genaue Preisdifferenz, Umsatz, Score) zu erhalten.
    *   **Sidebar-Filter:** Passen Sie die Schwellenwerte für Umsatz und Preisdifferenz an, um zu sehen, wie sich die Verteilung der Weine auf die strategischen Zonen verändert.
    *   **Detailtabellen:** Die Tabellen unterhalb dieses Diagramms listen die spezifischen Weine auf, die aktuell in die "Sweet Spot"- und "Pricing Opportunity"-Kategorien fallen.
    """)
    st.markdown("---")
    
    cols_to_show_table = [fp_name_col,coop_name_col,fp_preis_col,coop_preis_col,preis_diff_pct_col,nps_col,score_col]
    cols_to_show_table = [c for c in cols_to_show_table if c in df_analysis.columns]
    
    column_config_table = {
        nps_col: st.column_config.NumberColumn("NPS FP", format="%.0f"),
        preis_diff_pct_col: st.column_config.NumberColumn("Diff. (%)", format="%.1f%%"),
        fp_preis_col: st.column_config.NumberColumn("FP Preis", format="%.2f"),
        coop_preis_col: st.column_config.NumberColumn("Coop Preis", format="%.2f"),
    }
    # Score-Spalte nur hinzufügen, wenn sie existiert und ausgewählt wurde
    if score_col in cols_to_show_table:
         column_config_table[score_col] = st.column_config.NumberColumn("Score", format="%.1f")
    
    st.markdown(f"#### Sweet Spots (Coop mind. {coop_teurer_threshold_pct}% teurer, FP NPS ≥ {nps_threshold:.0f})")
    if not df_sweet_spots.empty and cols_to_show_table: 
        st.dataframe(df_sweet_spots[cols_to_show_table].sort_values(by=nps_col,ascending=False),hide_index=True,use_container_width=True,column_config=column_config_table)
    else: st.info("Keine Sweet Spots mit aktuellen Filtern.")
    
    st.markdown(f"#### Pricing Opportunities (FP mind. {fp_teurer_threshold_pct}% teurer, FP NPS ≥ {nps_threshold:.0f})")
    if not df_pricing_opportunities.empty and cols_to_show_table: 
        st.dataframe(df_pricing_opportunities[cols_to_show_table].sort_values(by=nps_col,ascending=False),hide_index=True,use_container_width=True,column_config=column_config_table)
    else: st.info("Keine Pricing Opportunities mit aktuellen Filtern.")

# --- Beispielhafter Aufruf (bleibt gleich) ---
if __name__ == '__main__':
    num_samples = 150; np.random.seed(43)
    data = {'Coop_Name': [f'C-Wein Nr. {i}' for i in range(num_samples)], 'FP_Name': [f'FP-Wein Nr. {i}' for i in range(num_samples)], 'NPS_FP': np.random.gamma(2, 7000, num_samples).round(0), 'FP_Preis': np.random.uniform(5, 50, num_samples).round(2)}
    data['Diff_%'] = np.random.normal(0, 15, num_samples).round(1)
    data['Score'] = np.random.uniform(70,100, num_samples).round(1)
    data['Coop_Preis'] = data['FP_Preis'] * (1 + data['Diff_%'] / 100)
    sample_df = pd.DataFrame(data); sample_df['Coop_Preis'] = sample_df['Coop_Preis'].round(2)
    st.title("Demo: Sweet Spot Analyse")
    plot_sweet_spot_analysis(sample_df)



# plot_utils.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np # Kann für einige Plotly-Funktionen oder Berechnungen nützlich sein



# ==============================================================================
# Funktion für GAP-Analyse Tabelle (angepasst mit Match-Status und return df_gaps)
# ==============================================================================
def plot_gap_analysis_table(
    df_coop_full: pd.DataFrame,
    df_matching: pd.DataFrame,
    coop_id_col_in_coop_df: str = "URL",
    coop_id_col_in_matching_df: str = "Coop_URL",
    match_status_col_in_matching_df: str = "Match_Status",
    non_match_status_value: str = "Kein Match",
    valid_match_statuses: list = None, # Vorerst nicht verwendet, aber als Option behalten
    gap_display_columns: list = None
):
    st.subheader("Identifizierte Sortimentslücken (Coop-Weine nicht bei Flaschenpost)")

    if coop_id_col_in_coop_df not in df_coop_full.columns:
        st.error(f"ID-Spalte '{coop_id_col_in_coop_df}' nicht in Coop-Daten. Verfügbar: {df_coop_full.columns.tolist()}")
        return pd.DataFrame() # Wichtig: DataFrame zurückgeben im Fehlerfall
    if coop_id_col_in_matching_df not in df_matching.columns:
        st.error(f"ID-Spalte (Coop) '{coop_id_col_in_matching_df}' nicht in Matching-Daten. Verfügbar: {df_matching.columns.tolist()}")
        return pd.DataFrame()
    if match_status_col_in_matching_df not in df_matching.columns:
        st.error(f"Match-Status-Spalte '{match_status_col_in_matching_df}' nicht in Matching-Daten. Verfügbar: {df_matching.columns.tolist()}")
        return pd.DataFrame()

    df_gaps = pd.DataFrame() # Initialisieren für den Fall, dass try fehlschlägt
    try:
        if valid_match_statuses:
            df_echte_matches = df_matching[df_matching[match_status_col_in_matching_df].isin(valid_match_statuses)]
        else:
            df_echte_matches = df_matching[df_matching[match_status_col_in_matching_df] != non_match_status_value]
        
        matched_coop_ids = df_echte_matches[coop_id_col_in_matching_df].astype(str).str.strip().dropna().unique()
        
        df_coop_full_temp = df_coop_full.copy()
        df_coop_full_temp['temp_join_key_coop'] = df_coop_full_temp[coop_id_col_in_coop_df].astype(str).str.strip()
        
        df_gaps = df_coop_full_temp[~df_coop_full_temp['temp_join_key_coop'].isin(matched_coop_ids)].copy()
        df_gaps.drop(columns=['temp_join_key_coop'], inplace=True, errors='ignore')

    except Exception as e:
        st.error(f"Fehler bei der Identifizierung der Gaps: {e}")
        import traceback
        st.error(traceback.format_exc())
        return pd.DataFrame() # Wichtig: DataFrame zurückgeben im Fehlerfall

    num_coop_total = len(df_coop_full)
    num_distinct_echte_matches_coop_products = len(matched_coop_ids)
    num_gaps = len(df_gaps)
    
    # Debug-Zeile kann hier bei Bedarf wieder aktiviert/entfernt werden
    # st.write(f"Debug: Coop Total={num_coop_total}, Coop-Produkte mit echtem Match bei FP={num_distinct_echte_matches_coop_products}, Berechnete Gaps={num_gaps}")

    st.markdown("#### Quantitative Übersicht der Lücken:")
    col1, col2, col3 = st.columns(3)
    col1.metric("Coop-Sortiment (Gesamt SKUs)", num_coop_total)
    col2.metric("Davon bei FP gematcht (Coop SKUs)", num_distinct_echte_matches_coop_products)
    col3.metric("Sortimentslücken (Coop-SKUs nicht bei FP)", num_gaps,
                delta=f"{-((num_gaps / num_coop_total) * 100 if num_coop_total > 0 else 0):.1f}% Abdeckungslücke",
                delta_color="inverse" if num_gaps > 0 else "normal")

    if df_gaps.empty:
        st.success("Sehr gut! Aktuell wurden keine Sortimentslücken im Coop-Sortiment identifiziert (basierend auf den als 'gematcht' markierten Einträgen).")
        return pd.DataFrame() # <<< Gib ein leeres DataFrame zurück

    st.markdown("---")
    st.markdown("#### Detailtabelle der Sortimentslücken:")
    
    df_gaps_display = df_gaps.copy()

    preis_col_name_coop = "Preis"
    if preis_col_name_coop in df_gaps_display.columns and pd.api.types.is_numeric_dtype(df_gaps_display[preis_col_name_coop]):
        try:
            # Sicherstellen, dass min und max unterschiedlich sind, um Fehler im Slider zu vermeiden
            min_val = float(df_gaps_display[preis_col_name_coop].min())
            max_val = float(df_gaps_display[preis_col_name_coop].max())
            if min_val < max_val:
                selected_preis_range = st.slider(
                    "Filter nach Coop-Preis der Lücken:",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, max_val),
                    key="gap_preis_filter_slider"
                )
                df_gaps_display = df_gaps_display[df_gaps_display[preis_col_name_coop].between(selected_preis_range[0], selected_preis_range[1])]
            elif min_val == max_val: # Falls alle Preise gleich sind, keinen Slider anzeigen oder Hinweis geben
                 st.caption(f"Alle Lücken haben denselben Preis: {min_val:.2f} CHF.")
            else: # Sollte nicht passieren, wenn Daten vorhanden sind
                 st.caption("Keine Preisdaten für Filterung verfügbar.")
        except Exception as e:
            st.warning(f"Konnte Preisfilter für Gaps nicht erstellen: {e}")

    weintyp_col_name_coop = "Weintyp"
    if weintyp_col_name_coop in df_gaps_display.columns:
        unique_weintypen_gap = sorted(df_gaps_display[weintyp_col_name_coop].dropna().unique())
        if unique_weintypen_gap:
            selected_weintyp_gap = st.multiselect(
                "Filter nach Coop-Weintyp der Lücken:",
                options=unique_weintypen_gap,
                default=[],
                key="gap_weintyp_filter_multiselect"
            )
            if selected_weintyp_gap:
                df_gaps_display = df_gaps_display[df_gaps_display[weintyp_col_name_coop].isin(selected_weintyp_gap)]

    if gap_display_columns is None:
        default_cols = ["Name", "Produzent", preis_col_name_coop, weintyp_col_name_coop, "Region", "URL"]
        gap_display_columns_final = [col for col in default_cols if col in df_gaps_display.columns]
    else:
        gap_display_columns_final = [col for col in gap_display_columns if col in df_gaps_display.columns]

    if not gap_display_columns_final:
        st.warning("Keine Spalten für Gap-Tabelle definiert.")
        return df_gaps # Gib die ungefilterten Gaps zurück, wenn keine Anzeigespalten da sind

    gap_column_config = {}
    if preis_col_name_coop in gap_display_columns_final:
        gap_column_config[preis_col_name_coop] = st.column_config.NumberColumn("Coop Preis", format="CHF %.2f")
    if "URL" in gap_display_columns_final:
        gap_column_config["URL"] = st.column_config.LinkColumn("Coop Link", display_text="Zum Wein", width="small")

    st.dataframe(
        df_gaps_display[gap_display_columns_final],
        use_container_width=True,
        hide_index=True,
        column_config=gap_column_config
    )
    st.caption(f"Zeigt {len(df_gaps_display)} von {num_gaps} Sortimentslücken basierend auf den aktuellen Filtern.")
    
    return df_gaps # <<< Gib das DataFrame mit den Gaps zurück

# ==============================================================================
# Platzhalter für weitere Plot-Funktionen aus deinem Projekt (z.B. für Matching-Tab)
# plot_matching_overview_gemini(...)
# plot_percent_price_comparison_gemini1(...)
# plot_price_outlier_table_enhanced(...)
# plot_matched_performance_analysis(...)
# plot_sweet_spot_analysis(...)
# ==============================================================================

# Beispielhafter __main__ Block, falls du plot_utils.py direkt testen möchtest
if __name__ == '__main__':
    # Hier könntest du Testdaten erstellen und deine Plot-Funktionen aufrufen
    # Beispiel für plot_weintypen_pie_and_table:
    sample_data = {
        "Weintyp": ["Rotwein", "Rotwein", "Weisswein", "Roséwein", "Rotwein", "Schaumwein", "Weisswein"]
    }
    sample_df = pd.DataFrame(sample_data)
    st.title("Test: plot_weintypen_pie_and_table")
    plot_weintypen_pie_and_table(sample_df, titel="Test Verteilung Weintypen")

    # Beispiel für plot_gap_analysis_table (erfordert mehr Testdaten)
    # ...


# plot_utils.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go # Für Balkendiagramme
import numpy as np

# ==============================================================================
# Funktion für Weintyp-Vergleich Gaps vs. Coop-Gesamt (ANGEPASST mit Erklärung und Schwelle)
# ==============================================================================
def plot_gaps_weintyp_comparison(
    df_gaps: pd.DataFrame,
    df_coop_original: pd.DataFrame,
    weintyp_col: str = "Weintyp",
    titel: str = "Vergleich: Weintyp-Verteilung der Lücken vs. Coop-Gesamtsortiment"
):
    st.subheader(titel)

    # --- NEU: Erklärungstext ---
    st.markdown("""
    Diese Analyse vergleicht die prozentuale Verteilung der Weintypen innerhalb der **Sortimentslücken** 
    (Coop-Weine, die Flaschenpost nicht führt) mit der Verteilung im **Coop-Gesamtsortiment**. 
    Ziel ist es aufzuzeigen, ob bestimmte Weintypen bei den Lücken über- oder unterrepräsentiert sind.

    *   Eine **positive Differenz** bedeutet, dass der betreffende Weintyp bei den Lücken einen höheren Anteil hat als im Coop-Gesamtsortiment (d.h., dieser Weintyp fehlt bei Flaschenpost im Verhältnis häufiger).
    *   Eine **negative Differenz** zeigt, dass der Weintyp bei den Lücken einen geringeren Anteil hat (d.h., dieser Weintyp fehlt bei Flaschenpost im Verhältnis seltener).

    Dies kann Hinweise darauf geben, ob Flaschenpost bei bestimmten Weintypen systematisch ein anderes Angebot hat als Coop oder wo spezifische Abdeckungslücken bestehen.
    """)
    st.markdown("---") # Trennlinie

    order = ["Rotwein", "Weisswein", "Roséwein", "Schaumwein"]
    if df_gaps.empty: st.info("Keine Sortimentslücken vorhanden, daher kein Vergleich möglich."); return
        
    gaps_counts = df_gaps[weintyp_col].value_counts().reindex(order, fill_value=0)
    gaps_total = gaps_counts.sum(); gaps_percent = (gaps_counts / gaps_total * 100) if gaps_total > 0 else pd.Series([0.0]*len(order), index=order)
    coop_counts = df_coop_original[weintyp_col].value_counts().reindex(order, fill_value=0)
    coop_total = coop_counts.sum(); coop_percent = (coop_counts / coop_total * 100) if coop_total > 0 else pd.Series([0.0]*len(order), index=order)

    comparison_df = pd.DataFrame({
        "Weintyp": order, "Anteil Lücken (%)": gaps_percent.values.round(1),
        "Anteil Coop-Gesamt (%)": coop_percent.values.round(1)
    })
    comparison_df["Differenz (Lücken - Coop) (%)"] = (comparison_df["Anteil Lücken (%)"] - comparison_df["Anteil Coop-Gesamt (%)"]).round(1)

    col_table, col_chart = st.columns([0.55, 0.45]) 

    with col_table:
        st.write("Vergleich der prozentualen Anteile:")
        st.dataframe(comparison_df, hide_index=True, use_container_width=True,
                       column_config={"Anteil Lücken (%)": st.column_config.NumberColumn(format="%.1f%%"),
                                      "Anteil Coop-Gesamt (%)": st.column_config.NumberColumn(format="%.1f%%"),
                                      "Differenz (Lücken - Coop) (%)": st.column_config.NumberColumn(format="%.1f%%")})
    with col_chart:
        fig_diff = go.Figure()
        fig_diff.add_trace(go.Bar(
            x=comparison_df["Weintyp"], y=comparison_df["Differenz (Lücken - Coop) (%)"],
            marker_color=['crimson' if x < 0 else 'mediumseagreen' for x in comparison_df["Differenz (Lücken - Coop) (%)"]],
            text=comparison_df["Differenz (Lücken - Coop) (%)"].apply(lambda x: f"{x:.1f}%P"),
            textposition='auto'
        ))
        fig_diff.update_layout(title_text="Abweichung Lücken vs. Coop-Gesamt", yaxis_title="Differenz in Prozentpunkten",
                               height=380, margin=dict(t=30, b=10))
        st.plotly_chart(fig_diff, use_container_width=True)

    # --- ANGEPASSTE Interpretation mit Schwelle ---
    interpretation_threshold = 3.0 # Prozentpunkte als Schwelle für "signifikant"
    max_ueberrep = comparison_df.loc[comparison_df["Differenz (Lücken - Coop) (%)"].idxmax()]
    max_unterrep = comparison_df.loc[comparison_df["Differenz (Lücken - Coop) (%)"].idxmin()]
    
    significant_findings = []
    if max_ueberrep["Differenz (Lücken - Coop) (%)"] >= interpretation_threshold:
        significant_findings.append(
            f"**{max_ueberrep['Weintyp']}** sind bei den Sortimentslücken um "
            f"**{max_ueberrep['Differenz (Lücken - Coop) (%)']:.1f} Prozentpunkte überrepräsentiert** "
            f"im Vergleich zum Coop-Gesamtsortiment"
        )
    if max_unterrep["Differenz (Lücken - Coop) (%)"] <= -interpretation_threshold:
         significant_findings.append(
            f"**{max_unterrep['Weintyp']}** sind bei den Sortimentslücken um "
            f"**{abs(max_unterrep['Differenz (Lücken - Coop) (%)']):.1f} Prozentpunkte unterrepräsentiert** "
            f"im Vergleich zum Coop-Gesamtsortiment"
        )
    
    st.markdown("##### Kurzeinschätzung:")
    if significant_findings:
        for finding in significant_findings:
            st.markdown(f"- {finding}")
    else:
        st.markdown("Die Weintyp-Verteilung der Sortimentslücken weicht nur geringfügig von der Verteilung im Coop-Gesamtsortiment ab (Abweichungen unter +/- " + str(interpretation_threshold) + " Prozentpunkten).")



# ==============================================================================
# NEUE Funktion für Preisklassen-Vergleich Gaps vs. Coop-Gesamt
# ==============================================================================
def plot_gaps_preisklassen_comparison(
    df_gaps: pd.DataFrame,
    df_coop_original: pd.DataFrame,
    preis_col: str = "Preis", # Name der Preisspalte in beiden DataFrames
    bins = None, # Bins werden dynamisch oder von außen gesetzt
    labels = None, # Labels müssen zu den Bins passen
    titel: str = "Vergleich: Preisklassen-Verteilung der Lücken vs. Coop-Gesamtsortiment"
):
    st.subheader(titel)

    # --- Erklärungstext ---
    st.markdown("""
    Diese Analyse vergleicht die prozentuale Verteilung der Preisklassen (basierend auf Coop-Preisen) 
    innerhalb der **Sortimentslücken** mit der Verteilung im **Coop-Gesamtsortiment**.
    Ziel ist es aufzuzeigen, ob Lücken in bestimmten Preissegmenten über- oder unterrepräsentiert sind.

    *   Eine **positive Differenz** bedeutet, dass die betreffende Preisklasse bei den Lücken einen höheren Anteil hat.
    *   Eine **negative Differenz** zeigt, dass die Preisklasse bei den Lücken einen geringeren Anteil hat.
    """)
    st.markdown("---")

    if df_gaps.empty:
        st.info("Keine Sortimentslücken vorhanden, daher kein Preisklassen-Vergleich möglich.")
        return

    # Standard-Bins und Labels, falls nicht übergeben (ggf. anpassen)
    if bins is None:
        max_preis_gaps = df_gaps[preis_col].max() if not df_gaps.empty else 100 # Max-Preis aus Gaps für dynamische Bins
        max_preis_coop = df_coop_original[preis_col].max() if not df_coop_original.empty else 100
        overall_max_preis = max(max_preis_gaps, max_preis_coop, 101) # Sicherstellen, dass max > 100 ist für letztes Label

        bins = [0, 20, 50, 100, overall_max_preis]
    
    if labels is None:
        # Labels dynamisch an Bins anpassen (vereinfacht)
        labels = []
        for i in range(len(bins) -1):
            if i == len(bins) - 2: # Letztes Label
                labels.append(f"{int(bins[i])}+ CHF")
            else:
                labels.append(f"{int(bins[i])}–{int(bins[i+1])} CHF")

    # Funktion zur Berechnung der Preisklassenverteilung
    def get_preisklassen_verteilung(df_input, col_name, current_bins, current_labels):
        df_temp = df_input.copy()
        df_temp["Preisklasse"] = pd.cut(df_temp[col_name], bins=current_bins, labels=current_labels, include_lowest=True, right=False) # right=False für [0-20), [20-50) etc.
        counts = df_temp["Preisklasse"].value_counts().reindex(current_labels, fill_value=0)
        total = counts.sum()
        percent = (counts / total * 100) if total > 0 else pd.Series([0.0]*len(current_labels), index=current_labels)
        return counts, percent

    # 1. Verteilung für Gaps
    gaps_counts, gaps_percent = get_preisklassen_verteilung(df_gaps, preis_col, bins, labels)

    # 2. Verteilung für Coop-Gesamtsortiment
    coop_counts, coop_percent = get_preisklassen_verteilung(df_coop_original, preis_col, bins, labels)

    # 3. DataFrame für Vergleichstabelle und Plot
    comparison_df = pd.DataFrame({
        "Preisklasse": labels,
        "Anteil Lücken (%)": gaps_percent.values.round(1),
        "Anteil Coop-Gesamt (%)": coop_percent.values.round(1)
    })
    comparison_df["Differenz (Lücken - Coop) (%)"] = (comparison_df["Anteil Lücken (%)"] - comparison_df["Anteil Coop-Gesamt (%)"]).round(1)

    # Layout mit Spalten
    col_table, col_chart = st.columns([0.55, 0.45])

    with col_table:
        st.write("Vergleich der prozentualen Anteile nach Preisklasse:")
        st.dataframe(
            comparison_df, hide_index=True, use_container_width=True,
            column_config={
                "Anteil Lücken (%)": st.column_config.NumberColumn(format="%.1f%%"),
                "Anteil Coop-Gesamt (%)": st.column_config.NumberColumn(format="%.1f%%"),
                "Differenz (Lücken - Coop) (%)": st.column_config.NumberColumn(format="%.1f%%")
            }
        )
    with col_chart:
        fig_diff = go.Figure()
        fig_diff.add_trace(go.Bar(
            x=comparison_df["Preisklasse"],
            y=comparison_df["Differenz (Lücken - Coop) (%)"],
            marker_color=['crimson' if x < 0 else 'mediumseagreen' for x in comparison_df["Differenz (Lücken - Coop) (%)"]],
            text=comparison_df["Differenz (Lücken - Coop) (%)"].apply(lambda x: f"{x:.1f}%P"),
            textposition='auto'
        ))
        fig_diff.update_layout(
            title_text="Abweichung Lücken vs. Coop-Gesamt (Anteil Preisklasse)",
            yaxis_title="Differenz in Prozentpunkten",
            height=380, margin=dict(t=30, b=10)
        )
        st.plotly_chart(fig_diff, use_container_width=True)

    # Interpretation
    interpretation_threshold = 5.0 # Prozentpunkte, etwas höher für Preisklassen ggf. sinnvoll
    max_ueberrep = comparison_df.loc[comparison_df["Differenz (Lücken - Coop) (%)"].idxmax()]
    max_unterrep = comparison_df.loc[comparison_df["Differenz (Lücken - Coop) (%)"].idxmin()]
    
    significant_findings = []
    if max_ueberrep["Differenz (Lücken - Coop) (%)"] >= interpretation_threshold:
        significant_findings.append(
            f"Die Preisklasse **{max_ueberrep['Preisklasse']}** ist bei den Sortimentslücken um "
            f"**{max_ueberrep['Differenz (Lücken - Coop) (%)']:.1f} Prozentpunkte überrepräsentiert**"
        )
    if max_unterrep["Differenz (Lücken - Coop) (%)"] <= -interpretation_threshold:
         significant_findings.append(
            f"Die Preisklasse **{max_unterrep['Preisklasse']}** ist bei den Sortimentslücken um "
            f"**{abs(max_unterrep['Differenz (Lücken - Coop) (%)']):.1f} Prozentpunkte unterrepräsentiert**"
        )
    
    st.markdown("##### Kurzeinschätzung:")
    if significant_findings:
        for finding in significant_findings:
            st.markdown(f"- {finding}")
    else:
        st.markdown("Die Preisklassen-Verteilung der Sortimentslücken weicht nur geringfügig von der Verteilung im Coop-Gesamtsortiment ab (Abweichungen unter +/- " + str(interpretation_threshold) + " Prozentpunkten).")


# ==============================================================================
# ANGEPASSTE Funktion für Preisverteilung nach Weintyp Vergleich Gaps vs. Coop-Gesamt
# KORREKTUR: Erklärungstext und Hervorhebung Nulllinie, Farben bleiben nach Weintyp
# ==============================================================================
def plot_gaps_preis_nach_weintyp_comparison(
    df_gaps: pd.DataFrame,
    df_coop_original: pd.DataFrame,
    preis_col: str = "Preis",
    weintyp_col: str = "Weintyp",
    bins = None, 
    labels = None, 
    titel: str = "Vergleich: Preisverteilung nach Weintyp (Lücken vs. Coop-Gesamt)",
    interpretation_threshold_pp: float = 2.0
):
    st.subheader(titel)
    # --- ANGEPASSTER Erklärungstext ---
    st.markdown("""
    Diese Analyse zeigt, wie sich die Zusammensetzung der **Sortimentslücken** (Coop-Weine, die Flaschenpost aktuell nicht im Online-Sortiment führt)
    innerhalb jeder Coop-Preisklasse von der typischen Zusammensetzung des Coop-Gesamtsortiments unterscheidet.
    Wir wollen verstehen: Wenn uns Weine in einer bestimmten Preisklasse im Vergleich zu Coop fehlen, welche Weintypen sind davon relativ gesehen überproportional betroffen?

    Das Diagramm und die Tabelle visualisieren die Differenz der prozentualen Anteile:
    *   Die **Farbe der Balken** entspricht dem jeweiligen Weintyp.
    *   Ein Balken **oberhalb der Nulllinie (positiver Wert)** bedeutet: Dieser Weintyp macht einen *größeren Anteil an den identifizierten Lücken* in dieser Preisklasse aus,     als er im Coop-Gesamtsortiment dieser Preisklasse hat. Das deutet darauf hin, dass die "fehlende Abdeckung" von Flaschenpost gegenüber Coop in diesem spezifischen Segment     diesen Weintyp relativ stärker betrifft.
    *   Ein Balken **unterhalb der Nulllinie (negativer Wert)** bedeutet: Dieser Weintyp macht einen *kleineren Anteil an den identifizierten Lücken* in dieser Preisklasse aus,     als er im Coop-Gesamtsortiment dieser Preisklasse hat. Obwohl hier Lücken zum Coop-Sortiment bestehen, sind sie für diesen Weintyp in diesem Segment – relativ gesehen –     weniger ausgeprägt.

    **Wichtiger Hinweis zur Interpretation:** Diese Analyse fokussiert auf die *relative Zusammensetzung* der Lücken im Vergleich zum Coop-Angebot. Aufgrund der deutlich     unterschiedlichen Gesamtgröße der Sortimente (Flaschenpost >24.000 SKUs, Coop ca. 3.500 SKUs) bedeutet eine relative Über- oder Unterrepräsentation bei den Lücken nicht     zwangsläufig, dass Flaschenpost in absoluten Zahlen weniger Produkte eines Typs/einer Preisklasse führt als Coop. Die Analyse dient primär dazu, *Strukturschwerpunkte*     innerhalb der identifizierten Lücken zum Coop-Sortiment aufzuzeigen. Eine hohe relative Abweichung bei den Lücken ist dann besonders interessant, wenn sie auch eine     relevante absolute Anzahl an Produkten betrifft.
    """)
    st.markdown("---")

    if df_gaps.empty: # Restliche Logik zur Datenaufbereitung bleibt gleich
        st.info("Keine Sortimentslücken vorhanden, daher kein detaillierter Preis-/Weintyp-Vergleich möglich.")
        return
    if bins is None:
        max_preis_gaps = df_gaps[preis_col].max() if not df_gaps.empty and preis_col in df_gaps else 100
        max_preis_coop = df_coop_original[preis_col].max() if not df_coop_original.empty and preis_col in df_coop_original else 100
        overall_max_preis = max(max_preis_gaps, max_preis_coop, 101.0); bins = [0, 20, 50, 100, overall_max_preis]
    if labels is None:
        labels = [];
        for i in range(len(bins) - 1):
            if i == len(bins) - 2: labels.append(f"{int(bins[i])}+ CHF")
            else: labels.append(f"{int(bins[i])}–{int(bins[i+1])} CHF")
    def create_pivot(df_input, current_bins, current_labels):
        order = ["Rotwein", "Weisswein", "Roséwein", "Schaumwein"]; df_temp = df_input.copy()
        df_temp["Preisklasse"] = pd.cut(df_temp[preis_col], bins=current_bins, labels=current_labels, include_lowest=True, right=False)
        pivot = df_temp.pivot_table(index="Preisklasse", columns=weintyp_col, aggfunc="size", fill_value=0)
        for typ in order:
            if typ not in pivot.columns: pivot[typ] = 0
        return pivot[order].reindex(current_labels, fill_value=0)
    pivot_gaps = create_pivot(df_gaps, bins, labels); pivot_coop = create_pivot(df_coop_original, bins, labels)
    comparison_data = []
    for preisklasse in labels:
        row = {"Preisklasse": preisklasse}; total_gaps_in_pk = pivot_gaps.loc[preisklasse].sum() if preisklasse in pivot_gaps.index else 0
        total_coop_in_pk = pivot_coop.loc[preisklasse].sum() if preisklasse in pivot_coop.index else 0
        for weintyp in ["Rotwein", "Weisswein", "Roséwein", "Schaumwein"]:
            val_gaps = pivot_gaps.loc[preisklasse, weintyp] if preisklasse in pivot_gaps.index and weintyp in pivot_gaps.columns else 0
            pct_gaps = (val_gaps / total_gaps_in_pk * 100) if total_gaps_in_pk > 0 else 0; row[f"{weintyp} Lücken (%)"] = pct_gaps
            val_coop = pivot_coop.loc[preisklasse, weintyp] if preisklasse in pivot_coop.index and weintyp in pivot_coop.columns else 0
            pct_coop = (val_coop / total_coop_in_pk * 100) if total_coop_in_pk > 0 else 0; row[f"{weintyp} Coop (%)"] = pct_coop
            row[f"Diff. {weintyp} (%)"] = pct_gaps - pct_coop
        comparison_data.append(row)
    comparison_table_df = pd.DataFrame(comparison_data)
    st.write("Vergleich der **prozentualen Anteile (%) jedes Weintyps innerhalb der jeweiligen Preisklasse**:")
    display_cols = ["Preisklasse"]
    column_config_compare = {"Preisklasse": st.column_config.TextColumn(width="medium")}
    for weintyp in ["Rotwein", "Weisswein", "Roséwein", "Schaumwein"]:
        display_cols.extend([f"{weintyp} Lücken (%)", f"{weintyp} Coop (%)", f"Diff. {weintyp} (%)"])
        column_config_compare[f"{weintyp} Lücken (%)"] = st.column_config.NumberColumn(format="%.1f%%")
        column_config_compare[f"{weintyp} Coop (%)"] = st.column_config.NumberColumn(format="%.1f%%")
        column_config_compare[f"Diff. {weintyp} (%)"] = st.column_config.NumberColumn(format="%.1f%%")
    st.dataframe(comparison_table_df[display_cols], hide_index=True, use_container_width=True, column_config=column_config_compare)
    st.markdown("---")
    st.write("Visualisierung der **Abweichungen (in Prozentpunkten)** der Lücken vom Coop-Gesamtsortiment pro Preisklasse:")
    plot_data_list = []
    for preisklasse_label in labels:
        for weintyp_label in ["Rotwein", "Weisswein", "Roséwein", "Schaumwein"]:
            diff_col_name = f"Diff. {weintyp_label} (%)"; preisklasse_row = comparison_table_df[comparison_table_df["Preisklasse"] == preisklasse_label]
            if not preisklasse_row.empty and diff_col_name in preisklasse_row.columns:
                 diff_value = preisklasse_row[diff_col_name].iloc[0]
                 plot_data_list.append({"Preisklasse": preisklasse_label, "Weintyp": weintyp_label, "Differenz (%)": diff_value})
    if not plot_data_list: st.warning("Keine Daten für Differenzvisualisierung."); return
    plot_df_long = pd.DataFrame(plot_data_list)

    # --- Ursprüngliche Plotly Express Logik für Farben (nach Weintyp) ---
    fig_diff_grouped = px.bar(
        plot_df_long,
        x="Preisklasse",
        y="Differenz (%)",
        color="Weintyp",  # Färbung nach Weintyp für Legende und Gruppierung
        barmode="group",
        text_auto='.1f',
        color_discrete_map={"Rotwein": "#8B0000", "Weisswein": "#FADA5E", "Roséwein": "#F6ADC6", "Schaumwein": "#E6E6FA"}
    )
    fig_diff_grouped.update_traces(texttemplate='%{y:.1f}%P', textposition='outside')
    fig_diff_grouped.update_layout(
        yaxis_title="Differenz in Prozentpunkten (Lücken - Coop)",
        xaxis_title="Preisklasse",
        height=500,
        legend_title_text='Weintyp',
        margin=dict(t=30, b=20),
        yaxis_zeroline=True, # Nulllinie anzeigen
        yaxis_zerolinewidth=2, # Breite der Nulllinie
        yaxis_zerolinecolor='Black' # Farbe der Nulllinie
    )
    st.plotly_chart(fig_diff_grouped, use_container_width=True)

    # Dynamische Kurzeinschätzung (bleibt gleich)
    st.markdown("##### Kurzeinschätzung der Abweichungen:") # ... Rest der Interpretationslogik
    bemerkenswerte_abweichungen = []
    for index, row in comparison_table_df.iterrows():
        preisklasse = row["Preisklasse"]
        for weintyp in ["Rotwein", "Weisswein", "Roséwein", "Schaumwein"]:
            differenz = row[f"Diff. {weintyp} (%)"]
            if abs(differenz) >= interpretation_threshold_pp:
                richtung = "stärker" if differenz > 0 else "schwächer"
                bemerkenswerte_abweichungen.append(
                    f"In der Preisklasse **{preisklasse}** ist **{weintyp}** bei den Lücken um **{abs(differenz):.1f} Prozentpunkte {richtung}** vertreten als im Coop-Gesamtsortiment."
                )
    if bemerkenswerte_abweichungen:
        for abweichung in bemerkenswerte_abweichungen: st.markdown(f"- {abweichung}")
    else:
        st.markdown(f"Keine Abweichungen von +/- {interpretation_threshold_pp:.1f} Prozentpunkten oder mehr in der Preis-/Weintyp-Verteilung der Lücken im Vergleich zum Coop-Gesamtsortiment festgestellt.")


# ==============================================================================
# ANGEPASSTE Funktion für Herkunftsländer-Vergleich Gaps vs. Coop-Gesamt
# KORREKTUR: Farbskala für das Balkendiagramm (Grün für Positiv, Rot für Negativ)
# ==============================================================================
def plot_gaps_herkunftslaender_comparison(
    df_gaps: pd.DataFrame,
    df_coop_original: pd.DataFrame,
    region_col_coop: str = "Region",
    top_n: int = 10,
    titel: str = "Vergleich: Top Herkunftsländer (Lücken vs. Coop-Gesamt)",
    interpretation_threshold_pp: float = 1.5 # Schwelle bleibt
):
    st.subheader(titel)
    # Erklärungstext (bleibt so, da wir die Farben jetzt anpassen)
    st.markdown(f"""
    Diese Analyse vergleicht die Verteilung der Top {top_n} Herkunftsländer der **Sortimentslücken**
    mit der Verteilung im **Coop-Gesamtsortiment**. 
    Das Land wird aus der Spalte '{region_col_coop}' extrahiert (erster Teil vor einem Komma, falls vorhanden).

    Die Tabelle zeigt die prozentualen Anteile der Top-Länder für die Lücken und das Coop-Gesamtsortiment
    sowie die Differenz. Das Diagramm visualisiert diese Differenzen:
    *   **Positive Balken (grün):** Das Land ist bei den Lücken **stärker vertreten** als im Coop-Gesamtsortiment (bezogen auf den Anteil des Landes am jeweiligen Gesamtsortiment der Gruppe).
    *   **Negative Balken (rot):** Das Land ist bei den Lücken **schwächer vertreten**.
    """)
    st.markdown("---")

    if df_gaps.empty: # Restliche Datenaufbereitung bleibt gleich
        st.info("Keine Sortimentslücken vorhanden, daher kein Herkunftsländer-Vergleich möglich.")
        return
    def get_laender_verteilung(df_input, region_col, num_top):
        df_temp = df_input.copy()
        df_temp["Land_extracted"] = df_temp[region_col].apply(lambda x: str(x).split(",")[0].strip() if pd.notna(x) and "," in str(x) else str(x).strip() if pd.notna(x) else "Unbekannt")
        counts = df_temp["Land_extracted"].value_counts(); total_in_scope = counts.sum()
        top_counts = counts.head(num_top)
        percent_overall = (counts / len(df_input) * 100) if len(df_input) > 0 else pd.Series(dtype='float64')
        laender_df = pd.DataFrame({'Land': top_counts.index, 'Anzahl': top_counts.values})
        laender_df['Anteil am Gesamt (%)'] = laender_df['Land'].map(percent_overall).fillna(0)
        return counts, percent_overall, laender_df
    _, gaps_percent_overall, top_gaps_df = get_laender_verteilung(df_gaps, region_col_coop, top_n)
    _, coop_percent_overall, top_coop_df = get_laender_verteilung(df_coop_original, region_col_coop, top_n)
    all_top_laender = pd.concat([top_gaps_df['Land'], top_coop_df['Land']]).unique()
    comparison_data = []
    for land in all_top_laender:
        anteil_gaps = gaps_percent_overall.get(land, 0); anteil_coop = coop_percent_overall.get(land, 0)
        comparison_data.append({"Land": land, "Anteil Lücken am Gesamt (%)": anteil_gaps, "Anteil Coop am Gesamt (%)": anteil_coop, "Differenz (Lücken - Coop) (%)": anteil_gaps - anteil_coop})
    comparison_table_df = pd.DataFrame(comparison_data).sort_values(by="Differenz (Lücken - Coop) (%)", ascending=False)
    comparison_table_df_display = comparison_table_df.head(top_n * 2)
    st.write(f"Vergleich der prozentualen Anteile der Top {top_n} Herkunftsländer (Anteil am jeweiligen Gesamtsortiment):")
    st.dataframe(comparison_table_df_display.round(1), hide_index=True, use_container_width=True,
        column_config={"Anteil Lücken am Gesamt (%)": st.column_config.NumberColumn(format="%.1f%%"),
                       "Anteil Coop am Gesamt (%)": st.column_config.NumberColumn(format="%.1f%%"),
                       "Differenz (Lücken - Coop) (%)": st.column_config.NumberColumn(format="%.1f%%")})
    st.markdown("---")
    st.write(f"Visualisierung der **Abweichungen (in Prozentpunkten)** der Lücken vom Coop-Gesamtsortiment (Anteil des Landes am jeweiligen Gesamtsortiment):")
    plot_df = comparison_table_df_display[(comparison_table_df_display['Anteil Lücken am Gesamt (%)'] > 0.1) | (comparison_table_df_display['Anteil Coop am Gesamt (%)'] > 0.1) | (abs(comparison_table_df_display['Differenz (Lücken - Coop) (%)']) > 0.1)].sort_values(by="Differenz (Lücken - Coop) (%)", ascending=False).head(top_n + 5)

    if not plot_df.empty:
        # --- KORRIGIERTE Farblogik ---
        # Erstelle eine Liste von Farben basierend auf dem Wert der Differenz
        colors = ['mediumseagreen' if val >= 0 else 'crimson' for val in plot_df["Differenz (Lücken - Coop) (%)"]]

        fig_diff_laender = px.bar(
            plot_df,
            x="Land",
            y="Differenz (Lücken - Coop) (%)",
            text_auto='.1f',
            # color="Differenz (Lücken - Coop) (%)", # Nicht mehr so, da wir Farben manuell setzen
            # color_continuous_scale=..., # Nicht mehr so
            # color_continuous_midpoint=0
        )
        # Setze die Farben manuell für den Trace
        fig_diff_laender.update_traces(marker_color=colors, texttemplate='%{y:.1f}%P', textposition='outside')
        
        fig_diff_laender.update_layout(
            yaxis_title="Differenz in Prozentpunkten",
            xaxis_title="Herkunftsland",
            height=500,
            xaxis_tickangle=-45,
            margin=dict(t=30, b=100),
            yaxis_zeroline=True, 
            yaxis_zerolinewidth=2, 
            yaxis_zerolinecolor='Black'
        )
        st.plotly_chart(fig_diff_laender, use_container_width=True)
    else:
        st.info("Keine ausreichenden Daten für die Visualisierung der Länderdifferenzen vorhanden.")

    # Dynamische Kurzeinschätzung (bleibt gleich)
    st.markdown("##### Kurzeinschätzung der Abweichungen:") # ... Rest der Interpretationslogik
    significant_findings = []
    for index, row in comparison_table_df_display.iterrows():
        land = row["Land"]; differenz = row["Differenz (Lücken - Coop) (%)"]
        if abs(differenz) >= interpretation_threshold_pp:
            richtung = "stärker" if differenz > 0 else "schwächer"
            significant_findings.append(f"Das Land **{land}** ist bei den Lücken um **{abs(differenz):.1f} Prozentpunkte {richtung}** vertreten als im Coop-Gesamtsortiment (bezogen auf den Anteil des Landes am jeweiligen Gesamtsortiment).")
    if significant_findings:
        for abweichung in significant_findings: st.markdown(f"- {abweichung}")
    else:
        st.markdown(f"Keine Abweichungen von +/- {interpretation_threshold_pp:.1f} Prozentpunkten oder mehr bei den Top-Herkunftsländern festgestellt.")



# In plot_utils.py (diese Funktion unten anfügen)

# =======================================================================================
# NEUE Funktion für Vergleich Frankreich-Regionen (Lücken vs. Coop-Gesamt)
# =======================================================================================
def plot_gaps_frankreich_regionen_comparison(
    df_gaps: pd.DataFrame,
    df_coop_original: pd.DataFrame,
    region_col: str = "Region", # Spalte mit der Roh-Regioneninfo
    titel: str = "Vergleich: Regionen Frankreichs (Lücken vs. Coop-Gesamt)",
    interpretation_threshold_pp: float = 5.0
):
    st.subheader(titel)
    st.markdown(f"""
    Diese Analyse vergleicht die Verteilung der Weinregionen innerhalb Frankreichs für die **Sortimentslücken**
    mit der Verteilung im **Coop-Gesamtsortiment (Frankreich)**.
    Die Regionen werden basierend auf der Spalte '{region_col}' aggregiert.

    Die Tabelle zeigt die prozentualen Anteile der Regionen für die Lücken und das Coop-Gesamtsortiment
    (bezogen auf die jeweiligen Frankreich-Weine) sowie die Differenz. Das Diagramm visualisiert diese Differenzen:
    *   **Positive Balken (grün):** Die Region ist bei den französischen Lücken **stärker vertreten**.
    *   **Negative Balken (rot):** Die Region ist bei den französischen Lücken **schwächer vertreten**.
    """)
    st.markdown("---")

    # Interne Helferfunktion, die deine Logik aus plot_frankreich_regionen kapselt
    def get_frankreich_regionen_verteilung(df_input_all_countries, input_region_col):
        df = df_input_all_countries.copy()
        # Normalisierungs- und Mapping-Logik aus deiner Funktion
        def normalize_string(text):
            text = str(text).lower(); text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
            return text.replace('–', '-').replace(' ', '-')
        subregion_mapping = { "maconnais": "Burgund", "chablis": "Burgund", "beaujolais": "Burgund", "cote-de-beaune": "Burgund", "cote-de-nuits": "Burgund", "cote-chalon": "Burgund", "coteaux-du-lyonnais": "Burgund", "bouzeron": "Burgund", "givry": "Burgund", "mercurey": "Burgund", "montagny": "Burgund", "rully": "Burgund", "cote-d-or": "Burgund", "irancy": "Burgund", "pouilly-fuisse": "Burgund", "saint-veran": "Burgund", "vire-clesse": "Burgund", "saint-bris": "Burgund", "fronsac": "Bordeaux", "saint-emilion": "Bordeaux", "pomerol": "Bordeaux", "margaux": "Bordeaux", "pauillac": "Bordeaux", "saint-julien": "Bordeaux", "saint-estephe": "Bordeaux", "graves": "Bordeaux", "medoc": "Bordeaux", "castillon": "Bordeaux", "listrac": "Bordeaux", "moulis": "Bordeaux", "entre-deux-mers": "Bordeaux", "sauternes": "Bordeaux", "barsac": "Bordeaux", "canon-fronsac": "Bordeaux", "hermitage": "Rhône", "chateauneuf-du-pape": "Rhône", "cornas": "Rhône", "saint-joseph": "Rhône", "gigondas": "Rhône", "cote-rotie": "Rhône", "vacqueyras": "Rhône", "crozes-hermitage": "Rhône", "rasteau": "Rhône", "lirac": "Rhône", "condrieu": "Rhône", "luberon": "Rhône", "cote-du-luberon": "Rhône", "keine-subregion": "Andere", "ubrige-regionen-eu": "Andere"}
        def categorize_region(subregion_normalized):
            if "burgund" in subregion_normalized: return "Burgund"
            elif "bordeaux" in subregion_normalized: return "Bordeaux"
            elif "rhone" in subregion_normalized: return "Rhône"
            return subregion_mapping.get(subregion_normalized, subregion_normalized.capitalize())
        
        df["Land_extracted"] = df[input_region_col].apply(lambda x: str(x).split(",")[0].strip() if pd.notna(x) and "," in str(x) else str(x).strip() if pd.notna(x) else "Unbekannt")
        df["Subregion_raw"] = df[input_region_col].apply(lambda x: str(x).split(",")[1].strip() if pd.notna(x) and "," in str(x) and len(str(x).split(",")) > 1 else "Keine Subregion")
        
        df_fr_only = df[df["Land_extracted"] == "Frankreich"].copy()
        if df_fr_only.empty: return pd.Series(dtype='int64'), pd.Series(dtype='float64') # Leere Series zurückgeben

        df_fr_only["Subregion_normalized"] = df_fr_only["Subregion_raw"].apply(normalize_string)
        df_fr_only["Region_plot"] = df_fr_only["Subregion_normalized"].apply(categorize_region)
        
        region_counts = df_fr_only["Region_plot"].value_counts()
        total_country_wines = region_counts.sum()
        region_percent = (region_counts / total_country_wines * 100) if total_country_wines > 0 else pd.Series(dtype='float64')
        return region_counts, region_percent

    # 1. Verteilung für Gaps (Frankreich)
    gaps_fr_counts, gaps_fr_percent = get_frankreich_regionen_verteilung(df_gaps, region_col)

    # 2. Verteilung für Coop-Gesamtsortiment (Frankreich)
    coop_fr_counts, coop_fr_percent = get_frankreich_regionen_verteilung(df_coop_original, region_col)

    if gaps_fr_counts.empty and coop_fr_counts.empty:
        st.info("Keine Frankreich-Daten in Lücken oder im Coop-Gesamtsortiment gefunden.")
        return

    # 3. Kombiniere die Regionen für die Vergleichstabelle
    all_fr_regions = pd.Index(gaps_fr_counts.index.tolist() + coop_fr_counts.index.tolist()).unique()
    
    comparison_data = []
    for region_name in all_fr_regions:
        anteil_gaps = gaps_fr_percent.get(region_name, 0)
        anteil_coop = coop_fr_percent.get(region_name, 0)
        comparison_data.append({
            "Region Frankreich": region_name,
            "Anteil Lücken (FR) (%)": anteil_gaps,
            "Anteil Coop (FR) (%)": anteil_coop,
            "Differenz (Lücken - Coop) (%)": anteil_gaps - anteil_coop
        })
    
    comparison_table_df = pd.DataFrame(comparison_data).sort_values(by="Differenz (Lücken - Coop) (%)", ascending=False)

    st.write("Vergleich der prozentualen Anteile der Regionen innerhalb Frankreichs:")
    st.dataframe(
        comparison_table_df.round(1), hide_index=True, use_container_width=True,
        column_config={
            "Anteil Lücken (FR) (%)": st.column_config.NumberColumn(format="%.1f%%"),
            "Anteil Coop (FR) (%)": st.column_config.NumberColumn(format="%.1f%%"),
            "Differenz (Lücken - Coop) (%)": st.column_config.NumberColumn(format="%.1f%%")
        }
    )
    st.markdown("---")

    st.write(f"Visualisierung der **Abweichungen (in Prozentpunkten)** der Lücken vom Coop-Gesamtsortiment (Frankreich-Regionen):")
    plot_df = comparison_table_df[abs(comparison_table_df["Differenz (Lücken - Coop) (%)"]) > 0.01].copy() # Nur plotten, wenn Differenz vorhanden
    
    if not plot_df.empty:
        colors = ['mediumseagreen' if val >= 0 else 'crimson' for val in plot_df["Differenz (Lücken - Coop) (%)"]]
        fig_diff_fr_regionen = px.bar(
            plot_df, x="Region Frankreich", y="Differenz (Lücken - Coop) (%)", text_auto='.1f'
        )
        fig_diff_fr_regionen.update_traces(marker_color=colors, texttemplate='%{y:.1f}%P', textposition='outside')
        fig_diff_fr_regionen.update_layout(
            yaxis_title="Differenz in Prozentpunkten", xaxis_title="Region in Frankreich", height=500,
            xaxis_tickangle=-45, margin=dict(t=30, b=120), # Mehr Platz für Labels
            yaxis_zeroline=True, yaxis_zerolinewidth=2, yaxis_zerolinecolor='Black'
        )
        st.plotly_chart(fig_diff_fr_regionen, use_container_width=True)
    else:
        st.info("Keine nennenswerten Differenzen bei den Frankreich-Regionen für Visualisierung gefunden.")

    st.markdown("##### Kurzeinschätzung der Abweichungen (Frankreich-Regionen):")
    significant_findings = []
    for index, row in comparison_table_df.iterrows():
        region_name = row["Region Frankreich"]; differenz = row["Differenz (Lücken - Coop) (%)"]
        if abs(differenz) >= interpretation_threshold_pp:
            richtung = "stärker" if differenz > 0 else "schwächer"
            significant_findings.append(f"Die Region **{region_name}** ist bei den französischen Lücken um **{abs(differenz):.1f} Prozentpunkte {richtung}** vertreten als im französischen Coop-Gesamtsortiment.")
    if significant_findings:
        for abweichung in significant_findings: st.markdown(f"- {abweichung}")
    else:
        st.markdown(f"Keine Abweichungen von +/- {interpretation_threshold_pp:.1f} Prozentpunkten oder mehr bei den Frankreich-Regionen festgestellt.")


# In plot_utils.py (diese Funktion unten anfügen)

# =======================================================================================
# NEUE Funktion für Vergleich Italien-Regionen (Lücken vs. Coop-Gesamt)
# =======================================================================================
def plot_gaps_italien_regionen_comparison(
    df_gaps: pd.DataFrame,
    df_coop_original: pd.DataFrame,
    region_col: str = "Region", # Spalte mit der Roh-Regioneninfo
    titel: str = "Vergleich: Regionen Italiens (Lücken vs. Coop-Gesamt)",
    interpretation_threshold_pp: float = 5.0
):
    st.subheader(titel)
    st.markdown(f"""
    Diese Analyse vergleicht die Verteilung der Weinregionen innerhalb Italiens für die **Sortimentslücken**
    mit der Verteilung im **Coop-Gesamtsortiment (Italien)**.
    Die Regionen werden basierend auf der Spalte '{region_col}' aggregiert.

    Die Tabelle zeigt die prozentualen Anteile der Regionen für die Lücken und das Coop-Gesamtsortiment
    (bezogen auf die jeweiligen Italien-Weine) sowie die Differenz. Das Diagramm visualisiert diese Differenzen:
    *   **Positive Balken (grün):** Die Region ist bei den italienischen Lücken **stärker vertreten**.
    *   **Negative Balken (rot):** Die Region ist bei den italienischen Lücken **schwächer vertreten**.
    """)
    st.markdown("---")

    # Interne Helferfunktion, die deine Logik aus plot_italien_regionen kapselt
    def get_italien_regionen_verteilung(df_input_all_countries, input_region_col):
        df = df_input_all_countries.copy()
        # Normalisierungs- und Mapping-Logik aus deiner Funktion
        def normalize_string(text):
            text = str(text).lower(); text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
            return text.replace('–', '-').replace(' ', '-')
        subregion_mapping = {"lombardei/veltlin": "Lombardei", "keine-subregion": "Andere", "ubrige-regionen-eu": "Andere", "brda": "Andere", "abruzzen-und-apulien": "Andere"} # Dein Mapping
        def categorize_region(subregion_normalized):
            if subregion_normalized in subregion_mapping: return subregion_mapping[subregion_normalized]
            return subregion_normalized.capitalize()
        
        df["Land_extracted"] = df[input_region_col].apply(lambda x: str(x).split(",")[0].strip() if pd.notna(x) and "," in str(x) else str(x).strip() if pd.notna(x) else "Unbekannt")
        df["Subregion_raw"] = df[input_region_col].apply(lambda x: str(x).split(",")[1].strip() if pd.notna(x) and "," in str(x) and len(str(x).split(",")) > 1 else "Keine Subregion")
        
        df_it_only = df[df["Land_extracted"] == "Italien"].copy()
        if df_it_only.empty: return pd.Series(dtype='int64'), pd.Series(dtype='float64')

        df_it_only["Subregion_normalized"] = df_it_only["Subregion_raw"].apply(normalize_string)
        df_it_only["Region_plot"] = df_it_only["Subregion_normalized"].apply(categorize_region)
        
        region_counts = df_it_only["Region_plot"].value_counts()
        total_country_wines = region_counts.sum()
        region_percent = (region_counts / total_country_wines * 100) if total_country_wines > 0 else pd.Series(dtype='float64')
        return region_counts, region_percent

    # 1. Verteilung für Gaps (Italien)
    gaps_it_counts, gaps_it_percent = get_italien_regionen_verteilung(df_gaps, region_col)

    # 2. Verteilung für Coop-Gesamtsortiment (Italien)
    coop_it_counts, coop_it_percent = get_italien_regionen_verteilung(df_coop_original, region_col)

    if gaps_it_counts.empty and coop_it_counts.empty:
        st.info("Keine Italien-Daten in Lücken oder im Coop-Gesamtsortiment gefunden.")
        return

    all_it_regions = pd.Index(gaps_it_counts.index.tolist() + coop_it_counts.index.tolist()).unique()
    
    comparison_data = []
    for region_name in all_it_regions:
        anteil_gaps = gaps_it_percent.get(region_name, 0)
        anteil_coop = coop_it_percent.get(region_name, 0)
        comparison_data.append({
            "Region Italien": region_name,
            "Anteil Lücken (IT) (%)": anteil_gaps,
            "Anteil Coop (IT) (%)": anteil_coop,
            "Differenz (Lücken - Coop) (%)": anteil_gaps - anteil_coop
        })
    
    comparison_table_df = pd.DataFrame(comparison_data).sort_values(by="Differenz (Lücken - Coop) (%)", ascending=False)

    st.write("Vergleich der prozentualen Anteile der Regionen innerhalb Italiens:")
    st.dataframe(
        comparison_table_df.round(1), hide_index=True, use_container_width=True,
        column_config={
            "Anteil Lücken (IT) (%)": st.column_config.NumberColumn(format="%.1f%%"),
            "Anteil Coop (IT) (%)": st.column_config.NumberColumn(format="%.1f%%"),
            "Differenz (Lücken - Coop) (%)": st.column_config.NumberColumn(format="%.1f%%")
        })
    st.markdown("---")

    st.write(f"Visualisierung der **Abweichungen (in Prozentpunkten)** der Lücken vom Coop-Gesamtsortiment (Italien-Regionen):")
    plot_df = comparison_table_df[abs(comparison_table_df["Differenz (Lücken - Coop) (%)"]) > 0.01].copy()
    
    if not plot_df.empty:
        colors = ['mediumseagreen' if val >= 0 else 'crimson' for val in plot_df["Differenz (Lücken - Coop) (%)"]]
        fig_diff_it_regionen = px.bar(
            plot_df, x="Region Italien", y="Differenz (Lücken - Coop) (%)", text_auto='.1f'
        )
        fig_diff_it_regionen.update_traces(marker_color=colors, texttemplate='%{y:.1f}%P', textposition='outside')
        fig_diff_it_regionen.update_layout(
            yaxis_title="Differenz in Prozentpunkten", xaxis_title="Region in Italien", height=500,
            xaxis_tickangle=-45, margin=dict(t=30, b=120),
            yaxis_zeroline=True, yaxis_zerolinewidth=2, yaxis_zerolinecolor='Black'
        )
        st.plotly_chart(fig_diff_it_regionen, use_container_width=True)
    else:
        st.info("Keine nennenswerten Differenzen bei den Italien-Regionen für Visualisierung gefunden.")

    st.markdown("##### Kurzeinschätzung der Abweichungen (Italien-Regionen):")
    significant_findings = []
    for index, row in comparison_table_df.iterrows():
        region_name = row["Region Italien"]; differenz = row["Differenz (Lücken - Coop) (%)"]
        if abs(differenz) >= interpretation_threshold_pp:
            richtung = "stärker" if differenz > 0 else "schwächer"
            significant_findings.append(f"Die Region **{region_name}** ist bei den italienischen Lücken um **{abs(differenz):.1f} Prozentpunkte {richtung}** vertreten als im italienischen Coop-Gesamtsortiment.")
    if significant_findings:
        for abweichung in significant_findings: st.markdown(f"- {abweichung}")
    else:
        st.markdown(f"Keine Abweichungen von +/- {interpretation_threshold_pp:.1f} Prozentpunkten oder mehr bei den Italien-Regionen festgestellt.")


# In plot_utils.py (diese Funktion unten anfügen)

# =======================================================================================
# NEUE Funktion für Vergleich Schweiz-Regionen (Lücken vs. Coop-Gesamt)
# =======================================================================================
def plot_gaps_schweiz_regionen_comparison(
    df_gaps: pd.DataFrame,
    df_coop_original: pd.DataFrame,
    region_col: str = "Region", # Spalte mit der Roh-Regioneninfo
    titel: str = "Vergleich: Regionen der Schweiz (Lücken vs. Coop-Gesamt)",
    interpretation_threshold_pp: float = 5.0
):
    st.subheader(titel)
    st.markdown(f"""
    Diese Analyse vergleicht die Verteilung der Weinregionen innerhalb der Schweiz für die **Sortimentslücken**
    mit der Verteilung im **Coop-Gesamtsortiment (Schweiz)**.
    Die Regionen werden basierend auf der Spalte '{region_col}' aggregiert.

    Die Tabelle zeigt die prozentualen Anteile der Regionen für die Lücken und das Coop-Gesamtsortiment
    (bezogen auf die jeweiligen Schweiz-Weine) sowie die Differenz. Das Diagramm visualisiert diese Differenzen:
    *   **Positive Balken (grün):** Die Region ist bei den Schweizer Lücken **stärker vertreten**.
    *   **Negative Balken (rot):** Die Region ist bei den Schweizer Lücken **schwächer vertreten**.
    """)
    st.markdown("---")

    # Interne Helferfunktion, die deine Logik aus plot_schweiz_regionen kapselt
    def get_schweiz_regionen_verteilung(df_input_all_countries, input_region_col):
        df = df_input_all_countries.copy()
        # Normalisierungs- und Mapping-Logik aus deiner Funktion
        def normalize_string(text):
            text = str(text).lower(); text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
            return text.replace('–', '-').replace(' ', '-')
        subregion_mapping = {"bodensee": "Ostschweiz", "ubrige-schweiz": "Andere"}
        def categorize_region(subregion_normalized):
            if subregion_normalized in subregion_mapping: return subregion_mapping[subregion_normalized]
            # Schreibweisen angleichen (aus deiner Funktion übernommen)
            map_dict = {"wallis": "Wallis", "waadt": "Waadt", "tessin": "Tessin", "drei-seen-region": "Drei-Seen-Region",
                        "genf": "Genf", "basel/aargau": "Basel/Aargau", "zurich": "Zürich", "schaffhausen": "Schaffhausen",
                        "graubunden": "Graubünden", "ostschweiz": "Ostschweiz", "thurgau": "Thurgau", "st.-gallen": "St. Gallen"}
            return map_dict.get(subregion_normalized, subregion_normalized.capitalize())

        df["Land_extracted"] = df[input_region_col].apply(lambda x: str(x).split(",")[0].strip() if pd.notna(x) and "," in str(x) else str(x).strip() if pd.notna(x) else "Unbekannt")
        df["Subregion_raw"] = df[input_region_col].apply(lambda x: str(x).split(",")[1].strip() if pd.notna(x) and "," in str(x) and len(str(x).split(",")) > 1 else "Keine Subregion")
        
        df_ch_only = df[df["Land_extracted"] == "Schweiz"].copy()
        if df_ch_only.empty: return pd.Series(dtype='int64'), pd.Series(dtype='float64')

        df_ch_only["Subregion_normalized"] = df_ch_only["Subregion_raw"].apply(normalize_string)
        df_ch_only["Region_plot"] = df_ch_only["Subregion_normalized"].apply(categorize_region)
        
        region_counts = df_ch_only["Region_plot"].value_counts()
        total_country_wines = region_counts.sum()
        region_percent = (region_counts / total_country_wines * 100) if total_country_wines > 0 else pd.Series(dtype='float64')
        return region_counts, region_percent

    gaps_ch_counts, gaps_ch_percent = get_schweiz_regionen_verteilung(df_gaps, region_col)
    coop_ch_counts, coop_ch_percent = get_schweiz_regionen_verteilung(df_coop_original, region_col)

    if gaps_ch_counts.empty and coop_ch_counts.empty:
        st.info("Keine Schweiz-Daten in Lücken oder im Coop-Gesamtsortiment gefunden.")
        return

    all_ch_regions = pd.Index(gaps_ch_counts.index.tolist() + coop_ch_counts.index.tolist()).unique()
    
    comparison_data = []
    for region_name in all_ch_regions:
        anteil_gaps = gaps_ch_percent.get(region_name, 0)
        anteil_coop = coop_ch_percent.get(region_name, 0)
        comparison_data.append({
            "Region Schweiz": region_name, "Anteil Lücken (CH) (%)": anteil_gaps,
            "Anteil Coop (CH) (%)": anteil_coop, "Differenz (Lücken - Coop) (%)": anteil_gaps - anteil_coop
        })
    comparison_table_df = pd.DataFrame(comparison_data).sort_values(by="Differenz (Lücken - Coop) (%)", ascending=False)

    st.write("Vergleich der prozentualen Anteile der Regionen innerhalb der Schweiz:")
    st.dataframe(comparison_table_df.round(1), hide_index=True, use_container_width=True,
        column_config={
            "Anteil Lücken (CH) (%)": st.column_config.NumberColumn(format="%.1f%%"),
            "Anteil Coop (CH) (%)": st.column_config.NumberColumn(format="%.1f%%"),
            "Differenz (Lücken - Coop) (%)": st.column_config.NumberColumn(format="%.1f%%")
        })
    st.markdown("---")
    st.write(f"Visualisierung der **Abweichungen (in Prozentpunkten)** der Lücken vom Coop-Gesamtsortiment (Schweiz-Regionen):")
    plot_df = comparison_table_df[abs(comparison_table_df["Differenz (Lücken - Coop) (%)"]) > 0.01].copy()
    
    if not plot_df.empty:
        colors = ['mediumseagreen' if val >= 0 else 'crimson' for val in plot_df["Differenz (Lücken - Coop) (%)"]]
        fig = px.bar(plot_df, x="Region Schweiz", y="Differenz (Lücken - Coop) (%)", text_auto='.1f')
        fig.update_traces(marker_color=colors, texttemplate='%{y:.1f}%P', textposition='outside')
        fig.update_layout(yaxis_title="Differenz in Prozentpunkten", xaxis_title="Region in der Schweiz", height=500,
                          xaxis_tickangle=-45, margin=dict(t=30, b=120), # Mehr Platz für Labels
                          yaxis_zeroline=True, yaxis_zerolinewidth=2, yaxis_zerolinecolor='Black')
        st.plotly_chart(fig, use_container_width=True)
    else: st.info("Keine nennenswerten Differenzen bei den Schweiz-Regionen für Visualisierung gefunden.")

    st.markdown("##### Kurzeinschätzung der Abweichungen (Schweiz-Regionen):")
    significant_findings = []
    for index, row in comparison_table_df.iterrows():
        region_name = row["Region Schweiz"]; differenz = row["Differenz (Lücken - Coop) (%)"]
        if abs(differenz) >= interpretation_threshold_pp:
            richtung = "stärker" if differenz > 0 else "schwächer"
            significant_findings.append(f"Die Region **{region_name}** ist bei den Schweizer Lücken um **{abs(differenz):.1f} Prozentpunkte {richtung}** vertreten als im Schweizer Coop-Gesamtsortiment.")
    if significant_findings:
        for abweichung in significant_findings: st.markdown(f"- {abweichung}")
    else: st.markdown(f"Keine Abweichungen von +/- {interpretation_threshold_pp:.1f} Prozentpunkten oder mehr bei den Schweiz-Regionen festgestellt.")



# In plot_utils.py (diese Funktion unten anfügen)

# =======================================================================================
# NEUE Funktion für Vergleich Spanien-Regionen (Lücken vs. Coop-Gesamt)
# =======================================================================================
def plot_gaps_spanien_regionen_comparison(
    df_gaps: pd.DataFrame,
    df_coop_original: pd.DataFrame,
    region_col: str = "Region", # Spalte mit der Roh-Regioneninfo
    titel: str = "Vergleich: Regionen Spaniens (Lücken vs. Coop-Gesamt)",
    interpretation_threshold_pp: float = 5.0
):
    st.subheader(titel)
    st.markdown(f"""
    Diese Analyse vergleicht die Verteilung der Weinregionen innerhalb Spaniens für die **Sortimentslücken**
    mit der Verteilung im **Coop-Gesamtsortiment (Spanien)**.
    Die Regionen werden basierend auf der Spalte '{region_col}' aggregiert.

    Die Tabelle zeigt die prozentualen Anteile der Regionen für die Lücken und das Coop-Gesamtsortiment
    (bezogen auf die jeweiligen Spanien-Weine) sowie die Differenz. Das Diagramm visualisiert diese Differenzen:
    *   **Positive Balken (grün):** Die Region ist bei den spanischen Lücken **stärker vertreten**.
    *   **Negative Balken (rot):** Die Region ist bei den spanischen Lücken **schwächer vertreten**.
    """)
    st.markdown("---")

    # Interne Helferfunktion, die deine Logik aus plot_spanien_regionen kapselt
    def get_spanien_regionen_verteilung(df_input_all_countries, input_region_col):
        df = df_input_all_countries.copy()
        # Normalisierungs- und Mapping-Logik aus deiner Funktion
        def normalize_string(text): # Deine Normalisierungsfunktion
            text = str(text).lower(); text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
            text = text.replace('–', '-').replace(' ', '-'); text = re.sub(r'-+', '-', text); text = re.sub(r'--+', '-', text)
            return text
        # Dein subregion_mapping für Spanien
        subregion_mapping = {"priorat": "Katalonien", "ribera-del-duero": "Castilla y León", "rueda": "Castilla y León", "toro": "Castilla y León", "kastilien-leon": "Castilla y León", "cigales": "Castilla y León", "requena": "Valencia", "yecla-do": "Murcia", "kastilien-la-mancha": "Castilla-La Mancha", "mentrida-do-(toledo)": "Castilla-La Mancha", "dehesa-del-carrizal-do": "Castilla-La Mancha", "kastilien-l-a-mancha": "Castilla-La Mancha", "alava": "Rioja", "mallorca": "Balearen", "ubriges-spanien": "Andere", "keine-subregion": "Andere"}
        def categorize_region(subregion_normalized): # Deine Kategorisierungsfunktion für Spanien
            if subregion_normalized in subregion_mapping: return subregion_mapping[subregion_normalized]
            map_dict = {"teneriffa": "Teneriffa", "navarra": "Navarra", "galicien": "Galicien", "somontano": "Somontano", "jerez": "Jerez"}
            return map_dict.get(subregion_normalized, subregion_normalized.capitalize())

        df["Land_extracted"] = df[input_region_col].apply(lambda x: str(x).split(",")[0].strip() if pd.notna(x) and "," in str(x) else str(x).strip() if pd.notna(x) else "Unbekannt")
        df["Subregion_raw"] = df[input_region_col].apply(lambda x: str(x).split(",")[1].strip() if pd.notna(x) and "," in str(x) and len(str(x).split(",")) > 1 else "Keine Subregion")
        
        df_es_only = df[df["Land_extracted"] == "Spanien"].copy()
        if df_es_only.empty: return pd.Series(dtype='int64'), pd.Series(dtype='float64')

        df_es_only["Subregion_normalized"] = df_es_only["Subregion_raw"].apply(normalize_string)
        df_es_only["Region_plot"] = df_es_only["Subregion_normalized"].apply(categorize_region)
        
        region_counts = df_es_only["Region_plot"].value_counts()
        total_country_wines = region_counts.sum()
        region_percent = (region_counts / total_country_wines * 100) if total_country_wines > 0 else pd.Series(dtype='float64')
        return region_counts, region_percent

    gaps_es_counts, gaps_es_percent = get_spanien_regionen_verteilung(df_gaps, region_col)
    coop_es_counts, coop_es_percent = get_spanien_regionen_verteilung(df_coop_original, region_col)

    if gaps_es_counts.empty and coop_es_counts.empty:
        st.info("Keine Spanien-Daten in Lücken oder im Coop-Gesamtsortiment gefunden.")
        return

    all_es_regions = pd.Index(gaps_es_counts.index.tolist() + coop_es_counts.index.tolist()).unique()
    
    comparison_data = []
    for region_name in all_es_regions:
        anteil_gaps = gaps_es_percent.get(region_name, 0); anteil_coop = coop_es_percent.get(region_name, 0)
        comparison_data.append({
            "Region Spanien": region_name, "Anteil Lücken (ES) (%)": anteil_gaps,
            "Anteil Coop (ES) (%)": anteil_coop, "Differenz (Lücken - Coop) (%)": anteil_gaps - anteil_coop})
    comparison_table_df = pd.DataFrame(comparison_data).sort_values(by="Differenz (Lücken - Coop) (%)", ascending=False)

    st.write("Vergleich der prozentualen Anteile der Regionen innerhalb Spaniens:")
    st.dataframe(comparison_table_df.round(1), hide_index=True, use_container_width=True,
        column_config={
            "Anteil Lücken (ES) (%)": st.column_config.NumberColumn(format="%.1f%%"),
            "Anteil Coop (ES) (%)": st.column_config.NumberColumn(format="%.1f%%"),
            "Differenz (Lücken - Coop) (%)": st.column_config.NumberColumn(format="%.1f%%")})
    st.markdown("---")
    st.write(f"Visualisierung der **Abweichungen (in Prozentpunkten)** der Lücken vom Coop-Gesamtsortiment (Spanien-Regionen):")
    plot_df = comparison_table_df[abs(comparison_table_df["Differenz (Lücken - Coop) (%)"]) > 0.01].copy()
    
    if not plot_df.empty:
        colors = ['mediumseagreen' if val >= 0 else 'crimson' for val in plot_df["Differenz (Lücken - Coop) (%)"]]
        fig = px.bar(plot_df, x="Region Spanien", y="Differenz (Lücken - Coop) (%)", text_auto='.1f')
        fig.update_traces(marker_color=colors, texttemplate='%{y:.1f}%P', textposition='outside')
        fig.update_layout(yaxis_title="Differenz in Prozentpunkten", xaxis_title="Region in Spanien", height=500,
                          xaxis_tickangle=-45, margin=dict(t=30, b=120), # Mehr Platz für Labels
                          yaxis_zeroline=True, yaxis_zerolinewidth=2, yaxis_zerolinecolor='Black')
        st.plotly_chart(fig, use_container_width=True)
    else: st.info("Keine nennenswerten Differenzen bei den Spanien-Regionen für Visualisierung gefunden.")

    st.markdown("##### Kurzeinschätzung der Abweichungen (Spanien-Regionen):")
    significant_findings = []
    for index, row in comparison_table_df.iterrows():
        region_name = row["Region Spanien"]; differenz = row["Differenz (Lücken - Coop) (%)"]
        if abs(differenz) >= interpretation_threshold_pp:
            richtung = "stärker" if differenz > 0 else "schwächer"
            significant_findings.append(f"Die Region **{region_name}** ist bei den spanischen Lücken um **{abs(differenz):.1f} Prozentpunkte {richtung}** vertreten als im spanischen Coop-Gesamtsortiment.")
    if significant_findings:
        for abweichung in significant_findings: st.markdown(f"- {abweichung}")
    else: st.markdown(f"Keine Abweichungen von +/- {interpretation_threshold_pp:.1f} Prozentpunkten oder mehr bei den Spanien-Regionen festgestellt.")


# In plot_utils.py (diese Funktion unten anfügen)

# ==============================================================================
# NEUE Funktion für Produzenten-Vergleich Gaps vs. Coop-Gesamt
# Verwendet df_matching_enriched als Basis
# ==============================================================================
def plot_gaps_produzenten_comparison(
    df_matching_all_coop: pd.DataFrame, # Dies ist dein angereichertes manuelle_matches_final2.xlsx
    coop_produzent_col: str = "Coop_Produzent",
    match_status_col: str = "Match_Status",
    non_match_status_value: str = "Kein Match",
    top_n: int = 10, # Anzahl der Top-Produzenten, die detaillierter betrachtet werden
    titel: str = "Vergleich: Top Produzenten (Lücken vs. Coop-Gesamt)",
    interpretation_threshold_pp: float = 3.0 # Schwelle für "bemerkenswerte" Abweichung
):
    st.subheader(titel)
    st.markdown(f"""
    Diese Analyse vergleicht die Verteilung der Top {top_n} Coop-Produzenten bei den **Sortimentslücken**
    (Coop-Weine mit Status '{non_match_status_value}') mit deren Verteilung im **Coop-Gesamtsortiment**
    (alle Coop-Weine aus der Matching-Datei).
    Die Anteile beziehen sich auf das jeweilige Gesamtsortiment (alle Lücken bzw. alle Coop-Produkte).

    Die Tabelle zeigt die prozentualen Anteile für die Lücken und das Coop-Gesamtsortiment
    sowie die Differenz. Das Diagramm visualisiert diese Differenzen:
    *   **Positive Balken (grün):** Der Produzent ist bei den Lücken **stärker vertreten**.
    *   **Negative Balken (rot):** Der Produzent ist bei den Lücken **schwächer vertreten**.
    """)
    st.markdown("---")

    # 1. Erstelle df_gaps direkt aus df_matching_all_coop
    df_gaps = df_matching_all_coop[df_matching_all_coop[match_status_col] == non_match_status_value].copy()

    if df_gaps.empty:
        st.info("Keine Sortimentslücken vorhanden (basierend auf Match-Status), daher kein Produzenten-Vergleich möglich.")
        return
    if coop_produzent_col not in df_matching_all_coop.columns:
        st.error(f"Spalte '{coop_produzent_col}' nicht in der Matching-Datei gefunden.")
        return

    # Helferfunktion zur Zählung und Prozentberechnung
    def get_produzenten_verteilung(df_input, produzent_col_name, num_top, df_basis_fuer_prozent):
        counts = df_input[produzent_col_name].value_counts()
        # Prozentanteile bezogen auf die Gesamtzahl der Weine im jeweiligen Basis-DataFrame
        percent_overall = (counts / len(df_basis_fuer_prozent) * 100) if len(df_basis_fuer_prozent) > 0 else pd.Series(dtype='float64')
        
        top_produzenten_namen = counts.head(num_top).index
        return counts, percent_overall, top_produzenten_namen

    # Verteilung für Gaps (Basis für Prozent: alle Gaps)
    _, gaps_percent_overall, top_gaps_produzenten = get_produzenten_verteilung(df_gaps, coop_produzent_col, top_n, df_gaps)

    # Verteilung für Coop-Gesamtsortiment (Basis für Prozent: alle Coop-Produkte in der Matching-Datei)
    _, coop_percent_overall, top_coop_produzenten = get_produzenten_verteilung(df_matching_all_coop, coop_produzent_col, top_n, df_matching_all_coop)
    
    # Kombiniere die Top-Produzenten aus beiden Listen für den Vergleich
    all_top_produzenten = pd.Index(top_gaps_produzenten.tolist() + top_coop_produzenten.tolist()).unique()
    
    comparison_data = []
    for produzent in all_top_produzenten:
        anteil_gaps = gaps_percent_overall.get(produzent, 0)
        anteil_coop = coop_percent_overall.get(produzent, 0)
        comparison_data.append({
            "Coop Produzent": produzent,
            "Anteil bei Lücken (%)": anteil_gaps,
            "Anteil im Coop-Gesamt (%)": anteil_coop,
            "Differenz (Lücken - Coop) (%)": anteil_gaps - anteil_coop
        })
    
    comparison_table_df = pd.DataFrame(comparison_data).sort_values(by="Differenz (Lücken - Coop) (%)", ascending=False)
    # Limitiere die Anzeige in der Tabelle auf eine sinnvolle Anzahl
    comparison_table_df_display = comparison_table_df.head(min(len(comparison_table_df), top_n + 5))


    st.write(f"Vergleich der prozentualen Anteile der Top-Coop-Produzenten (Anteil am jeweiligen Gesamtsortiment):")
    st.dataframe(
        comparison_table_df_display.round(1), hide_index=True, use_container_width=True,
        column_config={
            "Anteil bei Lücken (%)": st.column_config.NumberColumn(format="%.1f%%"),
            "Anteil im Coop-Gesamt (%)": st.column_config.NumberColumn(format="%.1f%%"),
            "Differenz (Lücken - Coop) (%)": st.column_config.NumberColumn(format="%.1f%%")
        }
    )
    st.markdown("---")

    st.write(f"Visualisierung der **Abweichungen (in Prozentpunkten)** der Lücken vom Coop-Gesamtsortiment:")
    
    # Nur Produzenten mit nennenswerter Differenz oder Präsenz für den Plot nehmen
    plot_df = comparison_table_df_display[
        (abs(comparison_table_df_display["Differenz (Lücken - Coop) (%)"]) > 0.1) |
        (comparison_table_df_display["Anteil bei Lücken (%)"] > 0.5) | # Produzenten, die zumindest bei Lücken etwas prominent sind
        (comparison_table_df_display["Anteil im Coop-Gesamt (%)"] > 0.5) # oder im Coop-Gesamt
    ].sort_values(by="Differenz (Lücken - Coop) (%)", ascending=False).head(top_n + 5)


    if not plot_df.empty:
        colors = ['mediumseagreen' if val >= 0 else 'crimson' for val in plot_df["Differenz (Lücken - Coop) (%)"]]
        fig = px.bar(
            plot_df, x="Coop Produzent", y="Differenz (Lücken - Coop) (%)", text_auto='.1f'
        )
        fig.update_traces(marker_color=colors, texttemplate='%{y:.1f}%P', textposition='outside')
        fig.update_layout(
            yaxis_title="Differenz in Prozentpunkten", xaxis_title="Coop Produzent", height=500,
            xaxis_tickangle=-45, margin=dict(t=30, b=150), # Mehr Platz unten für lange Produzentennamen
            yaxis_zeroline=True, yaxis_zerolinewidth=2, yaxis_zerolinecolor='Black'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Keine ausreichenden Daten für die Visualisierung der Produzenten-Differenzen vorhanden.")

    st.markdown("##### Kurzeinschätzung der Abweichungen:")
    significant_findings = []
    for index, row in comparison_table_df_display.iterrows():
        produzent = row["Coop Produzent"]; differenz = row["Differenz (Lücken - Coop) (%)"]
        if abs(differenz) >= interpretation_threshold_pp:
            richtung = "stärker" if differenz > 0 else "schwächer"
            significant_findings.append(f"Der Produzent **{produzent}** ist bei den Lücken um **{abs(differenz):.1f} Prozentpunkte {richtung}** vertreten als im Coop-Gesamtsortiment.")
    if significant_findings:
        for abweichung in significant_findings: st.markdown(f"- {abweichung}")
    else:
        st.markdown(f"Keine Produzenten mit Abweichungen von +/- {interpretation_threshold_pp:.1f} Prozentpunkten oder mehr bei den Lücken im Vergleich zum Coop-Gesamtsortiment festgestellt.")


# In plot_utils.py (NUR diese Funktion ersetzen)

# ==============================================================================
# Funktion für Top Produzenten in den Lücken (absolute Zahlen)
# Verwendet df_matching_enriched als Basis
# ERNEUTE, ENDGÜLTIGE KORREKTUR: Tippfehler bei produzenten_counts_gaps 
# ==============================================================================
def plot_top_produzenten_in_gaps(
    df_matching_all_coop: pd.DataFrame, 
    coop_produzent_col: str = "Coop_Produzent",
    match_status_col: str = "Match_Status",
    non_match_status_value: str = "Kein Match",
    top_n: int = 30, 
    titel: str = "Top Coop-Produzenten in den Sortimentslücken (absolute Anzahl fehlender Weine)"
):
    st.subheader(titel)
    # ... (Markdown Text bleibt gleich) ...
    st.markdown(f"""
    Diese Analyse zeigt, welche Coop-Produzenten am häufigsten mit ihren Weinen in den **Sortimentslücken** vertreten sind 
    (d.h. Coop-Weine mit dem Status '{non_match_status_value}', die Flaschenpost nicht führt). 
    Es wird die **absolute Anzahl** der "fehlenden" Weine pro Produzent für die Top {top_n} Produzenten dargestellt.

    **Wie diese Analyse genutzt werden kann:**
    *   **Identifikation von Schlüssel-Produzenten:** Gibt es bestimmte Produzenten, von denen Flaschenpost im Vergleich zu Coop besonders viele Weine nicht listet? Dies könnte auf strategische Entscheidungen, unterschiedliche Lieferantenbeziehungen oder potenzielle Bereiche für Sortimentserweiterungen hindeuten.
    *   **Fokus für weitere Recherche:** Bei Produzenten, die hier häufig erscheinen, könnte eine genauere qualitative Prüfung der spezifisch fehlenden Weine sinnvoll sein (z.B. über die Detailtabelle der Sortimentslücken).
    *   **Verständnis der Lücken-Zusammensetzung:** Hilft zu verstehen, ob die Lücken eher von vielen verschiedenen kleinen Produzenten oder von wenigen großen Produzenten dominiert werden.

    Beachten Sie, dass diese Analyse die absolute Häufigkeit in den Lücken zeigt und nicht den prozentualen Anteil des Produzenten am Coop-Gesamtsortiment (dafür siehe die vorherige Analyse "Vergleich: Top Coop-Produzenten (Lücken vs. Coop-Gesamt)").
    """)
    st.markdown("---")

    df_gaps = df_matching_all_coop[df_matching_all_coop[match_status_col] == non_match_status_value].copy()

    if df_gaps.empty:
        st.info("Keine Sortimentslücken vorhanden, daher keine Top-Produzenten-Analyse der Lücken möglich.")
        return
    if coop_produzent_col not in df_gaps.columns:
        st.error(f"Spalte '{coop_produzent_col}' nicht in den Gap-Daten gefunden.")
        return

    # Hier wird die Variable korrekt mit "z" definiert:
    produzenten_counts_gaps = df_gaps[coop_produzent_col].value_counts().head(top_n) 
    
    if produzenten_counts_gaps.empty: 
        st.info(f"Keine Produzenten in den Sortimentslücken gefunden für die Spalte '{coop_produzent_col}'.")
        return

    col_chart, col_table = st.columns([1.5, 1])

    with col_chart:
        fig = px.bar(
            x=produzenten_counts_gaps.index, 
            y=produzenten_counts_gaps.values, 
            text=produzenten_counts_gaps.values, 
            labels={'x': 'Coop Produzent', 'y': 'Anzahl fehlender Weine (Lücken)'},
            color_discrete_sequence=['#4A708B'] 
        )
        fig.update_traces(textposition="outside", textfont_size=12)
        fig.update_layout(
            height=max(400, top_n * 25), 
            plot_bgcolor="#ffffff",
            xaxis_title="Coop Produzent", yaxis_title="Anzahl fehlender Weine",
            xaxis_tickangle=-45, margin=dict(t=30, r=15, l=5, b=170 if top_n > 15 else 120) 
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_table:
        # HIER WAR DER FEHLER (VERMUTLICH): `producenten_counts_gaps` STATT `produzenten_counts_gaps`
        table_df = pd.DataFrame({
            "Coop Produzent": produzenten_counts_gaps.index,         # Korrigiert zu "z"
            "Anzahl fehlender Weine": produzenten_counts_gaps.values # Korrigiert zu "z"
        })
        total_gaps_count = len(df_gaps)
        table_df["Anteil an allen Lücken (%)"] = (table_df["Anzahl fehlender Weine"] / total_gaps_count * 100).round(1)
        
        st.dataframe(table_df, use_container_width=True, hide_index=True,
            column_config={"Anzahl fehlender Weine": st.column_config.NumberColumn(format="%d"),
                           "Anteil an allen Lücken (%)": st.column_config.NumberColumn(format="%.1f%%")})
        timestamp_str = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        file_name_csv = f"top_produzenten_in_gaps_{timestamp_str}.csv"
        st.download_button(label="Tabelle als CSV", data=table_df.to_csv(index=False, sep=';').encode("utf-8-sig"),
                           file_name=file_name_csv, mime="text/csv", key=f"dl_csv_top_prod_gaps_{timestamp_str}") 
    
    st.caption(f"Angezeigt werden die Top {min(top_n, len(produzenten_counts_gaps))} Produzenten, von denen Weine im Coop-Sortiment sind, aber nicht bei Flaschenpost (basierend auf '{non_match_status_value}').") # Korrigiert zu "z"



# In plot_utils.py (DIESE FUNKTION unten anfügen oder die bestehende davon ersetzen)
# Stelle sicher, dass re und unicodedata oben in plot_utils.py importiert sind:
# import re
# import unicodedata
# import pandas as pd # Wird innerhalb der Funktion verwendet
# import streamlit as st # Wird innerhalb der Funktion verwendet
# import plotly.express as px # Wird innerhalb der Funktion verwendet


# === Normalisierungs-Konstanten und Funktion für Produzentennamen ===
# Diese sollten idealerweise einmal global am Anfang von plot_utils.py stehen,
# wenn sie von mehreren Funktionen verwendet werden.
# Wenn sie nur hier gebraucht werden, ist es okay, sie direkt davor zu definieren.

_SORTED_AUSSCHLUSS_BEGRIFFE_PROD = sorted([ # DEINE AKTUALISIERTE LISTE
    "azienda agricola", "marchesi de", "barons de", "baron philippe", "feudi di", "feudi", "ac", "a.c.", "aoc", "aop", "do", "doc", "igt", "docg", "igp", "doca", "vinhos",
    "appellation", "controlee", "maison", "fratelli", "tenuta", "cantina", "famille", "marchesi", "raventos", "tenimenti",
    "azienda", "agricola", "cantine", "bodega", "estate", "winery", "bodegas", "domaine", "domaines", "weingut"
], key=len, reverse=True)

_EXCLUSION_PATTERN_PROD = re.compile(
    r'\b(?:' + '|'.join(map(re.escape, _SORTED_AUSSCHLUSS_BEGRIFFE_PROD)) + r')\b',
    flags=re.IGNORECASE
)
_NORMALIZE_PATTERN_PROD = re.compile(r"[-/,;.:\"'’()`*&]")
_MULTI_SPACE_PATTERN_PROD = re.compile(r"\s+")

def normalize_produzent_name(text):
    if pd.isna(text) or text == "": return ""
    text = str(text); text = unicodedata.normalize("NFKD", text)
    text = "".join([c for c in text if not unicodedata.combining(c)])
    text = text.lower(); text = _NORMALIZE_PATTERN_PROD.sub(" ", text)
    text = text.replace(" e figli", "").replace(" et fils", "").replace(" & fils", "").replace(" y hijos", "")
    text = text.replace(" vigneron", "").replace(" vignerons", "")
    text = _EXCLUSION_PATTERN_PROD.sub("", text) 
    text = _MULTI_SPACE_PATTERN_PROD.sub(" ", text); return text.strip()

# ==============================================================================
# Funktion: Coop-Produzenten der Gaps, die NICHT bei Flaschenpost sind
# ANGEPASST: _SORTED_AUSSCHLUSS_BEGRIFFE_PROD aktualisiert, top_n Default auf 30
# ==============================================================================
def plot_coop_produzenten_nicht_in_fp(
    df_matching_all_coop: pd.DataFrame, 
    df_fp_original: pd.DataFrame,       
    coop_produzent_col_matching: str = "Coop_Produzent",
    fp_produzent_col_original: str = "Produzent",
    match_status_col: str = "Match_Status",
    non_match_status_value: str = "Kein Match",
    top_n: int = 30, # <<< ANGEPASST AUF 30
    titel: str = "Coop-Produzenten (von Lücken), die nicht im Flaschenpost-Sortiment gelistet sind"
):
    st.subheader(titel)
    st.markdown(f"""
    Diese Analyse identifiziert Coop-Produzenten, von denen Weine im Coop-Sortiment als Lücke zu Flaschenpost klassifiziert wurden 
    (Status '{non_match_status_value}'), und die als Produzentenname **nicht** im gesamten Flaschenpost-Sortiment gefunden werden konnten.
    Die Produzentennamen werden vor dem Abgleich normalisiert (Kleinschreibung, Entfernung von Sonderzeichen und typischen Weinbau-Zusätzen).
    Angezeigt werden die Top {top_n} dieser Produzenten, sortiert nach der Anzahl der von ihnen stammenden "Gap"-Weine bei Coop.

    **Wie diese Analyse genutzt werden kann:**
    *   **Identifikation potenziell neuer Lieferanten/Marken:** Zeigt Produzenten, die Coop führt, Flaschenpost aber möglicherweise noch keine Geschäftsbeziehung hat oder deren Produkte nicht listet.
    *   **Bewertung von "echten" Produzenten-Lücken:** Hilft zu unterscheiden, ob eine Lücke bei einem Wein eines bekannten Produzenten (den FP sonst führt) besteht oder ob der gesamte Produzent bei FP fehlt.
    """)
    st.markdown("---")

    df_gaps = df_matching_all_coop[df_matching_all_coop[match_status_col] == non_match_status_value].copy()
    if df_gaps.empty: st.info("Keine Lücken, Analyse nicht möglich."); return
    if coop_produzent_col_matching not in df_gaps.columns: st.error(f"Spalte '{coop_produzent_col_matching}' nicht in Gap-Daten."); return
    
    df_gaps["Coop_Produzent_Normalized"] = df_gaps[coop_produzent_col_matching].apply(normalize_produzent_name)
    df_gaps = df_gaps[df_gaps["Coop_Produzent_Normalized"] != ""]

    if fp_produzent_col_original not in df_fp_original.columns: st.error(f"Spalte '{fp_produzent_col_original}' nicht in Flaschenpost-Datei."); return
    fp_produzenten_normalized_set = set(df_fp_original[fp_produzent_col_original].astype(str).apply(normalize_produzent_name).unique()); fp_produzenten_normalized_set.discard("")
    
    df_gaps["Ist_Produzent_bei_FP"] = df_gaps["Coop_Produzent_Normalized"].isin(fp_produzenten_normalized_set)
    df_produzenten_nur_coop_gaps = df_gaps[~df_gaps["Ist_Produzent_bei_FP"]]

    if df_produzenten_nur_coop_gaps.empty: st.info("Alle Produzenten der Lücken scheinen auch bei FP vertreten zu sein."); return
    
    top_produzenten_nur_coop = df_produzenten_nur_coop_gaps[coop_produzent_col_matching].value_counts().head(top_n)
    if top_produzenten_nur_coop.empty: st.info("Keine Produzenten nach Filterung übrig."); return

    col_chart, col_table = st.columns([1.5, 1])
    with col_chart:
        fig = px.bar(x=top_produzenten_nur_coop.index, y=top_produzenten_nur_coop.values, text=top_produzenten_nur_coop.values,
                     labels={'x': 'Coop Produzent (nicht bei FP)', 'y': 'Anzahl Gap-Weine bei Coop'}, color_discrete_sequence=['#8B4513'])
        fig.update_traces(textposition="outside", textfont_size=12)
        fig.update_layout(height=max(400, top_n * 25), plot_bgcolor="#ffffff", # Höhe angepasst
                          xaxis_title="Coop Produzent", yaxis_title="Anzahl Gap-Weine",
                          xaxis_tickangle=-45, margin=dict(t=30, r=15, l=5, b=170 if top_n > 15 else 120)) # Mehr Platz unten
        st.plotly_chart(fig, use_container_width=True)
    with col_table:
        table_df = pd.DataFrame({"Coop Produzent (nicht bei FP)": top_produzenten_nur_coop.index, "Anzahl Gap-Weine bei Coop": top_produzenten_nur_coop.values})
        st.dataframe(table_df, use_container_width=True, hide_index=True, column_config={"Anzahl Gap-Weine bei Coop": st.column_config.NumberColumn(format="%d")})
        timestamp_str = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S"); file_name_csv = f"produzenten_nur_coop_gaps_{timestamp_str}.csv"
        st.download_button(label="Tabelle als CSV", data=table_df.to_csv(index=False, sep=';').encode("utf-8-sig"),
                           file_name=file_name_csv, mime="text/csv", key=f"dl_csv_prod_nur_coop_{timestamp_str}")
    st.caption(f"Angezeigt: Top {min(top_n, len(top_produzenten_nur_coop))} Produzenten (Lücken, nicht bei FP).")