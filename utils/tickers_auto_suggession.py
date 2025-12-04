import streamlit as st
import pandas as pd

# -------------------- LOAD TICKERS --------------------
@st.cache_data
def load_tickers():
    return pd.read_csv("utils/tickers.csv")   # Must contain Symbol, Name

df = load_tickers()

# -------------------- AUTOCOMPLETE FUNCTION --------------------
def search_ticker(query):
    query = query.strip()
    if not query:
        return df.iloc[0:0]   # empty DataFrame

    query_upper = query.upper()
    query_lower = query.lower()

    results = df[
        df["Symbol"].str.startswith(query_upper) |
        df["Security"].str.lower().str.startswith(query_lower)
    ]

    return results.head(10)