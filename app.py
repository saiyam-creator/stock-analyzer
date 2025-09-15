# stock_analyzer_complete.py
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, time, timedelta
import math
import time

# -----------------------------
# Config / Dictionaries
# -----------------------------
st.set_page_config(
    page_title="Stock Analyzer — Complete", 
    layout="wide", 
    initial_sidebar_state="collapsed",
    page_icon="📈"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 0.5rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .market-header {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #e9ecef;
    }
    .index-card {
        background-color: white;
        padding: 12px;
        border-radius: 8px;
        margin: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
    }
    .index-name {
        font-weight: bold;
        font-size: 0.9rem;
        color: #495057;
    }
    .index-value {
        font-size: 1.1rem;
        font-weight: bold;
        color: #212529;
    }
    .positive {
        color: #28a745;
        font-weight: bold;
    }
    .negative {
        color: #dc3545;
        font-weight: bold;
    }
    .market-status {
        padding: 8px 12px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .market-open {
        background-color: #d4edda;
        color: #155724;
    }
    .market-closed {
        background-color: #f8d7da;
        color: #721c24;
    }
    .section-header {
        font-size: 1.5rem;
        color: #1f77b4;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 4px solid #1f77b4;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 4px 4px 0px 0px;
        background-color: #f0f2f6;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #1668a6;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Expand this dictionary to add more tickers
POPULAR_INDIAN_STOCKS = {
    "RELIANCE": "RELIANCE.NS",
    "TATA CONSULTANCY SERVICES": "TCS.NS",
    "HDFC BANK": "HDFCBANK.NS",
    "INFOSYS": "INFY.NS",
    "ICICI BANK": "ICICIBANK.NS",
    "HINDUSTAN UNILEVER": "HINDUNILVR.NS",
    "ITC": "ITC.NS",
    "BHARTI AIRTEL": "BHARTIARTL.NS",
    "LARSEN & TOUBRO": "LT.NS",
    "KOTAK MAHINDRA BANK": "KOTAKBANK.NS",
    "AXIS BANK": "AXISBANK.NS",
    "STATE BANK OF INDIA": "SBIN.NS",
    "BAJAJ FINANCE": "BAJFINANCE.NS",
    "HCL TECHNOLOGIES": "HCLTECH.NS",
    "MARUTI SUZUKI": "MARUTI.NS",
    "WIPRO": "WIPRO.NS",
    "ADANI ENTERPRISES": "ADANIENT.NS",
    "TATA MOTORS": "TATAMOTORS.NS",
    "SUN PHARMA": "SUNPHARMA.NS",
    "NESTLE INDIA": "NESTLEIND.NS",
    "ONGC": "ONGC.NS",
    "HDFC": "HDFC.NS",
    "DR. REDDY'S": "DRREDDY.NS",
    "21ST CENTURY MANAGEMENT SERVICES LIMITED": "21STCENMGM.NS",
    "3I INFOTECH LIMITED": "3IINFOTECH.NS",
    "3M INDIA LIMITED": "3MINDIA.NS",
    "8K MILES SOFTWARE SERVICES LIMITED": "8KMILES.NS",
    "A2Z INFRA ENGINEERING LIMITED": "A2ZINFRA.NS",
    "AARTI INDUSTRIES LIMITED": "AARTIIND.NS",
    "AARTI SURFACTANTS LIMITED": "AARTISURF.NS",
    "ABAN OFFSHORE LIMITED": "ABAN.NS",
    "ABB INDIA LIMITED": "ABB.NS",
    "ACC LIMITED": "ACC.NS",
    "ADANI GREEN ENERGY LIMITED": "ADANIGREEN.NS",
    "ADANI PORTS AND SPECIAL ECONOMIC ZONE LIMITED": "ADANIPORTS.NS",
    "ADANI POWER LIMITED": "ADANIPOWER.NS",
    "ADANI TRANSMISSION LIMITED": "ADANITRANS.NS",
    "ADITYA BIRLA CAPITAL LIMITED": "ADITYABIRLA.NS",
    "ADITYA BIRLA FASHION AND RETAIL LIMITED": "ABFRL.NS",
    "ADITYA BIRLA INSURANCE BROKERS LIMITED": "ABIBL.NS",
    "ADITYA BIRLA MONEY LIMITED": "ABML.NS",
    "ADITYA BIRLA SUN LIFE AMC LIMITED": "ABSLAMC.NS",
    "ADITYA BIRLA SUN LIFE INSURANCE LIMITED": "ABSLI.NS",
    "AIA ENGINEERING LIMITED": "AIAENG.NS",
    "AJANTA PHARMA LIMITED": "AJANTPHARM.NS",
    "AKZO NOBEL INDIA LIMITED": "AKZOINDIA.NS",
    "ALANKIT LIMITED": "ALANKIT.NS",
    "ALBERT DAVID LIMITED": "ALBERTDAVID.NS",
    "ALEMBIC LIMITED": "ALEMBICLTD.NS",
    "ALEMBIC PHARMACEUTICALS LIMITED": "ALBPHARMA.NS",
    "ALKEM LABORATORIES LIMITED": "ALKEM.NS",
    "ALLAHABAD BANK LIMITED": "ALLBANK.NS",
    "ALLSEC TECHNOLOGIES LIMITED": "ALLSEC.NS",
    "AMARA RAJA BATTERIES LIMITED": "AMARAJABAT.NS",
    "AMBUJA CEMENTS LIMITED": "AMBUJACEM.NS",
    "ANDHRA PAPER LIMITED": "ANDHRAPAP.NS",
    "ANDHRA PETROCHEMICALS LIMITED": "ANDHRAPETRO.NS",
    "ANDHRA SUGARS LIMITED": "ANDHRASUG.NS",
    "ANGEL ONE LIMITED": "ANGELONE.NS",
    "ANUPAM RASAYAN INDIA LIMITED": "ANURAS.NS",
    "APOLLO HOSPITALS ENTERPRISE LIMITED": "APOLLOHOSP.NS",
    "APOLLO TYRE LIMITED": "APOLLOTYRE.NS",
    "ARVIND LIMITED": "ARVIND.NS",
    "ASHOK LEYLAND LIMITED": "ASHOKLEY.NS",
    "ASIAN PAINTS LIMITED": "ASIANPAINT.NS",
    "ASSAM COMPANY INDIA LIMITED": "ASSAMCO.NS",
    "ASTRAL LIMITED": "ASTRAL.NS",
    "ATUL LIMITED": "ATUL.NS",
    "AU SMALL FINANCE BANK LIMITED": "AUBANK.NS",
    "AURIONPRO SOLUTIONS LIMITED": "AURIONPRO.NS",
    "AUTO CORPORATION LIMITED": "AUTOCORP.NS",
    "B P C L LIMITED": "BPCL.NS",
    "BALAJI TELEFILMS LIMITED": "BALAJITELE.NS",
    "BANK OF BARODA LIMITED": "BANKBARODA.NS",
    "BANK OF INDIA LIMITED": "BANKINDIA.NS",
    "BATA INDIA LIMITED": "BATAINDIA.NS",
    "BEML LIMITED": "BEML.NS",
    "BERGER PAINTS INDIA LIMITED": "BERGEPAINT.NS",
    "BHEL LIMITED": "BHEL.NS",
    "BIOCON LIMITED": "BIOCON.NS",
    "BIRLA CORPORATION LIMITED": "BIRLACORPN.NS",
    "BIRLASOFT LIMITED": "BIRLASOFT.NS",
    "BOSCH LIMITED": "BOSCHLTD.NS",
    "BRITANNIA INDUSTRIES LIMITED": "BRITANNIA.NS",
    "CADILA HEALTHCARE LIMITED": "CADILAHC.NS",
    "CANARA BANK LIMITED": "CANBK.NS",
    "CAPACITE INFRA PROJECTS LIMITED": "CAPACITE.NS",
    "CAPLIN POINT LABORATORIES LIMITED": "CAPLIPOINT.NS",
    "CASTROL INDIA LIMITED": "CASTROLIND.NS",
    "CENTRAL BANK OF INDIA LIMITED": "CENTRALBK.NS",
    "CENTURY TEXTILES AND INDUSTRIES LIMITED": "CENTURYTEX.NS",
    "CERA SANITARYWARE LIMITED": "CERA.NS",
    "CHAMBAL FERTILISERS AND CHEMICALS LIMITED": "CHAMBLFERT.NS",
    "CHENNAI PETROLEUM CORPORATION LIMITED": "CPCL.NS",
    "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED": "CHOLAFIN.NS",
    "CIPLA LIMITED": "CIPLA.NS",
    "COAL INDIA LIMITED": "COALINDIA.NS",
    "COLGATE-PALMOLIVE (INDIA) LIMITED": "COLPAL.NS",
    "CONTAINER CORPORATION OF INDIA LIMITED": "CONCOR.NS",
    "COROMANDEL INTERNATIONAL LIMITED": "COROMANDEL.NS",
    "CUMMINS INDIA LIMITED": "CUMMINSIND.NS",
    "DABUR INDIA LIMITED": "DABUR.NS",
    "DCB BANK LIMITED": "DCBBANK.NS",
    "DENA BANK LIMITED": "DENABANK.NS",
    "DIVI'S LABORATORIES LIMITED": "DIVISLAB.NS",
    "DLF LIMITED": "DLF.NS",
    "EICHER MOTORS LIMITED": "EICHERMOT.NS",
    "ESCORTS LIMITED": "ESCORTS.NS",
    "EXIDE INDUSTRIES LIMITED": "EXIDEIND.NS",
    "FEDERAL BANK LIMITED": "FEDERALBNK.NS",
    "FINO PAYTECH LIMITED": "FINOLEXIND.NS",
    "GAIL (INDIA) LIMITED": "GAIL.NS",
    "GODREJ CONSUMER PRODUCTS LIMITED": "GODREJCP.NS",
    "GODREJ INDUSTRIES LIMITED": "GODREJIND.NS",
    "GODREJ PROPERTIES LIMITED": "GODREJPROP.NS",
    "GRASIM INDUSTRIES LIMITED": "GRASIM.NS",
    "GUJARAT GAS LIMITED": "GUJGASLTD.NS",
    "GUJARAT MINERAL DEVELOPMENT CORPORATION LIMITED": "GMDCLTD.NS",
    "GUJARAT STATE FERTILIZERS AND CHEMICALS LIMITED": "GSFC.NS",
    "HAVELLS INDIA LIMITED": "HAVELLS.NS",
    "HDFC BANK": "HDFCBANK.NS",
    "HDFC": "HDFC.NS",
    "HAVELLS INDIA": "HAVELLS.NS", 
    "HCL TECHNOLOGIES": "HCLTECH.NS",
    "HDFC ASSET MANAGEMENT COMPANY LIMITED": "HDFCAMC.NS",
    "HERO MOTOCORP LIMITED": "HEROMOTOCO.NS",
    "HINDALCO INDUSTRIES LIMITED": "HINDALCO.NS",
    "HINDUSTAN COPPER LIMITED": "HINDCOPPER.NS",
    "HINDUSTAN PETROLEUM CORPORATION LIMITED": "HINDPETRO.NS",
    "HINDUSTAN ZINC LIMITED": "HINDZINC.NS",
    "IDFC FIRST BANK LIMITED": "IDFCFIRSTB.NS",
    "IDFC LIMITED": "IDFC.NS",
    "IFB INDUSTRIES LIMITED": "IFBINDUSTRIES.NS",
    "IFCI LIMITED": "IFCI.NS",
    "IG PETROCHEMICALS LIMITED": "IGPETRO.NS",
    "IIFL FINANCE LIMITED": "IIFL.NS",
    "IIFL SECURITIES LIMITED": "IIFLSEC.NS",
    "INDIAN BANK LIMITED": "INDIANB.NS",
    "INDIAN HOTELS COMPANY LIMITED": "INDHOTEL.NS",
    "INDOCO REMEDIES LIMITED": "INDOCO.NS",
    "INDUSIND BANK LIMITED": "INDUSINDBK.NS",
    "INDUSTRIAL INVESTMENT TRUST LIMITED": "IITL.NS",
    "INDUS TOWERS LIMITED": "INDUSTOWER.NS",
    "INFIBEAM AVENUES LIMITED": "INFIBEAM.NS",
    "INTERGLOBE AVIATION": "INDIGO.NS",
    "IOC": "IOC.NS",
    "JAIN IRRIGATION SYSTEMS": "JISLJALEQS.NS",
    "JINDAL STEEL & POWER": "JINDALSTEL.NS",
    "JSW STEEL": "JSWSTEEL.NS",
    "JUBILANT FOODWORKS": "JUBLFOOD.NS",
    "JUBILANT PHARMA": "JUBLPHARMA.NS",
    "L&T TECHNOLOGIES SERVICES": "LTTS.NS",
    "LUPIN": "LUPIN.NS",
    "M&M": "MM.NS",
    "MAHINDRA & MAHINDRA FINANCIAL SERVICES": "MMFSL.NS",
    "MAHINDRA LIFESPACE DEVELOPERS": "MINDTREE.NS",
    "MARICO": "MARICO.NS",
    "MOTHERSON SUMI SYSTEMS": "MOTHERSUMI.NS",
    "MUTHOOT FINANCE": "MUTHOOTFIN.NS",
    "NTPC": "NTPC.NS",
    "POWER GRID CORPORATION OF INDIA": "POWERGRID.NS",
    "SAIL": "SAIL.NS",
    "SHREE CEMENT": "SHREECEM.NS",
    "SIEMENS": "SIEMENS.NS",
    "TATA STEEL": "TATASTEEL.NS",
    "TECH MAHINDRA": "TECHM.NS",
    "ULTRATECH CEMENT": "ULTRACEMCO.NS",
    "UPL": "UPL.NS",
    "YES BANK": "YESBANK.NS",
    "ZEE ENTERTAINMENT ENTERPRISES": "ZEEL.NS",
    "ASIAN PAINTS": "ASIANPAINT.BO",
    "AXIS BANK": "AXISBANK.BO",
    "BAJAJ FINANCE": "BAJFINANCE.BO",
    "BAJAJ FINSERV": "BAJAJFINSV.BO",
    "BHARAT ELECTRONICS": "BEL.BO",
    "BHARTI AIRTEL": "BHARTIARTL.BO",
    "Eternal": "ETERNAL.BO",
    "HCL Technologies": "HCLTECH.BO",
    "HDFC Bank": "HDFCBANK.BO",
    "Hindustan Unilever": "HINDUNILVR.BO",
    "Tata Motors": "TATAMOTORS.BO",
    "Tata Steel": "TATASTEEL.BO",
    "Tech Mahindra": "TECHM.BO",
    "Titan Company": "TITAN.BO",
    "Trent": "TRENT.BO",
    "UltraTech Cement": "ULTRACEMCO.BO",
    "Reliance Industries": "RELIANCE.BO"
}

INDIAN_INDICES = {
    "NIFTY 50": "^NSEI",
    "NIFTY BANK": "^NSEBANK",
    "SENSEX": "^BSESN",
    "NIFTY IT": "^CNXIT",
    "NIFTY MIDCAP 100": "^NSEMDCP100",
}

INDIAN_ETFS = {
    "NIFTY BEES": "NIFTYBEES.NS",
    "BANK BEES": "BANKBEES.NS",
    "GOLD BEES": "GOLDBEES.NS",
    "HDFC NIFTY ETF": "HDFCNIFETF.NS",
}

# Combined mapping for quick lookup
COMBINED_MAP = {**POPULAR_INDIAN_STOCKS, **INDIAN_INDICES, **INDIAN_ETFS}

# -----------------------------
# Change the import statement at the top of your file:
from datetime import datetime, timedelta, time  # Add 'time' to the import

# Then in the get_market_status() function:
def get_market_status():
    """Check if Indian stock market is open"""
    now = datetime.now()
    # Convert to IST (UTC+5:30)
    ist_now = now + timedelta(hours=5, minutes=30)
    
    # Market hours: 9:15 AM to 3:30 PM IST, Monday to Friday
    market_open = time(9, 15)  # Now this will work correctly
    market_close = time(15, 30)
    
    # Check if it's a weekday
    if ist_now.weekday() >= 5:  # 5=Saturday, 6=Sunday
        return False, ist_now
    
    # Check if current time is within market hours
    current_time = ist_now.time()
    if market_open <= current_time <= market_close:
        return True, ist_now
    
    return False, ist_now

@st.cache_data(ttl=60)
def get_index_data():
    """Get current data for major indices"""
    indices_data = {}
    for name, ticker in INDIAN_INDICES.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period='1d', interval='1m')
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_close = stock.info.get('regularMarketPreviousClose', current_price)
                change = current_price - prev_close
                change_percent = (change / prev_close) * 100
                
                indices_data[name] = {
                    'current': current_price,
                    'change': change,
                    'change_percent': change_percent,
                    'ticker': ticker
                }
        except:
            continue
    
    return indices_data

def display_market_header():
    """Display market header with indices and market status"""
    # Get market data
    indices_data = get_index_data()
    market_open, current_time = get_market_status()
    
    # Create header
    st.markdown('<div class="market-header">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; margin-bottom: 15px;">📈 Live Market Overview</h3>', unsafe_allow_html=True)
    
    # Create columns for indices
    cols = st.columns(len(indices_data) + 1)
    
    # Display each index
    for idx, (index_name, data) in enumerate(indices_data.items()):
        with cols[idx]:
            change_class = "positive" if data['change'] >= 0 else "negative"
            change_icon = "📈" if data['change'] >= 0 else "📉"
            
            st.markdown(f"""
            <div class="index-card">
                <div class="index-name">{index_name}</div>
                <div class="index-value">₹{data['current']:,.2f}</div>
                <div class="{change_class}">
                    {change_icon} {data['change']:+.2f} ({data['change_percent']:+.2f}%)
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Display market status in the last column
    with cols[-1]:
        status_class = "market-status market-open" if market_open else "market-status market-closed"
        status_text = "OPEN" if market_open else "CLOSED"
        st.markdown(f"""
        <div class="index-card">
            <div class="index-name">Market Status</div>
            <div class="{status_class}">{status_text}</div>
            <div style="font-size: 0.8rem; margin-top: 5px;">
                IST: {current_time.strftime("%Y-%m-%d %H:%M:%S")}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Helpers: formatting
# -----------------------------
def format_large_number(x):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "N/A"
    try:
        x = float(x)
    except Exception:
        return str(x)
    if abs(x) >= 1e12:
        return f"{x/1e12:.2f} T"
    if abs(x) >= 1e9:
        return f"{x/1e9:.2f} B"
    if abs(x) >= 1e6:
        return f"{x/1e6:.2f} M"
    if abs(x) >= 1e3:
        return f"{x/1e3:.2f} K"
    return f"{x:.2f}"

def format_pct(x):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "N/A"
    return f"{x*100:.2f}%" if abs(x) < 100 else f"{x:.2f}"

# -----------------------------
# Caching network calls
# -----------------------------
# Cache the heavy network calls to reduce rate-limits and speed up UI
@st.cache_data(ttl=60)  # cache for 60s
def fetch_history(ticker, period="1y", interval="1d"):
    try:
        t = yf.Ticker(ticker)
        df = t.history(period=period, interval=interval)
        if df is None:
            return pd.DataFrame()
        # Standardize index
        df = df.sort_index()
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def fetch_info(ticker):
    try:
        t = yf.Ticker(ticker)
        return t.info or {}
    except Exception:
        return {}

@st.cache_data(ttl=30)
def fetch_today_minute(ticker):
    try:
        t = yf.Ticker(ticker)
        df = t.history(period="1d", interval="1m")
        return df
    except Exception:
        return pd.DataFrame()

# -----------------------------
# Technical indicators
# -----------------------------
def compute_indicators(df):
    df = df.copy()
    if df.empty or "Close" not in df.columns:
        return df
    # Moving averages
    df["SMA20"] = df["Close"].rolling(window=20, min_periods=1).mean()
    df["SMA50"] = df["Close"].rolling(window=50, min_periods=1).mean()
    df["SMA200"] = df["Close"].rolling(window=200, min_periods=1).mean()
    # MACD
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()
    # RSI (14)
    delta = df["Close"].diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    roll_up = up.rolling(14, min_periods=1).mean()
    roll_down = down.rolling(14, min_periods=1).mean()
    rs = roll_up / roll_down.replace(0, np.nan)
    df["RSI"] = 100 - (100 / (1 + rs))
    return df

# -----------------------------
# Peers detection & metrics
# -----------------------------
@st.cache_data(ttl=300)
def find_peers(ticker, candidate_map):
    info = fetch_info(ticker)
    industry = info.get("industry") or info.get("sector") or ""
    if not industry:
        return []
    peers = []
    for name, sym in candidate_map.items():
        if sym == ticker:
            continue
        inf = fetch_info(sym)
        if not inf:
            continue
        if (inf.get("industry") and inf.get("industry") == industry) or (inf.get("sector") and inf.get("sector") == industry):
            peers.append(sym)
    return peers

def compute_peers_metrics(peers_list):
    if not peers_list:
        return {"pe_avg": None, "count": 0}
    pes = []
    mcs = []
    rows = []
    for p in peers_list:
        inf = fetch_info(p)
        if not inf:
            continue
        pe = inf.get("trailingPE")
        mc = inf.get("marketCap")
        if pe:
            pes.append(pe)
        if mc:
            mcs.append(mc)
        rows.append({"ticker": p, "pe": pe, "marketCap": mc, "name": inf.get("shortName")})
    pe_avg = float(np.mean(pes)) if pes else None
    mc_avg = float(np.mean(mcs)) if mcs else None
    return {"pe_avg": pe_avg, "mc_avg": mc_avg, "count": len(rows), "rows": rows}

# -----------------------------
# Recommendation engine
# -----------------------------
def generate_recommendation(info, df, peers_metrics=None):
    reasons = []
    tech_score = 0.0
    fund_score = 0.0

    # Guard
    if df is None or df.empty or "Close" not in df.columns:
        return "No Data", "Insufficient price history."

    close = float(df["Close"].iloc[-1])
    prev_close = float(df["Close"].iloc[-2]) if len(df) > 1 else close
    # Technical signals
    sma20 = df["SMA20"].iloc[-1] if "SMA20" in df.columns else np.nan
    sma50 = df["SMA50"].iloc[-1] if "SMA50" in df.columns else np.nan
    sma200 = df["SMA200"].iloc[-1] if "SMA200" in df.columns else np.nan
    rsi = df["RSI"].iloc[-1] if "RSI" in df.columns else np.nan
    macd = df["MACD"].iloc[-1] if "MACD" in df.columns else np.nan
    macd_sig = df["MACD_SIGNAL"].iloc[-1] if "MACD_SIGNAL" in df.columns else np.nan

    # Price vs SMA
    if not np.isnan(sma50):
        if close > sma50:
            tech_score += 1.0
            reasons.append(f"Price {close:.2f} is above 50-SMA ({sma50:.2f}) — bullish.")
        else:
            tech_score -= 1.0
            reasons.append(f"Price {close:.2f} is below 50-SMA ({sma50:.2f}) — bearish.")

    if not np.isnan(sma20) and not np.isnan(sma50):
        if sma20 > sma50:
            tech_score += 0.7
            reasons.append("20-SMA above 50-SMA — momentum positive.")
        else:
            tech_score -= 0.4
            reasons.append("20-SMA below 50-SMA — weakening momentum.")

    # SMA200 as long-term filter
    if not np.isnan(sma200):
        if close > sma200:
            tech_score += 0.6
            reasons.append("Price above 200-SMA — long-term trend positive.")
        else:
            tech_score -= 0.6
            reasons.append("Price below 200-SMA — long-term trend negative.")

    # RSI
    if not np.isnan(rsi):
        if rsi < 30:
            tech_score += 1.2
            reasons.append(f"RSI {rsi:.1f} — oversold (buy signal).")
        elif rsi > 70:
            tech_score -= 1.2
            reasons.append(f"RSI {rsi:.1f} — overbought (caution).")
        else:
            reasons.append(f"RSI {rsi:.1f} — neutral.")

    # MACD
    if not np.isnan(macd) and not np.isnan(macd_sig):
        if macd > macd_sig:
            tech_score += 0.6
            reasons.append("MACD above signal — bullish momentum.")
        else:
            tech_score -= 0.6
            reasons.append("MACD below signal — bearish momentum.")

    # Short-term price action
    daily_pct = (close - prev_close) / prev_close * 100 if prev_close != 0 else 0
    reasons.append(f"Daily change: {daily_pct:.2f}%.")

    # Fundamental signals
    pe = info.get("trailingPE")
    forward_pe = info.get("forwardPE")
    roe = info.get("returnOnEquity")
    profit_margin = info.get("profitMargins")
    market_cap = info.get("marketCap")
    debt_to_equity = info.get("debtToEquity")
    eps = info.get("trailingEps")
    revenue = info.get("totalRevenue") or info.get("revenue") or info.get("regularMarketPreviousClose")

    # Compare P/E with peers average
    peer_note = ""
    if peers_metrics and peers_metrics.get("pe_avg") and pe:
        peer_pe = peers_metrics.get("pe_avg")
        if pe < peer_pe * 0.9:
            fund_score += 0.9
            reasons.append(f"Trailing P/E {pe:.1f} < peers avg {peer_pe:.1f} → relatively cheaper.")
        elif pe > peer_pe * 1.2:
            fund_score -= 0.9
            reasons.append(f"Trailing P/E {pe:.1f} > peers avg {peer_pe:.1f} → relatively expensive.")

    # P/E heuristics
    if pe:
        if pe < 12:
            fund_score += 0.7
            reasons.append(f"Low trailing P/E ({pe:.1f}) → value characteristic.")
        elif pe > 40:
            fund_score -= 0.7
            reasons.append(f"High trailing P/E ({pe:.1f}) → high expectations/valuation.")

    # ROE and margins
    if roe is not None:
        if roe > 0.15:
            fund_score += 0.8
            reasons.append(f"ROE {roe:.2f} — strong profitability.")
        elif roe < 0:
            fund_score -= 0.8
            reasons.append(f"ROE {roe:.2f} — unprofitable / poor returns.")

    if profit_margin is not None:
        if profit_margin > 0.15:
            fund_score += 0.6
            reasons.append(f"Profit margin {profit_margin:.2f} — profitable business.")
        elif profit_margin < 0:
            fund_score -= 0.6
            reasons.append(f"Profit margin {profit_margin:.2f} — negative margins.")

    # Debt
    if debt_to_equity is not None:
        if debt_to_equity < 1:
            fund_score += 0.3
            reasons.append(f"Debt-to-equity {debt_to_equity:.2f} — manageable leverage.")
        else:
            fund_score -= 0.3
            reasons.append(f"Debt-to-equity {debt_to_equity:.2f} — higher leverage risk.")

    # Market Cap weight for stability
    if market_cap:
        if market_cap > 1e11:
            fund_score += 0.4
            reasons.append("Large market cap — stable / blue-chip.")
        elif market_cap < 5e9:
            fund_score -= 0.4
            reasons.append("Small market cap — higher volatility/risk.")

    # Combine technical and fundamental
    final_score = tech_score * 0.6 + fund_score * 0.4

    # Map final_score to recommendations
    if final_score >= 1.8:
        rec = "Strong Buy"
    elif final_score >= 0.8:
        rec = "Buy"
    elif final_score >= -0.8:
        rec = "Hold"
    elif final_score >= -1.8:
        rec = "Sell"
    else:
        rec = "Strong Sell"

    reasoning = "\n".join(reasons)
    return rec, reasoning, round(final_score, 2)

# -----------------------------
# Clear caches helper
# -----------------------------
def clear_all_caches():
    try:
        fetch_history.clear()
        fetch_info.clear()
        fetch_today_minute.clear()
    except Exception:
        # older streamlit versions may not have .clear()
        st.experimental_memo.clear()
        st.experimental_singleton.clear()

# -----------------------------
# UI: Top selector & controls
# -----------------------------
st.markdown('<div class="main-header">📈 Stock Analyzer — Complete</div>', unsafe_allow_html=True)

# Display market header
display_market_header()

# Top selector area
top_col1, top_col2, top_col3 = st.columns([4, 1, 1])
with top_col1:
    st.markdown("#### Choose a stock / index / ETF")
    search_text = st.text_input("Search (type part of the name):", value="")
    # Build options list: show friendly name
    all_options = []
    for name, sym in POPULAR_INDIAN_STOCKS.items():
        all_options.append((f"{name} — {sym}", sym))
    for name, sym in INDIAN_ETFS.items():
        all_options.append((f"{name} — {sym}", sym))
    for name, sym in INDIAN_INDICES.items():
        all_options.append((f"{name} — {sym}", sym))
    # Filter by search_text
    if search_text:
        filtered = [opt for opt in all_options if search_text.lower() in opt[0].lower() or search_text.lower() in opt[1].lower()]
        if not filtered:
            st.info("No matches — showing full list.")
            filtered = all_options
    else:
        filtered = all_options
    option_labels = [opt[0] for opt in filtered]
    option_syms = [opt[1] for opt in filtered]
    # default selection index 0
    selected_index = st.selectbox("Select (top):", option_labels, index=0)
    selected_ticker = option_syms[option_labels.index(selected_index)]
with top_col2:
    analyze_clicked = st.button("Analyze")
with top_col3:
    refresh_clicked = st.button("Refresh / Clear Cache")

# Sidebar controls
with st.sidebar:
    st.header("Analysis Settings")
    period = st.selectbox("History period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
    interval = st.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)
    st.markdown("---")
    st.checkbox("Show technical indicators (SMA/RSI/MACD)", value=True, key="show_tech")
    st.checkbox("Show fundamentals", value=True, key="show_fund")
    st.checkbox("Compare to peers (built-in list)", value=True, key="show_peers")
    st.markdown("Auto-refresh (optional)")
    live_refresh = st.checkbox("Enable auto-refresh", value=False)
    refresh_interval = st.slider("Refresh interval (sec)", min_value=15, max_value=600, value=60, step=5)

# Optional auto-refresh hook
if live_refresh:
    try:
        from st_autorefresh import st_autorefresh
        st_autorefresh(interval=refresh_interval * 1000, key="autorefresh")
    except Exception:
        st.warning("Install `streamlit-autorefresh` to enable auto-refresh: pip install streamlit-autorefresh")

# Handle Refresh
if refresh_clicked:
    clear_all_caches()
    st.experimental_rerun()

# If Analyze clicked or auto-refresh triggered, run the analysis
if analyze_clicked or (live_refresh and st.session_state.get("autorefresh", None) is not None):
    ticker = selected_ticker  # e.g., "INFY.NS"
    st.markdown(f'<div class="section-header">Analysis — {ticker}</div>', unsafe_allow_html=True)
    # Fetch data
    with st.spinner("Fetching data..."):
        minute_df = fetch_today_minute(ticker)
        hist_df = fetch_history(ticker, period=period, interval=interval)
        info = fetch_info(ticker)

    # If historical empty, try a fallback shorter range
    if hist_df is None or hist_df.empty:
        st.error("No historical data found for the chosen ticker.")
    else:
        # Compute indicators
        df = compute_indicators(hist_df)

        # Live-like last price
        if minute_df is not None and not minute_df.empty:
            last_price = float(minute_df["Close"].iloc[-1])
            last_time = minute_df.index[-1]
        else:
            last_price = float(df["Close"].iloc[-1])
            last_time = df.index[-1]

        # Prev price for delta
        prev_price = float(df["Close"].iloc[-2]) if len(df) > 1 else last_price
        change = last_price - prev_price
        pct_change = (change / prev_price * 100) if prev_price != 0 else 0.0

        col_a, col_b, col_c = st.columns([1.2, 1, 2])
        col_a.metric("Last price", f"₹{last_price:.2f}", delta=f"{change:.2f} ({pct_change:.2f}%)")
        # timestamp formatting
        try:
            ts_text = last_time.strftime("%Y-%m-%d %H:%M:%S %Z") if hasattr(last_time, "tz") else last_time.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            ts_text = str(last_time)
        col_b.write(f"**Last update:**\n{ts_text}")
        col_c.write(f"**Company:** {info.get('shortName','-')}  \n**Sector:** {info.get('sector','-')}  \n**Industry:** {info.get('industry','-')}")

        st.markdown("---")

        # Chart: candlestick with overlays (uses plotly)
        st.subheader("Price chart (candlestick) with Moving Averages")
        fig = go.Figure()
        # Candlestick
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Price",
            increasing_line_color="green",
            decreasing_line_color="red",
            opacity=0.8
        ))
        # MAs
        if "SMA20" in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df["SMA20"], name="SMA20", line=dict(width=1.5)))
        if "SMA50" in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df["SMA50"], name="SMA50", line=dict(width=1.5)))
        if "SMA200" in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df["SMA200"], name="SMA200", line=dict(width=1.5)))
        fig.update_layout(height=480, margin=dict(l=10, r=10, t=30, b=10), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)

        # Technical summary panel
        if st.session_state.get("show_tech", True):
            st.subheader("Technical Indicators")
            tcol1, tcol2, tcol3, tcol4 = st.columns(4)
            last_rsi = df["RSI"].iloc[-1] if "RSI" in df.columns else None
            last_macd = df["MACD"].iloc[-1] if "MACD" in df.columns else None
            last_macd_sig = df["MACD_SIGNAL"].iloc[-1] if "MACD_SIGNAL" in df.columns else None
            last_sma20 = df["SMA20"].iloc[-1] if "SMA20" in df.columns else None
            tcol1.metric("RSI (14)", f"{last_rsi:.1f}" if last_rsi is not None and not np.isnan(last_rsi) else "N/A")
            tcol2.metric("MACD", f"{last_macd:.4f}" if last_macd is not None and not np.isnan(last_macd) else "N/A")
            tcol3.metric("MACD Signal", f"{last_macd_sig:.4f}" if last_macd_sig is not None and not np.isnan(last_macd_sig) else "N/A")
            tcol4.metric("SMA20", f"{last_sma20:.2f}" if last_sma20 is not None and not np.isnan(last_sma20) else "N/A")

            # RSI & MACD plots
            st.markdown("**RSI (14)**")
            rfig = go.Figure()
            rfig.add_trace(go.Scatter(x=df.index, y=df["RSI"], name="RSI"))
            rfig.add_hline(y=70, line=dict(color="red", dash="dash"))
            rfig.add_hline(y=30, line=dict(color="green", dash="dash"))
            rfig.update_layout(height=240, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(rfig, use_container_width=True)

            st.markdown("**MACD**")
            mfig = go.Figure()
            mfig.add_trace(go.Scatter(x=df.index, y=df["MACD"], name="MACD"))
            mfig.add_trace(go.Scatter(x=df.index, y=df["MACD_SIGNAL"], name="Signal"))
            mfig.update_layout(height=240, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(mfig, use_container_width=True)

        # Fundamentals
        if st.session_state.get("show_fund", True):
            st.subheader("Fundamental Summary (detailed)")
            fund_items = {
                "Short name": info.get("shortName"),
                "Sector": info.get("sector"),
                "Industry": info.get("industry"),
                "Market Cap": format_large_number(info.get("marketCap")),
                "Trailing P/E": info.get("trailingPE"),
                "Forward P/E": info.get("forwardPE"),
                "PEG Ratio": info.get("pegRatio"),
                "EPS (TTM)": info.get("trailingEps"),
                "Revenue (TTM)": format_large_number(info.get("totalRevenue") or info.get("revenue")),
                "Net Income (TTM)": format_large_number(info.get("netIncomeToCommon")),
                "Profit Margins": format_pct(info.get("profitMargins")),
                "Return on Equity (ROE)": format_pct(info.get("returnOnEquity")),
                "Debt to Equity": info.get("debtToEquity"),
                "Dividend Yield": format_pct(info.get("dividendYield")),
                "52-Week High": info.get("fiftyTwoWeekHigh"),
                "52-Week Low": info.get("fiftyTwoWeekLow"),
                "Beta": info.get("beta"),
            }
            fund_df = pd.DataFrame(list(fund_items.items()), columns=["Metric", "Value"])
            st.table(fund_df)

        # Peers & comparison
        peers_metrics = {}
        peers_list = []
        if st.session_state.get("show_peers", True):
            st.subheader("Peers / Industry Comparison (from built-in list)")
            peers_list = find_peers(ticker, {**POPULAR_INDIAN_STOCKS, **INDIAN_ETFS, **INDIAN_INDICES})
            peers_metrics = compute_peers_metrics(peers_list)
            if peers_list:
                rows = []
                for p in peers_list:
                    inf = fetch_info(p)
                    rows.append({
                        "Ticker": p,
                        "Name": inf.get("shortName"),
                        "PE (trailing)": inf.get("trailingPE"),
                        "Profit Margins": inf.get("profitMargins"),
                        "MarketCap": format_large_number(inf.get("marketCap"))
                    })
                peers_df = pd.DataFrame(rows).set_index("Ticker")
                st.dataframe(peers_df)
            else:
                st.write("No peers found among the built-in list (or industry data missing).")

        # Recommendation
        rec, reasoning, score = generate_recommendation(info, df, peers_metrics if peers_metrics else None)
        st.subheader("Recommendation")
        emoji = {"Strong Buy":"✅","Buy":"🟢","Hold":"🟡","Sell":"🔴","Strong Sell":"⛔"}.get(rec, "")
        st.markdown(f"### {emoji} **{rec}**  — score: {score}")
        st.markdown("**Reasoning (signals used):**")
        # Make the reasoning human-friendly (split lines)
        for line in reasoning.split("\n"):
            st.write(f"- {line}")

        st.caption("Data fetched from Yahoo Finance via yfinance (may be delayed). Use Refresh to clear caches.")

# If user didn't click analyze, show a helpful message
else:
    st.info("Select a ticker above and click **Analyze** to fetch data and run the full analysis.")
    st.write("Tip: Use search box to quickly find a stock (type part of the name).")

# Footer / help
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit + yfinance.  \nNote: yfinance data may be subject to delays and rate-limits.")