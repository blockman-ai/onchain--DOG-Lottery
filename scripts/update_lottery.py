import requests
import json
import random
from datetime import datetime

ADDRESS = "bc1psewn5hprrlhhcze9x9lcpd74wmpy26cwaxpzc270v8x0h9kt3kls6hrax4"
API_URL = f"https://mempool.space/api/address/{ADDRESS}/txs"

# Get recent transactions from mempool
response = requests.get(API_URL)
txs = response.json()

transactions = []
for tx in txs:
    # Estimate amount from outputs going to your address
    for vout in tx.get("vout", []):
        if vout["scriptpubkey_address"] == ADDRESS:
            amount = round(vout["value"] / 100_000_000, 8)  # Convert sats to BTC
            transactions.append({
                "txid": tx["txid"],
                "amount": amount
            })

# --- Lottery Logic ---
total_pot = sum(tx["amount"] for tx in transactions)
winner_payout = round(total_pot * 0.75, 8)
rollover = round(total_pot * 0.20, 8)
creator_fee = round(total_pot * 0.05, 8)
winner = random.choice(transactions) if transactions else {"txid": "none", "amount": 0}

# --- Save JSON Output ---
lottery_status = {
    "live_pot_total": total_pot,
    "payout_to_winner": winner_payout,
    "rollover_to_next_round": rollover,
    "creator_fee": creator_fee,
    "winner": winner
}

with open("lottery_entries.json", "w") as f:
    json.dump(transactions, f, indent=2)

with open("lottery_status.json", "w") as f:
    json.dump(lottery_status, f, indent=2)
