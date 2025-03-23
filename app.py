import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Set up the Streamlit app (MUST BE THE FIRST COMMAND)
st.set_page_config(page_title="Stock Tracker", layout="centered")

# Custom CSS for styling (hide sidebar)
st.markdown(
    """
    <style>
    /* Hide the sidebar */
    section[data-testid="stSidebar"] {
        display: none;
    }
    /* Remove max-width and center content */
    .stApp {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 20px;
    }
    /* Skyblue strip for indices */
    .indices-strip {
        background-color: skyblue;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        width: 100%;
    }
    /* Black navbar */
    .navbar {
        background-color: black;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
        width: 100%;
    }
    .navbar a {
        color: white;
        margin: 0 15px;
        text-decoration: none;
        font-weight: bold;
    }
    .navbar a:hover {
        color: skyblue;
    }
    /* Footer */
    .footer {
        background-color: black;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin-top: 20px;
        text-align: center;
        width: 100%;
    }
    /* Container for stock price and percentage change */
    .stock-info-container {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: left;
        width: 100%;
    }
    /* Table styling */
    .dataframe {
        width: 100%;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to fetch index data
def get_indices():
    indices = {"^NSEI": "NIFTY 50", "^BSESN": "SENSEX", "^NSEBANK": "BANKNIFTY", "^CNXIT": "NIFTY IT"}
    data = {}
    for symbol, name in indices.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
            last_price = hist['Close'].iloc[-1] if not hist.empty else "No Data"
            prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else last_price
            change = ((last_price - prev_close) / prev_close) * 100 if prev_close != 0 else 0
            data[name] = (last_price, change)
        except Exception as e:
            data[name] = ("Error", 0)
    return data

# Function to fetch stock data
def get_stock_data(symbol, period="6mo", interval="1d"):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period, interval=interval)
        if hist.empty:
            return None, "No data found for the given stock symbol. Please check and try again."
        return hist, None
    except Exception as e:
        return None, f"Error: {e}"

# Function to fetch stock price and percentage change
def get_stock_price_change(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="2d")  # Fetch last 2 days of data
        if hist.empty:
            return None, None, "No data found for the given stock symbol."
        last_price = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2]
        change = ((last_price - prev_close) / prev_close) * 100
        return last_price, change, None
    except Exception as e:
        return None, None, f"Error: {e}"

# Function to fetch financials
def get_financials(symbol):
    try:
        stock = yf.Ticker(symbol)
        balance_sheet = stock.balance_sheet
        financials = stock.financials
        return balance_sheet, financials
    except Exception as e:
        return None, None

# Function to format numbers (e.g., 1000000 -> 1M)
def format_number(value):
    if pd.isna(value):
        return "N/A"
    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif abs(value) >= 1_000:
        return f"{value / 1_000:.2f}K"
    else:
        return f"{value:.2f}"

# Black Navbar
st.markdown(
    """
    <div class="navbar">
        <a href="/">Home</a>
        <a href="/search">Search</a>
        <a href="/news">News</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Title and header
st.title("📈 Stock Tracker")
st.write("Your one-stop solution for stock market insights.")

# Skyblue strip for Market Indices
st.markdown('<div class="indices-strip">', unsafe_allow_html=True)
st.write("### Market Indices")
indices = get_indices()
cols = st.columns(len(indices))
for i, (index, (price, change)) in enumerate(indices.items()):
    cols[i].metric(
        label=index,
        value=f"{price:.2f}" if isinstance(price, (int, float)) else price,
        delta=f"{change:.2f}%"
    )
st.markdown('</div>', unsafe_allow_html=True)

# Stock Search Feature with Autocomplete
st.write("### 🔍 Type a Company Name or Brand to Search")
stock_symbol = st.text_input("Enter Stock Symbol (e.g., RELIANCE.NS, TCS.NS, 500325.BO)", "RELIANCE.NS")

# Display Stock Price and Percentage Change in a Container
if stock_symbol:
    last_price, change, error_msg = get_stock_price_change(stock_symbol)
    if error_msg:
        st.error(error_msg)
    else:
        st.markdown(
            f"""
            <div class="stock-info-container">
                <h3>📊 {stock_symbol}</h3>
                <p><strong>Current Price:</strong> {last_price:.2f}</p>
                <p><strong>Percentage Change:</strong> <span style="color: {'green' if change >= 0 else 'red'}">{change:.2f}%</span></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Advanced Charting Options
st.write("### 📊 Advanced Charting")
timeframe = st.selectbox("Select Timeframe", ["1mo", "3mo", "6mo", "1y", "2y"])
interval = st.selectbox("Select Interval", ["1d", "1wk", "1mo"])
indicators = st.multiselect("Add Technical Indicators", ["SMA", "EMA", "RSI", "MACD"])

# Fetch and display stock data
if stock_symbol:
    hist_data, error_msg = get_stock_data(stock_symbol, period=timeframe, interval=interval)
    if error_msg:
        st.error(error_msg)
    else:
        # Display Stock Price Chart
        st.write(f"### 📊 {stock_symbol} Stock Price Chart")
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=hist_data.index,
            open=hist_data['Open'],
            high=hist_data['High'],
            low=hist_data['Low'],
            close=hist_data['Close'],
            name='Candlestick Chart'
        ))

        # Add Technical Indicators
        if "SMA" in indicators:
            fig.add_trace(go.Scatter(
                x=hist_data.index,
                y=hist_data['Close'].rolling(window=20).mean(),
                name="SMA (20)",
                line=dict(color='blue', width=2)
            ))
        if "EMA" in indicators:
            fig.add_trace(go.Scatter(
                x=hist_data.index,
                y=hist_data['Close'].ewm(span=20, adjust=False).mean(),
                name="EMA (20)",
                line=dict(color='orange', width=2)
            ))

        fig.update_layout(
            title=f"{stock_symbol} Stock Price Movement",
            xaxis_title="Date",
            yaxis_title="Price",
            xaxis_rangeslider_visible=True,
            template="plotly_dark",
            height=600,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Fetch and Display Financials
        st.write("### 💰 Financial Statements")
        balance_sheet, financials = get_financials(stock_symbol)

        if balance_sheet is not None:
            st.write("#### Balance Sheet")
            st.dataframe(balance_sheet.style.format(format_number), use_container_width=True)
        else:
            st.warning("Balance sheet data not available.")

        if financials is not None:
            st.write("#### Income Statement")
            st.dataframe(financials.style.format(format_number), use_container_width=True)
        else:
            st.warning("Financial statement data not available.")

# Footer
st.markdown(
    """
    <div class="footer">
        <p>© 2023 Stock Tracker. All rights reserved.</p>
        <br>
        <p>A Project By Sai Harshith B N</p>
    </div>
    """,
    unsafe_allow_html=True,
)
