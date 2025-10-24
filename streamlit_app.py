import streamlit as st
import datetime as dt
import pandas as pd

# On importe ton script
import jumper_volume as jv

st.set_page_config(page_title="Jumper Volume Analyzer", page_icon="🔗", layout="wide")
st.title("🔗 Jumper Volume Analyzer")
st.caption("UI simple et gratuite (Streamlit).")

# Formulaire
with st.form("form"):
    wallet = st.text_input("Adresse du wallet (EVM)", value="")
    since = st.date_input("Analyser depuis (YYYY-MM-DD)", value=dt.date.today() - dt.timedelta(days=30))
    submitted = st.form_submit_button("Analyser")

if submitted:
    if not wallet or not wallet.startswith("0x") or len(wallet) < 10:
        st.error("Merci d’entrer une adresse EVM valide.")
        st.stop()

    # 1) On met à jour la variable globale du module pour utiliser ton wallet
    jv.WALLET = wallet.strip()

    # 2) On récupère la liste des blockchains
    with st.spinner("Chargement des blockchains…"):
        chain_map = jv.fetch_chains()
    if not chain_map:
        st.error("Impossible de récupérer la liste des blockchains.")
        st.stop()

    # 3) On récupère les transactions (ton code le fait déjà)
    from_date_str = since.strftime("%Y-%m-%d")
    with st.spinner("Récupération des transactions…"):
        txs = jv.fetch_and_process_data(from_date_str, chain_map)

    if not txs:
        st.warning("Aucune transaction trouvée sur la période.")
        st.stop()

    # 4) Analyse (ta classe existante)
    analyzer = jv.TransactionAnalyzer()
    ok = analyzer.analyze_transactions(txs)
    if not ok:
        st.warning("Pas de données analysables.")
        st.stop()

    # 5) Affichage des KPIs (tirés des attributs de ta classe)
    st.subheader("KPIs")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Transferts", len(analyzer.transactions))
    c2.metric("Bridges", analyzer.bridges)
    c3.metric("Swaps", analyzer.swaps)
    c4.metric("Blockchains utilisées", len(analyzer.blockchains))

    c5, c6, c7 = st.columns(3)
    c5.metric("Valeur totale (USD)", f"${analyzer.total_value:,.2f}")
    c6.metric("Bridges (USD)", f"${analyzer.bridge_value:,.2f}")
    c7.metric("Swaps (USD)", f"${analyzer.swap_value:,.2f}")

    # 6) Tableau (toutes les colonnes retournées par ton build_transaction_dict)
    st.subheader("Détails des transactions")
    df = pd.DataFrame(txs)
    st.dataframe(df, use_container_width=True, height=500)

    # 7) Export
    st.download_button("📥 Télécharger CSV", df.to_csv(index=False).encode("utf-8"),
                       file_name="transfers.csv", mime="text/csv")