import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="My Trading Signals", layout="wide")

st.title("🚀 My Trading Signal App")
st.markdown("**SMC + APA Strategy**")

symbol = st.text_input("Enter Symbol (e.g. AAPL, BTC-USD, TSLA)", "AAPL")
period = st.selectbox("Time Period", ["1mo", "3mo", "6mo", "1y"], index=3)

if st.button("🔥 Get Trading Signal"):
    with st.spinner("Analyzing..."):
        df = yf.download(symbol, period=period, progress=False)
        if df.empty:
            st.error("No data found. Try another symbol.")
        else:
            df['SMA50'] = df['Close'].rolling(50).mean()
            df['SMA200'] = df['Close'].rolling(200).mean()
            latest = df.iloc[-1]
            
            trend = "🟢 Bullish" if latest['SMA50'] > latest['SMA200'] else "🔴 Bearish"
            signal = "Strong Buy" if trend == "🟢 Bullish" else "Strong Sell"
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Current Price", f"${latest['Close']:.2f}")
            col2.metric("Signal", signal)
            col3.metric("Trend", trend)
            
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
            fig.update_layout(height=450, template="plotly_dark", title=f"{symbol} Chart")
            st.plotly_chart(fig, use_container_width=True)