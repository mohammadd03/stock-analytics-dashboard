import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="📈 Stock Analytics Dashboard", layout="wide")

st.title("📊 Stock Analytics Dashboard")

# Sidebar Inputs
st.sidebar.header("🔧 Select Options")
stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, MSFT, TSLA)", "AAPL")

# Date Inputs
today = date.today()
default_start = today - timedelta(days=180)
start_date = st.sidebar.date_input("Start Date", default_start)
end_date = st.sidebar.date_input("End Date", today)

interval = st.sidebar.selectbox("Select Interval", ["1d", "1wk", "1mo"])

# Download Data
try:
    stock = yf.download(stock_symbol, start=start_date, end=end_date, interval=interval)

    # Fix MultiIndex columns if present
    if isinstance(stock.columns, pd.MultiIndex):
        stock.columns = stock.columns.get_level_values(0)

    if stock.empty:
        st.error("❌ No data found. Please check the stock symbol or date range.")
    else:
        # Add Moving Averages
        stock["SMA_20"] = stock["Close"].rolling(window=20).mean()
        stock["SMA_50"] = stock["Close"].rolling(window=50).mean()

        # Show metrics
        st.subheader(f"📌 Stock Summary for {stock_symbol.upper()}")
        start_price = stock["Close"].iloc[0]
        end_price = stock["Close"].iloc[-1]
        percent_change = ((end_price - start_price) / start_price) * 100

        col1, col2, col3 = st.columns(3)
        col1.metric("Start Price", f"${start_price:.2f}")
        col2.metric("End Price", f"${end_price:.2f}")
        col3.metric("Change", f"{percent_change:.2f}%")

        # Show line chart
        st.subheader("📈 Price Trend with Moving Averages")
        st.line_chart(stock[["Close", "SMA_20", "SMA_50"]])

        # Show raw data
        st.subheader("📄 Raw Data")
        st.dataframe(stock.tail(50))

except Exception as e:
    st.error(f"⚠️ Error: {e}")
