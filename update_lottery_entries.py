import json
import requests
from datetime import datetime

# Your $DOG Rune receiving address
lottery_address = "bc1psewn5hprrlhhcze9x9lcpd74wmpy26cwaxpzc270v8x0h9kt3kls6hrax4"

# Mempool API endpoint (change if using another instance)
MEMPOOL_API = f"https://mempool.space/api/address/{lottery_address}/txs"

# Fetch recent transactions to the lottery address
response = requests.get(MEMPOOL_API)
if response.status_code != 200:
    raise Exception("Failed to fetch transactions from Mempool API")

txs = response.json()
entries = []

# Loop through transactions and extract Rune-relevant ones (simulate for now)
for tx in txs:
    txid = tx["txid"]
    timestamp = datetime.utcfromtimestamp(tx["status"]["block_time"]).isoformat() if tx["status"]["confirmed"] else datetime.utcnow().isoformat()

    # Simulated: Extracting $DOG Rune amount from transaction outputs (normally you'd need a Rune indexer)
    amount = 10  # <-- Placeholder for actual Rune detection logic

    entries.append({
        "txid": txid,
        "amount": amount,
        "timestamp": timestamp
    })

# Save as JSON
with open("lottery_entries.json", "w") as f:
    json.dump(entries, f, indent=2)

print(f"Updated lottery_entries.json with {len(entries)} entries.")
