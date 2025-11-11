import streamlit as st
import pandas as pd

# HUOM! Data on aina hyvä rajata pelkästään siihen, mitä dataa käytetään
# Streamlitiin kirjautuminen githubilla

rovaniemi_df = pd.read_csv("https://pxdata.stat.fi/PxWeb/sq/4c02da84-4baf-4fec-8c45-101aa473f885", encoding="latin-1")
rovaniemi_df[["Vuosi", "Kuukausi_num"]] = rovaniemi_df["Kuukausi"].str.split("M", expand=True)

st.title("Hotellien kuukausittainen kapasiteetti ja yöpymiset kunnittain muuttujina Kuukausi, Kunta ja Tiedot")

# ==============================================================================
# Load one municipality via saved-query CSV URL (PxWeb).
# Show a data table for that municipality.
st.header("Load one municipality via saved-query CSV URL (PxWeb).")
st.header("Show a data table for that municipality.")
st.dataframe(rovaniemi_df)



# ==============================================================================
# Simple overall trend (line chart) for a chosen metric.
st.header("Simple overall trend (line chart) for a chosen metric.")
huone_aste_roi_df = rovaniemi_df[["Kuukausi", "Huonekäyttöaste, % Rovaniemi"]]
st.line_chart(huone_aste_roi_df, x="Kuukausi", y="Huonekäyttöaste, % Rovaniemi")



# ==============================================================================
# Yearly totals (bar chart) for nights spent.
st.header("Yearly totals (bar chart) for nights spent.")

# Tunnilla tehty
vuosi_yo_roi_df = rovaniemi_df[["Vuosi", "Kuukausi", "Yöpymiset, lkm Rovaniemi"]].groupby(by="Vuosi").sum()
st.dataframe(vuosi_yo_roi_df)
st.text("Classic groupBy")
st.bar_chart(vuosi_yo_roi_df, y="Yöpymiset, lkm Rovaniemi")

# Oma ratkaisu
st.text("Aggregation")
yearly_df = rovaniemi_df.groupby(by="Vuosi", as_index=False).agg({"Yöpymiset, lkm Rovaniemi": "sum"})
st.bar_chart(yearly_df, x="Vuosi", y="Yöpymiset, lkm Rovaniemi")



# ==============================================================================
# Domestic vs Foreign: table + small line chart (if columns exist).
#vuosi_yo_roi_ku_df = rovaniemi_df[["Vuosi", "Kotimaiset yöpymiset, lkm Rovaniemi", "Ulkomaiset yöpymiset Rovaniemi"]].groupby(by="Vuosi").sum()
st.header("Domestic vs Foreign: table + small line chart (if columns exist).")
temp_df = rovaniemi_df[["Vuosi", "Kotimaiset yöpymiset, lkm Rovaniemi", "Ulkomaiset yöpymiset Rovaniemi"]]
temp_df["Ulkomaiset yöpymiset Rovaniemi"] = temp_df["Ulkomaiset yöpymiset Rovaniemi"].str.replace(".", "")
temp_df["Ulkomaiset yöpymiset Rovaniemi"] = pd.to_numeric(temp_df["Ulkomaiset yöpymiset Rovaniemi"])
vuosiroikudf = temp_df.groupby(by="Vuosi").sum()
st.dataframe(vuosiroikudf)
st.line_chart(vuosiroikudf)#, y=["Kotimaiset yöpymiset, lkm Rovaniemi", "Ulkomaiset yöpymiset Rovaniemi"])



# ==============================================================================
# An area_chart of a chosen metric.
st.header("An area_chart of a chosen metric.")

# Tunnilla tehty
#huone_vuode_df = rovaniemi_df[["Huoneet, lkm Rovaniemi", "Vuoteet, lkm Rovaniemi"]]
st.text("Tunnilla tehty")
st.area_chart(rovaniemi_df, x="Kuukausi", y=["Huoneet, lkm Rovaniemi", "Vuoteet, lkm Rovaniemi"])

# Omia kokeiluja
st.text("Omia kokeiluja")
# Poistetaan stringidatasta piste, muutetaan data numeeriseksi
rovaniemi_df["Yöpymisen keskihinta Rovaniemi"] = rovaniemi_df["Yöpymisen keskihinta Rovaniemi"].str.replace(".", "")
rovaniemi_df["Yöpymisen keskihinta Rovaniemi"] = pd.to_numeric(rovaniemi_df["Yöpymisen keskihinta Rovaniemi"])
rovaniemi_df["Huoneen keskihinta Rovaniemi"] = rovaniemi_df["Huoneen keskihinta Rovaniemi"].str.replace(".", "")
rovaniemi_df["Huoneen keskihinta Rovaniemi"] = pd.to_numeric(rovaniemi_df["Huoneen keskihinta Rovaniemi"])

# Koska luvuista poistettiin piste, lukujen todellinen arvo 100 kertaistui. 
# Jaetaan siis arvot sadalla, jotta saadaan todelliset lukemat näkyviin.
rovaniemi_df["Yöpymisen keskihinta Rovaniemi"] = rovaniemi_df["Yöpymisen keskihinta Rovaniemi"] / 100
rovaniemi_df["Huoneen keskihinta Rovaniemi"] = rovaniemi_df["Huoneen keskihinta Rovaniemi"] / 100

st.area_chart(rovaniemi_df, x="Vuosi", y=["Huoneen keskihinta Rovaniemi", "Yöpymisen keskihinta Rovaniemi"])



# ==============================================================================
# Compare with another municipality: load a second CSV + overlay on a chart.
st.header("Compare with another municipality: load a second CSV + overlay on a chart.")
rovaniemiC_df = rovaniemi_df[["Vuosi", "Yöpymiset, lkm Rovaniemi"]].groupby(by="Vuosi").sum()

oulu_df = pd.read_csv("https://pxdata.stat.fi/PxWeb/sq/f89e6f51-a1f6-4067-9606-192a9911fc0d", encoding="latin-1")
oulu_df[["Vuosi", "Kuukausi_num"]] = oulu_df["Kuukausi"].str.split("M", expand=True)
oulu_df["Yöpymiset, lkm Oulu"] = pd.to_numeric(oulu_df["Yöpymiset, lkm Oulu"])
ouluC_df = oulu_df[["Vuosi", "Yöpymiset, lkm Oulu"]].groupby(by="Vuosi").sum()

# Check the dataframe in streamlist app
#rovaniemiC_df
#ouluC_df

combined_df = rovaniemiC_df.merge(ouluC_df, on="Vuosi", how="left")
st.line_chart(combined_df)



# ==============================================================================
# Download button to export the comparison data.

