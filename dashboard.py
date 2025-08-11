# dashboard.py - TradingView embed + simple dashboard
import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
from datetime import datetime, timedelta

st.set_page_config(page_title="Shanil Market Dashboard", layout="wide")
st.title("📊 Shanil's Market Dashboard")
st.markdown("Live prices, TradingView chart, news & key liquidity levels")

# ----- Asset mapping (display name -> Yahoo ticker and TradingView symbol) -----
ASSETS = {
    "Gold (XAU/USD)": {"yahoo": "XAUUSD=X", "tv": "OANDA:XAUUSD"},
    "EUR/USD":        {"yahoo": "EURUSD=X",  "tv": "OANDA:EURUSD"},
    "GBP/USD":        {"yahoo": "GBPUSD=X",  "tv": "OANDA:GBPUSD"},
    "USD/JPY":        {"yahoo": "JPY=X",     "tv": "OANDA:USDJPY"},  # note Yahoo shows JPY=X as USD/JPY
    "BTC/USD":        {"yahoo": "BTC-USD",   "tv": "BITSTAMP:BTCUSD"},
    "SPY":            {"yahoo": "SPY",       "tv": "NYSEARCA:SPY"}
}

# ----- Sidebar controls -----
st.sidebar.header("Settings")
asset_name = st.sidebar.selectbox("Select asset", list(ASSETS.keys()), index=0)
period = st.sidebar.selectbox("Period", ["5d", "1mo", "3mo"], index=1)
interval = st.sidebar.selectbox("Interval", ["15m", "30m", "1h", "1d"], index=0)
show_tv = st.sidebar.checkbox("Show TradingView chart", True)

# resolve tickers
yahoo_ticker = ASSETS[asset_name]["yahoo"]
tv_symbol = ASSETS[asset_name]["tv"]

st.subheader(f"🔎 {asset_name} Overview")

# ----- TradingView embed (interactive) -----
if show_tv:
    # create a safe html container id by replacing ":" with "_"
    container_id = f"tradingview_{tv_symbol.replace(':','_')}"
    tradingview_html = f"""
    <div class="tradingview-widget-container">
      <div id="{container_id}"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "width": "100%",
        "height": 520,
        "symbol": "{tv_symbol}",
        "interval": "60",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "hide_top_toolbar": false,
        "save_image": false,
        "container_id": "{container_id}"
      }});
      </script>
    </div>
    """
    components.html(tradingview_html, height=560)
else:
    st.info("TradingView chart is hidden. Enable it from the sidebar to view the interactive chart.")

# ----- Fetch Yahoo data for liquidity levels (fallback) -----
st.subheader("📍 Key Liquidity Levels (yfinance)")
try:
    data = yf.download(yahoo_ticker, period=period, interval=interval, progress=False)
except Exception as e:
    st.warning("yfinance fetch failed: " + str(e))
    data = None

if data is not None and not data.empty:
    # try to compute yesterday's high/low (best effort)
    try:
        # ensure datetime index
        df = data.copy()
        df = df.reset_index()
        # use last two rows if timeframe too short
        if len(df) >= 2:
            yesterday_row = df.iloc[-2]
            st.write(f"Yesterday's High: **{yesterday_row['High']}**")
            st.write(f"Yesterday's Low: **{yesterday_row['Low']}**")
        else:
            st.write("Not enough historical rows to compute yesterday's levels for this interval.")
    except Exception as e:
        st.write("Could not compute yesterday's levels:", e)
else:
    st.write("No intraday data available for the chosen symbol/interval. Try different Period/Interval or rely on the TradingView chart above.")

# ----- News (simple links fallback) -----
st.subheader("📰 Latest Market News")
st.markdown("- NewsAPI key not set in this app — using general news links instead.")
st.markdown("- [Investing.com News](https://www.investing.com/news/)")
st.markdown("- [ForexFactory Calendar](https://www.forexfactory.com/calendar.php)")

st.markdown("---")
st.caption("Tip: use the sidebar to change asset, period and whether to show the TradingView chart.")
