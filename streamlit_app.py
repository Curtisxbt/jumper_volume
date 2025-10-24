# =========================
#  Jumper – Modern UI (Streamlit)
#  Theme color: #C1A5EC
#  Version: "mega KPIs" + no on-page table + month-start default
# =========================
import datetime as dt
import pandas as pd
import plotly.express as px
import streamlit as st

import jumper_volume as jv  # ton module

PRIMARY = "#C1A5EC"
DARK = "#0B0B11"
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
[data-testid="stAppViewContainer"] {{
  background: radial-gradient(1200px 800px at 10% -10%, rgba(193,165,236,0.10), transparent 60%),
              radial-gradient(1000px 600px at 90% 10%, rgba(193,165,236,0.08), transparent 60%),
              linear-gradient(180deg, #0B0B11 0%, #0E0E14 100%);
  color: var(--text);
}}
.block-container {{ padding-top: 1.5rem; }}
.hero {{ display: grid; gap: .5rem; }}
.badge {{
  display:inline-block; padding:.25rem .55rem; font-size:.8rem; letter-spacing:.08em;
  border-radius:999px; color:#111; background: linear-gradient(135deg, #fff, #f6f2ff);
  border: 1px solid rgba(255,255,255,.5);
}}
h1.hero-title {{
  margin:0; font-size: clamp(2rem, 5vw, 3rem); line-height: 1.1;
  background: linear-gradient(90deg, #ffffff 10%, var(--jumper) 90%);
  -webkit-background-clip: text; background-clip: text; color: transparent; font-weight: 800;
}}
.hero-sub {{ color: var(--muted); margin-top:.3rem; }}

/* MEGA KPIs */
.mega-grid {{
  display:grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 18px; margin: 12px 0 6px;
}}
.mega-card {{
  background: var(--card);
  border: 1.5px solid rgba(193,165,236,0.35);
  border-radius: 22px;
  padding: 22px 24px;
  box-shadow: 0 12px 40px rgba(193,165,236,0.12), inset 0 1px 0 rgba(255,255,255,0.06);
  backdrop-filter: blur(10px);
}}
.mega-label {{
  color: var(--muted); font-size: .95rem; letter-spacing: .04em; margin-bottom: .25rem;
}}
.mega-value {{
  font-size: clamp(2.3rem, 6vw, 3.8rem);
  font-weight: 900; letter-spacing: .3px;
  background: linear-gradient(90deg, #fff 0%, var(--jumper) 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}}

/* Inputs & buttons */
.stTextInput > div > div > input,
.stDateInput > div > div > input {{
  background: rgba(255,255,255,0.06)!important;
  border: 1px solid rgba(255,255,255,0.16)!important;
  color: var(--text)!important;
}}
.stButton>button, .stDownloadButton>button {{
  background: linear-gradient(135deg, var(--jumper), #a47fe6);
  border: none; color: #111; font-weight: 800;
  border-radius: 14px; padding: .7rem 1.1rem;
  box-shadow: 0 8px 24px rgba(193,165,236,0.35);
}}
.stButton>button:hover, .stDownloadButton>button:hover {{
  transform: translateY(-1px);
  box-shadow: 0 12px 28px rgba(193,165,236,0.45);
}}

/* Hide default header/footer */
header[data-testid="stHeader"] {{ background: transparent; }}
footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# --------- HERO ---------
st.markdown("""
<div class="hero">
  <span class="badge">Jumper • LI.FI</span>
  <h1 class="hero-title">Cross-chain Analytics</h1>
  <div class="hero-sub">Analyze bridges & swaps for any EVM wallet — instant insights</div>
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
            today = dt.date.today()
            first_of_month = today.replace(day=1)  # ⬅️ défaut = 1er jour du mois en cours
            since = st.date_input("Since", value=first_of_month)
        with c3:
            submitted = st.form_submit_button("Analyze 🔍")

if submitted:
    # basic guard
    if not wallet or not wallet.startswith("0x") or len(wallet) < 10:
        st.error("Please enter a valid EVM address (starts with 0x).")
        st.stop()

    # override in your module (no address stored)
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

    # --------- MEGA KPIs (the 3 big ones) ---------
    transfers_count = f"{len(analyzer.transactions):,}"
    bridge_usd = f"${analyzer.bridge_value:,.2f}"
    swap_usd   = f"${analyzer.swap_value:,.2f}"

    st.markdown(
        f"""
        <div class="mega-grid">
          <div class="mega-card">
            <div class="mega-label">Transfers</div>
            <div class="mega-value">{transfers_count}</div>
          </div>
          <div class="mega-card">
            <div class="mega-label">Bridge USD</div>
            <div class="mega-value">{bridge_usd}</div>
          </div>
          <div class="mega-card">
            <div class="mega-label">Swap USD</div>
            <div class="mega-value">{swap_usd}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("")

    # --------- CHARTS (conservés) ---------
    df = pd.DataFrame(txs)
    if "timestamp" in df.columns:
        df["date"] = pd.to_datetime(df["timestamp"], unit="s", utc=True).dt.tz_convert("UTC").dt.date

    st.markdown("### Insights")
    tab1, tab2, tab3 = st.tabs(["📈 Daily USD volume", "🏷️ Platforms", "⛓️ Chains usage"])

    with tab1:
        if "date" in df.columns and "usd" in df.columns:
            daily = df.groupby("date")["usd"].sum().reset_index().sort_values("date")
            fig = px.area(daily, x="date", y="usd", title=None)
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
        if hasattr(analyzer, "platforms") and analyzer.platforms:
            platforms = analyzer.platforms
        elif "platform" in df.columns:
            platforms = df["platform"].value_counts().to_dict()
        if platforms:
            pf = pd.DataFrame([{"platform": k, "count": v} for k, v in platforms.items()]).sort_values("count", ascending=False)
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

    # --------- EXPORT ONLY (no on-page table) ---------
    st.markdown("""
    <div class="mega-card" style="margin-top:12px;">
      <b>Need all raw transfers?</b><br/>
      Download the full CSV below — the detailed table is intentionally hidden on the page.
    </div>
    """, unsafe_allow_html=True)
    st.download_button("📥 Download CSV", df.to_csv(index=False).encode("utf-8"),
                       "transfers.csv", "text/csv")

else:
    # Empty state
    st.markdown("""
    <div class="mega-card">
      Paste any EVM wallet to explore cross-chain activity.
      Inputs are empty by design — we never prefill addresses.
    </div>
    """, unsafe_allow_html=True)
