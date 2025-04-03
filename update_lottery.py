import json
import requests
import random
from datetime import datetime

# CONFIG
LOTTERY_ADDRESS = "bc1psewn5hprrlhhcze9x9lcpd74wmpy26cwaxpzc270v8x0h9kt3kls6hrax4"
DOG_RUNE_ID = "618ffb4e23e19566c7567841187a1c424dfd775e4f8cb633a7a3d4836784835fi0"

# STEP 1: Fetch transactions from Mempool.space API
def fetch_transactions(address):
    url = f"https://mempool.space/api/address/{address}/txs"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Failed to fetch txs:", e)
        return []

# STEP 2: Simulate DOG Rune detection
def simulate_dog_entries(transactions):
    entries = []
    for tx in transactions:
        if "txid" in tx:
            entries.append({
                "txid": tx["txid"],
                "amount": random.choice([10, 20, 50]),  # Simulated DOG amount
                "timestamp": datetime.utcnow().isoformat()
            })
    return entries

# STEP 3: Pick winner and calculate pot
def calculate_lottery(entries):
    total = sum(e["amount"] for e in entries)
    winner = random.choice(entries) if entries else {"txid": "none", "amount": 0}
    return {
        "live_pot_total": total,
        "payout_to_winner": round(total * 0.75, 2),
        "rollover_to_next_round": round(total * 0.20, 2),
        "creator_fee": round(total * 0.05, 2),
        "winner": winner
    }

# MAIN FLOW
txs = fetch_transactions(LOTTERY_ADDRESS)
entries = simulate_dog_entries(txs)
status = calculate_lottery(entries)

# SAVE OUTPUT FILES
with open("/mnt/data/lottery_entries.json", "w") as f:
    json.dump(entries, f, indent=2)

with open("/mnt/data/lottery_status.json", "w") as f:
    json.dump(status, f, indent=2)

"/mnt/data/lottery_entries.json and /mnt/data/lottery_status.json generated."
