# =========================
#  Jumper – Premium Startup UI
#  Design System: Glassmorphism + Gradient Accents
#  Primary: #C1A5EC (Lavender)
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

[data-testid="stAppViewContainer"] {{
  background: 
    radial-gradient(ellipse 1400px 900px at 20% 0%, rgba(193,165,236,0.15), transparent),
    radial-gradient(ellipse 1200px 700px at 80% 100%, rgba(139,122,184,0.12), transparent),
    radial-gradient(circle 800px at 50% 50%, rgba(193,165,236,0.05), transparent),
    linear-gradient(180deg, {DARKER} 0%, {DARK} 100%);
  color: #FFFFFF;
  min-height: 100vh;
}}

.block-container {{
  padding: 2rem 3rem 3rem;
  max-width: 1400px;
}}

/* ===== HERO SECTION ===== */
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

.hero-subtitle {{
  font-size: 1.25rem;
  color: rgba(255,255,255,0.65);
  font-weight: 500;
  line-height: 1.6;
  max-width: 600px;
}}

/* ===== GLASS CARD SYSTEM ===== */
.glass-card {{
  background: linear-gradient(135deg, 
    rgba(255,255,255,0.08) 0%, 
    rgba(193,165,236,0.05) 100%);
  border: 1px solid rgba(255,255,255,0.12);
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

/* ===== MEGA KPI CARDS ===== */
.kpi-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin: 2.5rem 0;
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

.kpi-card:hover::after {{
  opacity: 1;
}}

.kpi-label {{
  font-size: 0.9rem;
  font-weight: 600;
  color: rgba(255,255,255,0.6);
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 0.75rem;
}}

.kpi-value {{
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 900;
  background: linear-gradient(135deg, #FFFFFF 0%, {PRIMARY} 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  line-height: 1;
  letter-spacing: -0.02em;
}}

.kpi-icon {{
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  font-size: 2rem;
  opacity: 0.15;
}}

/* ===== FORM STYLING ===== */
.stTextInput > div > div > input,
.stDateInput > div > div > input {{
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

.stTextInput label, .stDateInput label {{
  font-weight: 600 !important;
  color: rgba(255,255,255,0.85) !important;
  font-size: 0.9rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.5px !important;
}}

/* ===== BUTTON STYLING ===== */
.stButton > button,
.stDownloadButton > button {{
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

.stButton > button:hover,
.stDownloadButton > button:hover {{
  transform: translateY(-2px) !important;
  box-shadow: 0 12px 48px rgba(193,165,236,0.6) !important;
}}

.stButton > button:hover::before,
.stDownloadButton > button:hover::before {{
  left: 100%;
}}

/* ===== TABS STYLING ===== */
.stTabs [data-baseweb="tab-list"] {{
  gap: 1rem;
  background: rgba(255,255,255,0.03);
  padding: 0.5rem;
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.08);
}}

.stTabs [data-baseweb="tab"] {{
  background: transparent;
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  color: rgba(255,255,255,0.6);
  transition: all 0.3s;
}}

.stTabs [aria-selected="true"] {{
  background: linear-gradient(135deg, {PRIMARY}, {SECONDARY});
  color: #FFFFFF !important;
  box-shadow: 0 4px 16px rgba(193,165,236,0.3);
}}

/* ===== CHART CONTAINER ===== */
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

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {{
  width: 10px;
  height: 10px;
}}

::-webkit-scrollbar-track {{
  background: rgba(255,255,255,0.03);
}}

::-webkit-scrollbar-thumb {{
  background: linear-gradient(180deg, {PRIMARY}, {SECONDARY});
  border-radius: 10px;
}}

::-webkit-scrollbar-thumb:hover {{
  background: linear-gradient(180deg, {ACCENT}, {PRIMARY});
}}

/* ===== SPINNER ===== */
.stSpinner > div {{
  border-top-color: {PRIMARY} !important;
}}

/* ===== INFO CARDS ===== */
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

/* ===== HIDE DEFAULTS ===== */
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
    <span>POWERED BY LI.FI</span>
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
                "Wallet Address", 
                placeholder="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb...",
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
            <h3 style="margin:0 0 0.5rem 0;">📭 No Transfers Found</h3>
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

    # --------- MEGA KPIs ---------
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

    # --------- DATA PROCESSING ---------
    df = pd.DataFrame(txs)
    if "timestamp" in df.columns:
        df["date"] = pd.to_datetime(df["timestamp"], unit="s", utc=True).dt.tz_convert("UTC").dt.date

    # --------- INSIGHTS SECTION ---------
    st.markdown("### 📈 Detailed Insights")
    
    tab1, tab2, tab3 = st.tabs(["💰 Volume Trends", "🏢 Platform Analytics", "⛓️ Chain Distribution"])

    with tab1:
        if "date" in df.columns and "usd" in df.columns:
            daily = df.groupby("date")["usd"].sum().reset_index().sort_values("date")
            
            fig = px.area(
                daily, 
                x="date", 
                y="usd",
                labels={"usd": "Volume (USD)", "date": "Date"}
            )
            
            fig.update_traces(
                line_color=PRIMARY,
                fillcolor=f"rgba(193,165,236,0.2)",
                hovertemplate="<b>%{x}</b><br>$%{y:,.2f}<extra></extra>"
            )
            
            fig.update_layout(
                height=400,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#FFFFFF", family="Inter"),
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(
                    gridcolor="rgba(255,255,255,0.06)",
                    showgrid=True,
                    zeroline=False
                ),
                yaxis=dict(
                    gridcolor="rgba(255,255,255,0.06)",
                    showgrid=True,
                    zeroline=False
                ),
                hovermode="x unified"
            )
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("📊 Volume data unavailable")

    with tab2:
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

    with tab3:
        cols = [c for c in ["from_chain", "to_chain"] if c in df.columns]
        if cols:
            chain_counts = (
                pd.concat([df[c] for c in cols])
                .value_counts()
                .reset_index()
                .rename(columns={"index": "chain", 0: "count"})
            )
            
            fig = px.bar(
                chain_counts, 
                x="chain", 
                y="count",
                labels={"count": "Interactions", "chain": "Blockchain"}
            )
            
            fig.update_traces(
                marker_color=PRIMARY,
                hovertemplate="<b>%{x}</b><br>%{y} interactions<extra></extra>"
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
            st.info("📊 Chain data unavailable")

    # --------- EXPORT SECTION ---------
    st.markdown("### 📥 Data Export")
    
    st.markdown("""
    <div class="glass-card">
        <h4 style="margin: 0 0 1rem 0;">Download Complete Dataset</h4>
        <p style="margin: 0; color: rgba(255,255,255,0.7); line-height: 1.6;">
            Export all transaction data in CSV format for further analysis, 
            reporting, or integration with your existing tools.
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
