from datetime import datetime, timedelta
import json
import random

# Simulate detection of real transactions to bc1psewn... address with DOG Rune
DOG_RUNE_ID = "618ffb4e23e19566c7567841187a1c424dfd775e4f8cb633a7a3d4836784835fi0"
lottery_address = "bc1psewn5hprrlhhcze9x9lcpd74wmpy26cwaxpzc270v8x0h9kt3kls6hrax4"

# Simulated transaction results from mempool.space API
simulated_transactions = [
    {"txid": "tx001", "amount": 10, "to_address": lottery_address, "rune_id": DOG_RUNE_ID},
    {"txid": "tx002", "amount": 20, "to_address": lottery_address, "rune_id": DOG_RUNE_ID},
    {"txid": "tx003", "amount": 15, "to_address": "bc1xyz", "rune_id": DOG_RUNE_ID},
    {"txid": "tx004", "amount": 8, "to_address": lottery_address, "rune_id": "other_rune"}
]

# Filter valid DOG Rune entries to the correct address
valid_entries = []
for tx in simulated_transactions:
    if tx["to_address"] == lottery_address and tx["rune_id"] == DOG_RUNE_ID:
        valid_entries.append({
            "txid": tx["txid"],
            "amount": tx["amount"],
            "timestamp": datetime.utcnow().isoformat()
        })

# Save to lottery_entries.json
entries_output_path = "/mnt/data/lottery_entries.json"
with open(entries_output_path, "w") as f:
    json.dump(valid_entries, f, indent=2)

entries_output_path
