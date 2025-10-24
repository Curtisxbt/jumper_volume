#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script unifié pour analyser les volumes de transactions Jumper Exchange
Version optimisée : tout en mémoire, sans écriture de fichiers intermédiaires
"""
import datetime as dt
import time
import requests
import json
import re
from collections import defaultdict

# ==================== CONFIGURATION ====================
API_URL = "https://li.quest/v2/analytics/transfers"
CHAINS_URL = "https://chainid.network/chains.json"
INTEGRATOR = "jumper.exchange"
WALLET = None  

# ==================== UTILITAIRES ====================
def to_unix(ts_str: str) -> int:
    """Convertit une date YYYY-MM-DD en timestamp Unix"""
    d = dt.datetime.strptime(ts_str, "%Y-%m-%d").replace(tzinfo=dt.timezone.utc)
    return int(d.timestamp())

def shorten_tx(tx: str) -> str:
    """Raccourcit un hash de transaction"""
    return tx[:6] + "..." + tx[-4:] if tx else ""

def usd_fmt(x):
    """Formate un montant en USD"""
    if x is None:
        return "$0.0000"
    return f"${x:,.4f}".replace(",", " ")

def amt_fmt(raw_amount, decimals):
    """Formate un montant de token"""
    if raw_amount is None or decimals is None:
        return "0.0000"
    try:
        val = int(raw_amount) / (10 ** decimals)
        return f"{val:.4f}"
    except:
        return "0.0000"

def iso_and_relative(utc_ts: int) -> str:
    """Formate un timestamp en date relative et ISO"""
    now = dt.datetime.now(dt.timezone.utc)
    t = dt.datetime.fromtimestamp(utc_ts, tz=dt.timezone.utc)
    delta = now - t
    mins = int(delta.total_seconds() // 60)
    hours = mins // 60
    rem_m = mins % 60
    rel = []
    if hours > 0:
        rel.append(f"{hours} hours")
    if rem_m > 0 or hours == 0:
        rel.append(f"{rem_m} minutes")
    rel_str = ", ".join(rel) + " ago"
    iso_str = t.strftime("%d %b %Y (%H:%M UTC)")
    return f"{rel_str} • {iso_str}"

# ==================== GESTION DES CHAÎNES ====================
def fetch_chains() -> dict:
    """Télécharge et retourne la liste des blockchains (en mémoire)"""
    print("\n🔄 Récupération de la liste des blockchains...")
    try:
        r = requests.get(CHAINS_URL, timeout=30)
        r.raise_for_status()
        chains = r.json()
        
        mapping = {}
        for c in chains:
            try:
                cid = c.get("chainId")
                name = c.get("name")
                if cid and name:
                    mapping[int(cid)] = name
            except Exception:
                continue
        
        print(f"✅ {len(mapping)} chaînes récupérées")
        return mapping
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des chaînes: {e}")
        return {}

# ==================== RÉCUPÉRATION DES DONNÉES ====================
def fetch_all(wallet: str, from_ts: int, to_ts: int, limit: int = 200):
    """Récupère toutes les transactions via l'API"""
    params = {
        "wallet": wallet,
        "fromTimestamp": from_ts,
        "toTimestamp": to_ts,
        "status": "ALL",
        "integrator": INTEGRATOR,
        "limit": limit,
    }
    out = []
    next_cursor = None
    session = requests.Session()
    
    print("🔥 Récupération des transactions...")
    while True:
        if next_cursor:
            params["next"] = next_cursor
        else:
            params.pop("next", None)
        
        try:
            r = session.get(API_URL, params=params, timeout=30)
            r.raise_for_status()
            data = r.json()
            out.extend(data.get("data", []))
            
            if not data.get("hasNext"):
                break
            next_cursor = data.get("next")
            time.sleep(0.1)
        except Exception as e:
            print(f"❌ Erreur lors de la récupération: {e}")
            break
    
    return out

def build_transaction_dict(item: dict, chain_map: dict) -> dict:
    """Construit un dictionnaire de transaction structuré"""
    sending = item.get("sending", {}) or {}
    receiving = item.get("receiving", {}) or {}
    tool = item.get("tool") or ""
    shash = sending.get("txHash") or receiving.get("txHash")
    when_ts = sending.get("timestamp") or receiving.get("timestamp") or 0
    
    # From
    s_amt = amt_fmt(sending.get("amount"), (sending.get("token") or {}).get("decimals"))
    s_tok = (sending.get("token") or {}).get("symbol") or ""
    s_chain = chain_map.get(sending.get("chainId"), f"Chain {sending.get('chainId')}")
    s_usd = None
    try:
        s_price = float((sending.get("token") or {}).get("priceUSD") or 0)
        if sending.get("amount") and (sending.get("token") or {}).get("decimals") is not None:
            s_usd = (int(sending["amount"]) / (10 ** (sending["token"]["decimals"]))) * s_price
    except:
        pass
    
    # To
    r_amt = amt_fmt(receiving.get("amount"), (receiving.get("token") or {}).get("decimals"))
    r_tok = (receiving.get("token") or {}).get("symbol") or ""
    r_chain = chain_map.get(receiving.get("chainId"), f"Chain {receiving.get('chainId')}")
    r_usd = None
    try:
        r_price = float((receiving.get("token") or {}).get("priceUSD") or 0)
        if receiving.get("amount") and (receiving.get("token") or {}).get("decimals") is not None:
            r_usd = (int(receiving["amount"]) / (10 ** (receiving["token"]["decimals"]))) * r_price
    except:
        pass
    
    return {
        'tx_id': shorten_tx(shash),
        'timestamp': int(when_ts),
        'from_token': s_tok,
        'from_blockchain': s_chain,
        'from_amount': float(s_amt.replace(" ", "")),
        'to_token': r_tok,
        'to_blockchain': r_chain,
        'to_amount': float(r_amt.replace(" ", "")),
        'usd_value': s_usd or r_usd or 0,
        'platform': tool
    }

