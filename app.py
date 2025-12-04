import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from utils.tickers_auto_suggession import search_ticker
import os

# -------------------- UI START --------------------
st.title("Backtesting Engine (SMA Crossover)")


# -------------------- AUTOCOMPLETE INPUT --------------------
query = st.text_input("Type a stock symbol or name")

selected_ticker = None

if query:
    suggestions = search_ticker(query)

    if len(suggestions) > 0:

        # Single-selection dropdown
        selected_option = st.selectbox(
            "Suggestions:",
            [f"{row.Symbol} — {row.Security}" for _, row in suggestions.iterrows()]
        )

        # Extract selected ticker (left side of " — ")
        selected_ticker = selected_option.split(" — ")[0]

        # Auto-fill the symbol box
        st.info(f"Selected Ticker: {selected_ticker}")

    else:
        st.warning("No matching ticker found.")


# -------------------- MAIN STOCK INPUT --------------------
# If user selected something from autocomplete → auto-fill it
if selected_ticker:
    symbol = st.text_input("Enter stock symbol", selected_ticker)
else:
    symbol = st.text_input("Enter stock symbol", "AAPL")



# -------------------- RUN BACKTEST --------------------
if st.button("Run Backtest"):
    BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
    res = requests.get(f"{BACKEND_URL}/backtest", params={"symbol": symbol})

    if res.status_code == 200:

        data = res.json()["data"]
        metrics = res.json()["metrics"]
        df = pd.DataFrame(data)

        st.write(df.head())

        st.subheader("Equity Curve")
        fig1 = px.line(df, x="Date", y="Equity_Curve")
        st.plotly_chart(fig1)

        st.subheader("Signals (Buy/Sell)")
        fig2 = px.line(df, x="Date", y=f"Close_{symbol}")
        fig2.add_scatter(
            x=df["Date"], 
            y=df[f"Close_{symbol}"], 
            mode="markers",
            marker=dict(color="green", size=8),
            name="Buy",
            visible="legendonly"
        )
        st.plotly_chart(fig2)

        st.subheader("Performance Metrics")
        st.json(metrics)

    else:
        st.error("Failed to fetch data")