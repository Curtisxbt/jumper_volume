# =========================
#  Jumper – Modern UI (Streamlit)
#  Theme color: #C1A5EC
# =========================
import datetime as dt
import pandas as pd
import plotly.express as px
import streamlit as st

import jumper_volume as jv  # ton module

PRIMARY = "#C1A5EC"
DARK = "#0B0B11"            # fond sombre élégant
CARD_BG = "rgba(255,255,255,0.06)"

st.set_page_config(
    page_title="Jumper Analytics",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------- GLOBAL STYLE (CSS) ---------
st.markdown(f"""
<style>
:root {{
  --jumper: {PRIMARY};
  --bg: {DARK};
  --card: {CARD_BG};
  --text: #EDECF8;
  --muted: #9EA0A6;
}}
/* Background */
[data-testid="stAppViewContainer"] {{
  background: radial-gradient(1200px 800px at 10% -10%, rgba(193,165,236,0.10), transparent 60%),
              radial-gradient(1000px 600px at 90% 10%, rgba(193,165,236,0.08), transparent 60%),
              linear-gradient(180deg, #0B0B11 0%, #0E0E14 100%);
  color: var(--text);
}}
/* Remove default padding top */
.block-container {{
  padding-top: 1.5rem;
}}
/* Hero */
.hero {{
  display: grid; gap: .5rem;
}}
.badge {{
  display:inline-block; padding:.25rem .55rem; font-size:.8rem; letter-spacing:.08em;
  border-radius:999px; color:#111; background: linear-gradient(135deg, #fff, #f6f2ff);
  border: 1px solid rgba(255,255,255,.5);
}}
h1.hero-title {{
  margin:0;
  font-size: clamp(2rem, 5vw, 3rem);
  line-height: 1.1;
  background: linear-gradient(90deg, #ffffff 10%, var(--jumper) 90%);
  -webkit-background-clip: text; background-clip: text; color: transparent;
  font-weight: 800;
}}
.hero-sub {{
  color: var(--muted);
  margin-top:.3rem;
}}
/* Cards */
.card {{
  background: var(--card);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 18px;
  padding: 18px 16px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.06);
  backdrop-filter: blur(8px);
}}
.card.kpi {{
  padding: 16px 16px;
}}
.kpi-label {{
  color: var(--muted); font-size:.85rem; margin-bottom:.25rem;
}}
.kpi-value {{
  font-size: clamp(1.4rem, 3vw, 1.9rem); font-weight: 800; letter-spacing:.2px;
  background: linear-gradient(90deg, #fff 0%, var(--jumper) 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}}
/* Inputs & buttons */
.stTextInput > div > div > input {{
  background: rgba(255,255,255,0.06)!important;
  border: 1px solid rgba(255,255,255,0.16)!important;
  color: var(--text)!important;
}}
.stDateInput > div > div > input {{
  background: rgba(255,255,255,0.06)!important;
  border: 1px solid rgba(255,255,255,0.16)!important;
  color: var(--text)!important;
}}
.stButton>button, .stDownloadButton>button {{
  background: linear-gradient(135deg, var(--jumper), #a47fe6);
  border: none;
  color: #111;
  font-weight: 700;
  border-radius: 12px;
  padding: .6rem 1rem;
  box-shadow: 0 8px 24px rgba(193,165,236,0.35);
}}
.stButton>button:hover, .stDownloadButton>button:hover {{
  transform: translateY(-1px);
  box-shadow: 0 12px 28px rgba(193,165,236,0.45);
}}
/* Dataframe tweaks */
[data-testid="stDataFrame"] div[role="grid"] {{
  border-radius: 14px; overflow: hidden;
  border: 1px solid rgba(255,255,255,0.12);
}}
/* Hide Streamlit default header/footer */
header[data-testid="stHeader"] {{ background: transparent; }}
footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# --------- HERO ---------
st.markdown("""
<div class="hero">
  <span class="badge">Jumper • LI.FI</span>
  <h1 class="hero-title">Cross-chain Analytics</h1>
  <div class="hero-sub">Analyze bridges & swaps for any EVM wallet • clean insights • instant results</div>
</div>
""", unsafe_allow_html=True)
st.markdown("")  # spacer

# --------- FORM ---------
with st.container():
    with st.form("params"):
        c1, c2, c3 = st.columns([2,1,1])
        with c1:
            wallet = st.text_input("Wallet address (EVM)", placeholder="0x…")
        with c2:
            default_start = dt.date.today() - dt.timedelta(days=30)
            since = st.date_input("Since", value=default_start)
        with c3:
            submitted = st.form_submit_button("Analyze 🔍")

if submitted:
    # basic guard
    if not wallet or not wallet.startswith("0x") or len(wallet) < 10:
        st.error("Please enter a valid EVM address (starts with 0x).")
        st.stop()

    # override global in your module (no address stored anywhere)
    jv.WALLET = wallet.strip()

    # Fetch chains
    with st.spinner("Loading chains…"):
        chain_map = jv.fetch_chains()
    if not chain_map:
        st.error("Could not load chains metadata.")
        st.stop()

    # Fetch & process transfers
    from_date_str = since.strftime("%Y-%m-%d")
    with st.spinner("Fetching transfers & computing stats…"):
        txs = jv.fetch_and_process_data(from_date_str, chain_map)

    if not txs:
        st.warning("No transfers found for this period.")
        st.stop()

    # Analyze
    analyzer = jv.TransactionAnalyzer()
    ok = analyzer.analyze_transactions(txs)
    if not ok:
        st.warning("No analyzable data returned.")
        st.stop()

    # --------- KPIs ---------
    def kpi_card(label, value):
        col = st.container()
        with col:
            st.markdown(f"""
            <div class="card kpi">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    colA, colB, colC, colD = st.columns(4)
    with colA: kpi_card("Transfers", f"{len(analyzer.transactions):,}")
    with colB: kpi_card("Bridges", f"{analyzer.bridges:,}")
    with colC: kpi_card("Swaps", f"{analyzer.swaps:,}")
    with colD: kpi_card("Chains used", f"{len(analyzer.blockchains):,}")

    colE, colF, colG = st.columns(3)
    with colE: kpi_card("Total USD", f"${analyzer.total_value:,.2f}")
    with colF: kpi_card("Bridges USD", f"${analyzer.bridge_value:,.2f}")
    with colG: kpi_card("Swaps USD", f"${analyzer.swap_value:,.2f}")

    st.markdown("")

    # --------- DATAFRAME ---------
    df = pd.DataFrame(txs)

    # Build a date column if we have timestamps
    if "timestamp" in df.columns:
        df["date"] = pd.to_datetime(df["timestamp"], unit="s", utc=True).dt.tz_convert("UTC").dt.date

    # --------- CHARTS (Plotly, brand color) ---------
    st.markdown("### Insights")
    tab1, tab2, tab3 = st.tabs(["📈 Daily USD volume", "🏷️ Platforms", "⛓️ Chains usage"])

    with tab1:
        if "date" in df.columns and "usd" in df.columns:
            daily = df.groupby("date")["usd"].sum().reset_index()
            fig = px.area(
                daily, x="date", y="usd",
                title=None,
            )
            fig.update_traces(line_color=PRIMARY, fill="tozeroy")
            fig.update_layout(
                height=360, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#EDECF8", margin=dict(l=10,r=10,t=10,b=10),
                xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No 'date' / 'usd' columns available for the chart.")

    with tab2:
        platforms = None
        # if your analyzer exposes a dict of platforms, use it; otherwise compute from df['platform']
        if hasattr(analyzer, "platforms") and analyzer.platforms:
            platforms = analyzer.platforms
        elif "platform" in df.columns:
            platforms = df["platform"].value_counts().to_dict()

        if platforms:
            pf = pd.DataFrame([{"platform": k, "count": v} for k, v in platforms.items()])
            pf = pf.sort_values("count", ascending=False)
            fig = px.bar(pf, x="platform", y="count", title=None)
            fig.update_traces(marker_color=PRIMARY)
            fig.update_layout(
                height=360, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#EDECF8", margin=dict(l=10,r=10,t=10,b=10),
                xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No platform data.")

    with tab3:
        # Combine from_chain and to_chain counts if available
        chain_counts = None
        cols = [c for c in ["from_chain", "to_chain"] if c in df.columns]
        if cols:
            chain_counts = (
                pd.concat([df[c] for c in cols])
                .value_counts()
                .reset_index()
                .rename(columns={"index":"chain", 0:"count"})
            )
            fig = px.bar(chain_counts, x="chain", y="count", title=None)
            fig.update_traces(marker_color=PRIMARY)
            fig.update_layout(
                height=360, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#EDECF8", margin=dict(l=10,r=10,t=10,b=10),
                xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No chain columns found ('from_chain'/'to_chain').")

    # --------- TABLE + EXPORT ---------
    st.markdown("### Transfers")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, height=520)
    st.markdown('</div>', unsafe_allow_html=True)
    st.download_button("📥 Download CSV", df.to_csv(index=False).encode("utf-8"),
                       "transfers.csv", "text/csv")

else:
    # Nice empty state
    st.markdown("""
    <div class="card">
      <b>Tip</b>: paste any EVM wallet to explore cross-chain activity.
      The input is empty by design — we never store nor prefill addresses.
    </div>
    """, unsafe_allow_html=True)
