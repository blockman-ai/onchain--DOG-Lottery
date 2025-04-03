import json
import random
from datetime import datetime
import requests

# Constants
ADDRESS = "bc1psewn5hprrlhhcze9x9lcpd74wmpy26cwaxpzc270v8x0h9kt3kls6hrax4"
MEMPOOL_API_URL = f"https://mempool.space/api/address/{ADDRESS}/txs"

# Fetch transactions from mempool.space
try:
    response = requests.get(MEMPOOL_API_URL)
    response.raise_for_status()
    txs = response.json()
except Exception as e:
    print("Error fetching transactions from mempool.space:", e)
    txs = []

# Extract valid outputs sent to the address
transactions = []
for tx in txs:
    for vout in tx.get("vout", []):
        if vout.get("scriptpubkey_address") == ADDRESS:
            amount = round(vout["value"] / 100_000_000, 8)  # Convert sats to BTC/DOG
            transactions.append({
                "txid": tx["txid"],
                "amount": amount,
                "timestamp": datetime.utcnow().isoformat()
            })

# Fallback if no valid entries found
if not transactions:
    transactions = [
        {"txid": "sim-tx001", "amount": 10, "timestamp": datetime.utcnow().isoformat()},
        {"txid": "sim-tx002", "amount": 20, "timestamp": datetime.utcnow().isoformat()}
    ]

# Calculate pot
total_pot = sum(tx["amount"] for tx in transactions)
winner_payout = round(total_pot * 0.75, 8)
rollover = round(total_pot * 0.20, 8)
creator_fee = round(total_pot * 0.05, 8)
winner = random.choice(transactions)

# 1. Save lottery_status.json
lottery_status = {
    "live_pot_total": total_pot,
    "payout_to_winner": winner_payout,
    "rollover_to_next_round": rollover,
    "creator_fee": creator_fee,
    "winner": {
        "txid": winner["txid"],
        "amount": winner["amount"]
    }
}

with open("lottery_status.json", "w") as f:
    json.dump(lottery_status, f, indent=2)

# 2. Save lottery_entries.json
with open("lottery_entries.json", "w") as f:
    json.dump(transactions, f, indent=2)

print("Lottery data updated successfully.")
