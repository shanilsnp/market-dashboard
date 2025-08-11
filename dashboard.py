import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta

# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(page_title="Shanil Market Dashboard", layout="wide")

st.title("📊 Shanil's Market Dashboard")
st.markdown("Live prices, charts, news & calendar — automated daily")

# ----------------------------
# Sidebar settings
# ----------------------------
st.sidebar.header("Settings")
ticker = st.sidebar.selectbox("Select Asset", ["XAUUSD=X", "EURUSD=X", "GBPUSD=X", "USDJPY=X", "BTC-USD", "SPY"])
period = st.sidebar.selectbox("Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y"])
interval = st.sidebar.selectbox("Interval", ["1m", "5m", "15m", "30m", "1h", "1d"])

# ----------------------------
# Fetch Data
# ----------------------------
st.subheader(f"💹 {ticker} Chart")
data = yf.download(ticker, period=period, interval=interval)

fig = go.Figure(data=[go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close']
)])
fig.update_layout(height=500, xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Economic Calendar Embed
# ----------------------------
st.subheader("🗓 Economic Calendar")
st.markdown("[View Full Calendar on ForexFactory](https://www.forexfactory.com/calendar)")

# ----------------------------
# News Feed
# ----------------------------
st.subheader("📰 Latest Market News")

# You can replace with your NewsAPI.org key
NEWS_API_KEY = ""  # Optional: Put your API key here
if NEWS_API_KEY:
    url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    for article in articles[:5]:
        st.markdown(f"**[{article['title']}]({article['url']})**")
else:
    st.markdown("NewsAPI key not set — showing [Investing.com News](https://www.investing.com/news/) instead.")

# ----------------------------
# Liquidity Levels Example (Yesterday's High & Low)
# ----------------------------
st.subheader("📍 Key Liquidity Levels")
if not data.empty:
    yesterday = data.iloc[-2]
    st.write(f"Yesterday's High: {yesterday['High']}")
    st.write(f"Yesterday's Low: {yesterday['Low']}")