def fetch_and_process_data(from_date: str, chain_map: dict):
    """Récupère et traite les données de transactions (en mémoire)"""
    from_ts = to_unix(from_date)
    to_ts = int(dt.datetime.now(dt.timezone.utc).timestamp())
    
    raw_data = fetch_all(WALLET, from_ts, to_ts, limit=200)
    raw_data.sort(key=lambda x: (x.get("sending", {}) or {}).get("timestamp", 0), reverse=True)
    
    transactions = []
    for item in raw_data:
        try:
            tx = build_transaction_dict(item, chain_map)
            if tx['tx_id'] and tx['from_token'] and tx['to_token']:
                transactions.append(tx)
        except:
            continue
    
    print(f"✅ {len(transactions)} transactions récupérées et traitées")
    return transactions

# ==================== ANALYSE DES DONNÉES ====================
class TransactionAnalyzer:
    def __init__(self):
        self.transactions = []
        self.platforms = defaultdict(int)
        self.blockchains = set()
        self.bridges = 0
        self.swaps = 0
        self.bridge_value = 0.0
        self.swap_value = 0.0
        self.total_value = 0.0
    
    def analyze_transactions(self, transactions: list):
        """Analyse les transactions à partir d'une liste de dictionnaires"""
        if not transactions:
            print("❌ Aucune transaction à analyser!")
            return False
        
        for tx in transactions:
            self.blockchains.add(tx['from_blockchain'])
            self.blockchains.add(tx['to_blockchain'])
            
            platform = tx.get('platform', 'Unknown Platform')
            self.platforms[platform] += 1
            
            # Bridge vs Swap
            if tx['from_blockchain'] == tx['to_blockchain']:
                self.swaps += 1
                self.swap_value += tx['usd_value']
            else:
                self.bridges += 1
                self.bridge_value += tx['usd_value']
            
            self.total_value += tx['usd_value']
        
        self.transactions = transactions
        return True
    
    def print_results(self):
        """Affiche les résultats de l'analyse"""
        print("\n" + "=" * 60)
        print("📊 ANALYSE DES TRANSACTIONS BLOCKCHAIN")
        print("=" * 60)
        
        print(f"\n📈 STATISTIQUES GÉNÉRALES")
        print(f"   • Total des transactions : {len(self.transactions)}")
        print(f"   • Total des bridges : {self.bridges}")
        print(f"   • Total des swaps : {self.swaps}")
        print(f"   • Nombre de blockchains utilisées : {len(self.blockchains)}")
        
        print(f"\n💰 VALEURS EN DOLLARS")
        print(f"   • Valeur totale : ${self.total_value:,.2f}")
        print(f"   • Valeur des bridges : ${self.bridge_value:,.2f}")
        print(f"   • Valeur des swaps : ${self.swap_value:,.2f}")
        
        if self.total_value > 0:
            bridge_pct = (self.bridge_value / self.total_value) * 100
            swap_pct = (self.swap_value / self.total_value) * 100
            print(f"   • % Bridges : {bridge_pct:.1f}%")
            print(f"   • % Swaps : {swap_pct:.1f}%")
        
        print(f"\n🔗 BLOCKCHAINS UTILISÉES ({len(self.blockchains)})")
        for i, blockchain in enumerate(sorted(self.blockchains), 1):
            print(f"   {i}. {blockchain}")
        
        print(f"\n🪐 RÉPARTITION PAR PLATEFORME")
        sorted_platforms = sorted(self.platforms.items(), key=lambda x: x[1], reverse=True)
        for platform, count in sorted_platforms:
            percentage = (count / len(self.transactions)) * 100
            print(f"   • {platform} : {count} transaction(s) ({percentage:.1f}%)")
        
        print("=" * 60 + "\n")

# ==================== FONCTION PRINCIPALE ====================
def main():
    print("\n" + "=" * 60)
    print("🚀 JUMPER VOLUME ANALYZER - Version Mémoire")
    print("=" * 60)
    
    # Récupération de la liste des chaînes (en mémoire)
    chain_map = fetch_chains()
    
    if not chain_map:
        print("❌ Impossible de récupérer la liste des blockchains!")
        return
    
    # Demande de la date de début
    from_date = input("\n📅 Date de début (YYYY-MM-DD): ").strip()
    
    # Récupération et traitement des transactions (en mémoire)
    transactions = fetch_and_process_data(from_date, chain_map)
    
    if not transactions:
        print("❌ Aucune transaction trouvée!")
        return
    
    # Analyse des transactions
    analyzer = TransactionAnalyzer()
    if analyzer.analyze_transactions(transactions):
        analyzer.print_results()

if __name__ == "__main__":
    main()