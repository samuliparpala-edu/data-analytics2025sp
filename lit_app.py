import streamlit as st
import pandas as pd

# HUOM! Data on aina hyvä rajata pelkästään siihen, mitä dataa käytetään

rovaniemi_df = pd.read_csv("https://pxdata.stat.fi/PxWeb/sq/4c02da84-4baf-4fec-8c45-101aa473f885", encoding="latin-1")
rovaniemi_df[["Vuosi", "Kuukausi_num"]] = rovaniemi_df["Kuukausi"].str.split("M", expand=True)

# Load one municipality via saved-query CSV URL (PxWeb).
# Show a data table for that municipality.
st.dataframe(rovaniemi_df)

# Simple overall trend (line chart) for a chosen metric.
huone_aste_roi_df = rovaniemi_df[["Kuukausi", "Huonekäyttöaste, % Rovaniemi"]]
st.line_chart(huone_aste_roi_df, x="Kuukausi", y="Huonekäyttöaste, % Rovaniemi")

# Yearly totals (bar chart) for nights spent.
# "Yöpymiset, lkm Rovaniemi"
# Tunnilla tehty
vuosi_yo_roi_df = rovaniemi_df[["Vuosi", "Kuukausi", "Yöpymiset, lkm Rovaniemi"]].groupby(by="Vuosi").sum()
st.dataframe(vuosi_yo_roi_df)
#st.bar_chart(vuosi_yo_roi_df, x="Vuosi", y="Yöpymiset, lkm Rovaniemi")
st.bar_chart(vuosi_yo_roi_df, y="Yöpymiset, lkm Rovaniemi")

# Oma ratkaisu
yearly_df = rovaniemi_df.groupby(by="Vuosi", as_index=False).agg({"Yöpymiset, lkm Rovaniemi": "sum"})
st.bar_chart(yearly_df, x="Vuosi", y="Yöpymiset, lkm Rovaniemi")
