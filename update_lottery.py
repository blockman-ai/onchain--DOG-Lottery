import requests
import json
from datetime import datetime

# 1. CONFIG
DOG_ADDRESS = "bc1psewn5hprrlhhcze9x9lcpd74wmpy26cwaxpzc270v8x0h9kt3kls6hrax4"
MEMPOOL_API = f"https://mempool.space/api/address/{DOG_ADDRESS}/txs"
OUTPUT_PATH = "lottery_entries.json"

# 2. FETCH TXs
try:
    res = requests.get(MEMPOOL_API)
    res.raise_for_status()
    txs = res.json()
except Exception as e:
    print("Error fetching mempool data:", e)
    txs = []

# 3. EXTRACT ENTRIES (simulated for now)
entries = []
for tx in txs:
    txid = tx["txid"]
    timestamp = datetime.utcfromtimestamp(tx["status"]["block_time"]).isoformat() if tx["status"]["confirmed"] else datetime.utcnow().isoformat()
    for vout in tx.get("vout", []):
        if vout["scriptpubkey_address"] == DOG_ADDRESS and vout["value"] > 500:
            entries.append({
                "txid": txid,
                "amount": round(vout["value"] / 1000, 2),  # Simulate DOG = value / 1000 sats
                "timestamp": timestamp
            })

# 4. FALLBACK FOR TESTING
if not entries:
    entries = [
        {"txid": "sim-tx001", "amount": 10, "timestamp": datetime.utcnow().isoformat()},
        {"txid": "sim-tx002", "amount": 20, "timestamp": datetime.utcnow().isoformat()}
    ]

# 5. SAVE
with open(OUTPUT_PATH, "w") as f:
    json.dump(entries, f, indent=2)
