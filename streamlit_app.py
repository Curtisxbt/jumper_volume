# =========================
#  Jumper – Volume Tracker
#  by CURTIS_XBT
# =========================
import datetime as dt
import pandas as pd
import plotly.express as px
import streamlit as st

import jumper_volume as jv

PRIMARY = "#C1A5EC"
SECONDARY = "#8B7AB8"
ACCENT = "#E8DEFF"
DARK = "#0A0A0F"
DARKER = "#050508"

st.set_page_config(
    page_title="Jumper Analytics",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------- PREMIUM CSS ---------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* {{
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}

:root {{
  --primary: {PRIMARY};
  --secondary: {SECONDARY};
  --accent: {ACCENT};
  --dark: {DARK};
  --darker: {DARKER};
}}

html[data-theme="light"] {{
  --text-primary: #0A0A0F;
  --text-muted: #444444;
  --text-button: #0A0A0F;
  --bg-card: rgba(0,0,0,0.04);
  --border-card: rgba(0,0,0,0.12);
  --input-bg: rgba(0,0,0,0.05);
  --input-border: rgba(0,0,0,0.2);
}}

html[data-theme="dark"] {{
  --text-primary: #FFFFFF;
  --text-muted: rgba(255,255,255,0.65);
  --text-button: #FFFFFF;
  --bg-card: rgba(255,255,255,0.08);
  --border-card: rgba(255,255,255,0.12);
  --input-bg: rgba(255,255,255,0.08);
  --input-border: rgba(193,165,236,0.25);
}}

[data-testid="stAppViewContainer"] {{
  background: 
    radial-gradient(ellipse 1400px 900px at 20% 0%, rgba(193,165,236,0.15), transparent),
    radial-gradient(ellipse 1200px 700px at 80% 100%, rgba(139,122,184,0.12), transparent),
    radial-gradient(circle 800px at 50% 50%, rgba(193,165,236,0.05), transparent),
    linear-gradient(180deg, {DARKER} 0%, {DARK} 100%);
  color: var(--text-primary);
  min-height: 100vh;
}}

html[data-theme="light"] [data-testid="stAppViewContainer"] {{
  background: 
    radial-gradient(ellipse 1400px 900px at 20% 0%, rgba(193,165,236,0.08), transparent),
    radial-gradient(ellipse 1200px 700px at 80% 100%, rgba(139,122,184,0.06), transparent),
    linear-gradient(180deg, #FAFAFA 0%, #F5F5F5 100%);
}}

.block-container {{
  padding: 2rem 3rem 3rem;
  max-width: 1400px;
}}

.hero-container {{
  margin-bottom: 3rem;
  position: relative;
}}

.badge {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 18px;
  background: linear-gradient(135deg, rgba(255,255,255,0.12), rgba(193,165,236,0.15));
  border: 1px solid rgba(193,165,236,0.3);
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  backdrop-filter: blur(20px);
  box-shadow: 0 4px 20px rgba(193,165,236,0.15);
  margin-bottom: 1.5rem;
}}

html[data-theme="light"] .badge {{
  background: linear-gradient(135deg, rgba(193,165,236,0.15), rgba(193,165,236,0.25));
  border: 1px solid rgba(193,165,236,0.4);
}}

.badge::before {{
  content: '';
  width: 8px;
  height: 8px;
  background: linear-gradient(135deg, {PRIMARY}, {ACCENT});
  border-radius: 50%;
  box-shadow: 0 0 12px {PRIMARY};
  animation: pulse 2s infinite;
}}

@keyframes pulse {{
  0%, 100% {{ opacity: 1; transform: scale(1); }}
  50% {{ opacity: 0.6; transform: scale(0.85); }}
}}

h1.hero-title {{
  font-size: clamp(3rem, 8vw, 5.5rem);
  font-weight: 900;
  line-height: 1;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #FFFFFF 0%, {PRIMARY} 50%, {ACCENT} 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  letter-spacing: -0.03em;
  text-shadow: 0 0 80px rgba(193,165,236,0.3);
}}

html[data-theme="light"] h1.hero-title {{
  background: linear-gradient(135deg, #0A0A0F 0%, {SECONDARY} 50%, {PRIMARY} 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}}

.hero-subtitle {{
  font-size: 1.25rem;
  color: var(--text-muted);
  font-weight: 500;
  line-height: 1.6;
  max-width: 600px;
}}

.glass-card {{
  background: linear-gradient(135deg, 
    var(--bg-card) 0%, 
    rgba(193,165,236,0.05) 100%);
  border: 1px solid var(--border-card);
  border-radius: 24px;
  padding: 2rem;
  backdrop-filter: blur(20px);
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.3),
    inset 0 1px 0 rgba(255,255,255,0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}}

html[data-theme="light"] .glass-card {{
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.08),
    inset 0 1px 0 rgba(255,255,255,0.5);
}}

.glass-card::before {{
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(193,165,236,0.5), 
    transparent);
}}

.glass-card:hover {{
  transform: translateY(-4px);
  border-color: rgba(193,165,236,0.4);
  box-shadow: 
    0 16px 48px rgba(193,165,236,0.2),
    inset 0 1px 0 rgba(255,255,255,0.15);
}}

html[data-theme="light"] .glass-card:hover {{
  box-shadow: 
    0 16px 48px rgba(193,165,236,0.15),
    inset 0 1px 0 rgba(255,255,255,0.8);
}}

.kpi-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin: 2.5rem 0;
}}

@media (max-width: 968px) {{
  .kpi-grid {{
    grid-template-columns: 1fr;
  }}
}}

.kpi-card {{
  background: linear-gradient(135deg, 
    rgba(193,165,236,0.12) 0%, 
    rgba(139,122,184,0.08) 100%);
  border: 1.5px solid rgba(193,165,236,0.25);
  border-radius: 28px;
  padding: 2rem 1.75rem;
  backdrop-filter: blur(20px);
  box-shadow: 
    0 12px 40px rgba(193,165,236,0.15),
    inset 0 1px 0 rgba(255,255,255,0.1);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}}

html[data-theme="light"] .kpi-card {{
  background: linear-gradient(135deg, 
    rgba(193,165,236,0.12) 0%, 
    rgba(139,122,184,0.10) 100%);
  border: 1.5px solid rgba(193,165,236,0.3);
  box-shadow: 
    0 12px 40px rgba(193,165,236,0.1),
    inset 0 1px 0 rgba(255,255,255,0.5);
}}

.kpi-card::after {{
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(193,165,236,0.15) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.4s;
}}

.kpi-card:hover {{
  transform: translateY(-6px) scale(1.02);
  border-color: rgba(193,165,236,0.5);
  box-shadow: 
    0 20px 60px rgba(193,165,236,0.3),
    inset 0 1px 0 rgba(255,255,255,0.2);
}}

html[data-theme="light"] .kpi-card:hover {{
  box-shadow: 
    0 20px 60px rgba(193,165,236,0.2),
    inset 0 1px 0 rgba(255,255,255,0.8);
}}

.kpi-card:hover::after {{
  opacity: 1;
}}

.kpi-label {{
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 0.75rem;
}}

.kpi-value {{
  font-size: clamp(2rem, 4vw, 3.5rem);
  font-weight: 900;
  background: linear-gradient(135deg, #FFFFFF 0%, {PRIMARY} 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  line-height: 1.1;
  letter-spacing: -0.02em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: clip;
}}

html[data-theme="light"] .kpi-value {{
  background: linear-gradient(135deg, #0A0A0F 0%, {SECONDARY} 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}}

.kpi-icon {{
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  font-size: 2.5rem;
  opacity: 0.35;
  filter: drop-shadow(0 0 8px rgba(193,165,236,0.4));
}}

.blockchain-counter {{
  text-align: center;
  margin: 2.5rem 0;
  padding: 2rem;
  background: linear-gradient(135deg, 
    rgba(193,165,236,0.08) 0%, 
    rgba(139,122,184,0.05) 100%);
  border: 1px solid rgba(193,165,236,0.2);
  border-radius: 24px;
  backdrop-filter: blur(20px);
}}

html[data-theme="light"] .blockchain-counter {{
  background: linear-gradient(135deg, 
    rgba(193,165,236,0.10) 0%, 
    rgba(139,122,184,0.08) 100%);
  border: 1px solid rgba(193,165,236,0.3);
}}

.blockchain-counter-label {{
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 0.5rem;
}}

.blockchain-counter-value {{
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 900;
  background: linear-gradient(135deg, #FFFFFF 0%, {PRIMARY} 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  letter-spacing: -0.02em;
}}

html[data-theme="light"] .blockchain-counter-value {{
  background: linear-gradient(135deg, #0A0A0F 0%, {SECONDARY} 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}}

.chain-badges {{
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin: 1.5rem 0;
}}

.chain-badge {{
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, rgba(193,165,236,0.15), rgba(139,122,184,0.1));
  border: 1.5px solid rgba(193,165,236,0.3);
  border-radius: 16px;
  backdrop-filter: blur(20px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 16px rgba(193,165,236,0.1);
}}

html[data-theme="light"] .chain-badge {{
  background: linear-gradient(135deg, rgba(193,165,236,0.15), rgba(139,122,184,0.12));
  border: 1.5px solid rgba(193,165,236,0.35);
}}

.chain-badge:hover {{
  transform: translateY(-3px);
  border-color: rgba(193,165,236,0.6);
  box-shadow: 0 8px 24px rgba(193,165,236,0.25);
  background: linear-gradient(135deg, rgba(193,165,236,0.22), rgba(139,122,184,0.15));
}}

.chain-badge-icon {{
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, {PRIMARY}, {SECONDARY});
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
  color: #FFF;
  box-shadow: 0 4px 12px rgba(193,165,236,0.3);
}}

.chain-badge-name {{
  font-weight: 600;
  font-size: 1rem;
  color: var(--text-primary);
  letter-spacing: 0.3px;
}}

.chain-badge-count {{
  font-size: 0.85rem;
  color: var(--text-muted);
  font-weight: 500;
}}

html[data-theme="light"] .stTextInput > div > div > input,
html[data-theme="light"] .stDateInput > div > div > input {{
  background: rgba(0,0,0,0.05) !important;
  border: 1.5px solid rgba(0,0,0,0.2) !important;
  border-radius: 16px !important;
  color: #0A0A0F !important;
  padding: 0.9rem 1.2rem !important;
  font-size: 1rem !important;
  font-weight: 500 !important;
  transition: all 0.3s !important;
  backdrop-filter: blur(10px) !important;
}}

html[data-theme="dark"] .stTextInput > div > div > input,
html[data-theme="dark"] .stDateInput > div > div > input {{
  background: rgba(255,255,255,0.08) !important;
  border: 1.5px solid rgba(193,165,236,0.25) !important;
  border-radius: 16px !important;
  color: #FFFFFF !important;
  padding: 0.9rem 1.2rem !important;
  font-size: 1rem !important;
  font-weight: 500 !important;
  transition: all 0.3s !important;
  backdrop-filter: blur(10px) !important;
}}

.stTextInput > div > div > input:focus,
.stDateInput > div > div > input:focus {{
  border-color: {PRIMARY} !important;
  box-shadow: 0 0 0 3px rgba(193,165,236,0.15) !important;
  background: rgba(255,255,255,0.12) !important;
}}

html[data-theme="light"] .stTextInput > div > div > input:focus,
html[data-theme="light"] .stDateInput > div > div > input:focus {{
  background: rgba(0,0,0,0.08) !important;
}}

.stTextInput label, .stDateInput label {{
  font-weight: 600 !important;
  color: var(--text-primary) !important;
  font-size: 0.9rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.5px !important;
}}

html[data-theme="light"] .stButton > button,
html[data-theme="light"] .stDownloadButton > button {{
  background: linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 100%) !important;
  border: none !important;
  border-radius: 16px !important;
  padding: 1rem 2.5rem !important;
  font-size: 1rem !important;
  font-weight: 700 !important;
  color: #0A0A0F !important;
  letter-spacing: 0.5px !important;
  text-transform: uppercase !important;
  box-shadow: 0 8px 32px rgba(193,165,236,0.4) !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  position: relative !important;
  overflow: hidden !important;
}}

html[data-theme="dark"] .stButton > button,
html[data-theme="dark"] .stDownloadButton > button {{
  background: linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 100%) !important;
  border: none !important;
  border-radius: 16px !important;
  padding: 1rem 2.5rem !important;
  font-size: 1rem !important;
  font-weight: 700 !important;
  color: #FFFFFF !important;
  letter-spacing: 0.5px !important;
  text-transform: uppercase !important;
  box-shadow: 0 8px 32px rgba(193,165,236,0.4) !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  position: relative !important;
  overflow: hidden !important;
}}

.stButton > button::before,
.stDownloadButton > button::before {{
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}}

html[data-theme="light"] .stButton > button:hover,
html[data-theme="light"] .stDownloadButton > button:hover {{
  transform: translateY(-2px) !important;
  box-shadow: 0 12px 48px rgba(193,165,236,0.5) !important;
  color: #0A0A0F !important;
}}

html[data-theme="dark"] .stButton > button:hover,
html[data-theme="dark"] .stDownloadButton > button:hover {{
  transform: translateY(-2px) !important;
  box-shadow: 0 12px 48px rgba(193,165,236,0.6) !important;
  color: #FFFFFF !important;
}}

.stButton > button:hover::before,
.stDownloadButton > button:hover::before {{
  left: 100%;
}}

html[data-theme="light"] .stButton > button:active,
html[data-theme="light"] .stDownloadButton > button:active,
html[data-theme="light"] .stButton > button:focus,
html[data-theme="light"] .stDownloadButton > button:focus {{
  color: #0A0A0F !important;
}}

html[data-theme="dark"] .stButton > button:active,
html[data-theme="dark"] .stDownloadButton > button:active,
html[data-theme="dark"] .stButton > button:focus,
html[data-theme="dark"] .stDownloadButton > button:focus {{
  color: #FFFFFF !important;
}}

.stTabs [data-baseweb="tab-list"] {{
  gap: 1rem;
  background: rgba(255,255,255,0.03);
  padding: 0.5rem;
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.08);
}}

html[data-theme="light"] .stTabs [data-baseweb="tab-list"] {{
  background: rgba(0,0,0,0.03);
  border: 1px solid rgba(0,0,0,0.1);
}}

.stTabs [data-baseweb="tab"] {{
  background: transparent;
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  color: var(--text-muted);
  transition: all 0.3s;
}}

.stTabs [aria-selected="true"] {{
  background: linear-gradient(135deg, {PRIMARY}, {SECONDARY});
  color: #FFFFFF !important;
  box-shadow: 0 4px 16px rgba(193,165,236,0.3);
}}

.chart-container {{
  background: linear-gradient(135deg, 
    rgba(255,255,255,0.04) 0%, 
    rgba(193,165,236,0.03) 100%);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px;
  padding: 1.5rem;
  margin: 1rem 0;
  backdrop-filter: blur(10px);
}}

html[data-theme="light"] .chart-container {{
  background: linear-gradient(135deg, 
    rgba(0,0,0,0.02) 0%, 
    rgba(193,165,236,0.05) 100%);
  border: 1px solid rgba(0,0,0,0.08);
}}

::-webkit-scrollbar {{
  width: 10px;
  height: 10px;
}}

::-webkit-scrollbar-track {{
  background: rgba(255,255,255,0.03);
}}

html[data-theme="light"] ::-webkit-scrollbar-track {{
  background: rgba(0,0,0,0.03);
}}

::-webkit-scrollbar-thumb {{
  background: linear-gradient(180deg, {PRIMARY}, {SECONDARY});
  border-radius: 10px;
}}

::-webkit-scrollbar-thumb:hover {{
  background: linear-gradient(180deg, {ACCENT}, {PRIMARY});
}}

.stSpinner > div {{
  border-top-color: {PRIMARY} !important;
}}

.info-card {{
  background: linear-gradient(135deg, 
    rgba(193,165,236,0.08) 0%, 
    rgba(139,122,184,0.05) 100%);
  border: 1px solid rgba(193,165,236,0.2);
  border-left: 4px solid {PRIMARY};
  border-radius: 16px;
  padding: 1.5rem;
  margin: 1.5rem 0;
  backdrop-filter: blur(10px);
}}

html[data-theme="light"] .info-card {{
  background: linear-gradient(135deg, 
    rgba(193,165,236,0.10) 0%, 
    rgba(139,122,184,0.08) 100%);
  border: 1px solid rgba(193,165,236,0.3);
  border-left: 4px solid {PRIMARY};
}}

header[data-testid="stHeader"] {{
  background: transparent;
}}

footer {{
  visibility: hidden;
}}

#MainMenu {{
  visibility: hidden;
}}
</style>
""", unsafe_allow_html=True)

# --------- HERO ---------
st.markdown("""
<div class="hero-container">
  <div class="badge">
    <span>BUILT BY CURTIS_XBT</span>
  </div>
  <h1 class="hero-title">Jumper Analytics</h1>
  <div class="hero-subtitle">
    Enterprise-grade cross-chain analytics. Track bridges, swaps, and multi-chain activity 
    across any EVM wallet with real-time insights.
  </div>
</div>
""", unsafe_allow_html=True)

# --------- FORM ---------
with st.container():
    with st.form("params"):
        col1, col2, col3 = st.columns([3, 1.5, 1])
        
        with col1:
            wallet = st.text_input(
                "Wallet Address (EVM)", 
                value="",
                placeholder="0x...",
                help="Enter any EVM-compatible wallet address"
            )
        
        with col2:
            today = dt.date.today()
            first_of_month = today.replace(day=1)
            since = st.date_input(
                "Analysis Period", 
                value=first_of_month,
                help="Start date for transaction analysis"
            )
        
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🚀 Analyze", use_container_width=True)

if submitted:
    if not wallet or not wallet.startswith("0x") or len(wallet) < 10:
        st.error("⚠️ Please enter a valid EVM address (starts with 0x)")
        st.stop()

    jv.WALLET = wallet.strip()

    with st.spinner("🔄 Loading blockchain data..."):
        chain_map = jv.fetch_chains()
    
    if not chain_map:
        st.error("❌ Could not load chains metadata")
        st.stop()

    from_date_str = since.strftime("%Y-%m-%d")
    with st.spinner("⚡ Processing transactions..."):
        txs = jv.fetch_and_process_data(from_date_str, chain_map)

    if not txs:
        st.markdown("""
        <div class="info-card">
            <h3 style="margin:0 0 0.5rem 0;">🔭 No Transfers Found</h3>
            <p style="margin:0; color: rgba(255,255,255,0.7);">
                No transactions detected for this wallet in the selected period. 
                Try adjusting the date range or verify the wallet address.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    analyzer = jv.TransactionAnalyzer()
    ok = analyzer.analyze_transactions(txs)
    
    if not ok:
        st.warning("⚠️ No analyzable data returned")
        st.stop()

    # --------- BUILD DATAFRAME ---------
    df = pd.DataFrame(txs)
    
    # --------- FIXED BLOCKCHAIN EXTRACTION ---------
    # Use the correct keys from build_transaction_dict: 'from_blockchain' and 'to_blockchain'
    unique_chains = set()
    for tx in txs:
        from_chain = tx.get("from_blockchain")
        to_chain = tx.get("to_blockchain")
        
        if from_chain and str(from_chain).strip():
            unique_chains.add(str(from_chain).strip())
        if to_chain and str(to_chain).strip():
            unique_chains.add(str(to_chain).strip())
    
    num_blockchains = len(unique_chains)

    # --------- MEGA KPIs (3 CARDS) ---------
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-icon">📊</div>
            <div class="kpi-label">Total Transfers</div>
            <div class="kpi-value">{len(analyzer.transactions):,}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">🌉</div>
            <div class="kpi-label">Bridge Volume</div>
            <div class="kpi-value">${analyzer.bridge_value:,.0f}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">🔄</div>
            <div class="kpi-label">Swap Volume</div>
            <div class="kpi-value">${analyzer.swap_value:,.0f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --------- BLOCKCHAIN COUNTER ---------
    st.markdown(f"""
    <div class="blockchain-counter">
        <div class="blockchain-counter-label">⛓️ Chains Used</div>
        <div class="blockchain-counter-value">{num_blockchains} blockchain{"s" if num_blockchains != 1 else ""}</div>
    </div>
    """, unsafe_allow_html=True)

    # --------- DATA PROCESSING FOR CHARTS ---------
    if "timestamp" in df.columns:
        df["date"] = pd.to_datetime(df["timestamp"], unit="s", utc=True).dt.tz_convert("UTC").dt.date

    # --------- INSIGHTS SECTION ---------

    st.markdown("### 📈 Detailed Insights")
    
    tab1, tab2 = st.tabs(["🏢 Platform Analytics", "⛓️ Chains Used"])

    with tab1:
        platforms = None
        if hasattr(analyzer, "platforms") and analyzer.platforms:
            platforms = analyzer.platforms
        elif "platform" in df.columns:
            platforms = df["platform"].value_counts().to_dict()
        
        if platforms:
            pf = pd.DataFrame([
                {"platform": k, "count": v} 
                for k, v in platforms.items()
            ]).sort_values("count", ascending=False)
            
            fig = px.bar(
                pf, 
                x="platform", 
                y="count",
                labels={"count": "Transactions", "platform": "Platform"}
            )
            
            fig.update_traces(
                marker_color=PRIMARY,
                hovertemplate="<b>%{x}</b><br>%{y} transactions<extra></extra>"
            )
            
            fig.update_layout(
                height=400,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#FFFFFF", family="Inter"),
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(
                    gridcolor="rgba(255,255,255,0.06)",
                    showgrid=False
                ),
                yaxis=dict(
                    gridcolor="rgba(255,255,255,0.06)",
                    showgrid=True
                ),
                showlegend=False
            )
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("📊 Platform data unavailable")

    with tab2:
        # Extract unique blockchains
        blockchains_list = sorted(list(unique_chains))
        
        if blockchains_list:
            st.markdown(f"""
            <div class="glass-card">
                <h4 style="margin: 0 0 1.5rem 0;">⛓️ Blockchains Used ({len(blockchains_list)})</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Display as simple list
            for i, chain in enumerate(blockchains_list, 1):
                st.markdown(f"**{i}.** {chain}")
        else:
            st.info("📊 No blockchain data available")

    # --------- EXPORT SECTION ---------
    st.markdown("### 📥 Data Export")
    
    st.markdown("""
    <div class="glass-card">
        <h4 style="margin: 0 0 1rem 0;">Download Complete Dataset</h4>
        <p style="margin: 0; color: rgba(255,255,255,0.7); line-height: 1.6;">
            Download the full CSV below – the detailed table is intentionally hidden on the page 
            to maintain a clean, focused interface. Export for further analysis or integration with your tools.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.download_button(
        "📄 Download CSV Report",
        df.to_csv(index=False).encode("utf-8"),
        "jumper_analytics_report.csv",
        "text/csv",
        use_container_width=True
    )

else:
    # --------- EMPTY STATE ---------
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 3rem 2rem;">
        <div style="font-size: 4rem; margin-bottom: 1.5rem; opacity: 0.3;">🔗</div>
        <h3 style="margin: 0 0 1rem 0; font-size: 1.5rem;">Ready to Analyze</h3>
        <p style="margin: 0; color: rgba(255,255,255,0.6); max-width: 500px; margin: 0 auto; line-height: 1.8;">
            Enter any EVM wallet address above to unlock comprehensive cross-chain analytics. 
            Track bridges, swaps, and multi-chain activity with institutional-grade precision.
        </p>
    </div>
    """, unsafe_allow_html=True)
