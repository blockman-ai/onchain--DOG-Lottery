import requests
import json
from datetime import datetime
import random

# Constants
DOG_RUNE_ID = "618ffb4e23e19566c7567841187a1c424dfd775e4f8cb633a7a3d4836784835fi0"
LOTTERY_ADDRESS = "bc1psewn5hprrlhhcze9x9lcpd74wmpy26cwaxpzc270v8x0h9kt3kls6hrax4"
CREATOR_ADDRESS = "bc1prhcdy4ytncv8xgq0xwtqg0gfk2t38asddq3ex7xxa43dxhrfhkhsn6yhk9"

# Mempool API to get transactions for the address (confirmed + mempool)
API_URL = f"https://mempool.space/api/address/{LOTTERY_ADDRESS}/txs"

try:
    response = requests.get(API_URL)
    response.raise_for_status()
    txs = response.json()

    # Simulate filtering by Rune ID (we'll assume every tx here is a $DOG Rune transfer)
    # In production: you would verify rune ID and amount with ord or Hiro API
    entries = []
    for tx in txs:
        txid = tx["txid"]
        # Simulated $DOG amount assumption
        simulated_amount = random.randint(5, 100)
        entries.append({
            "txid": txid,
            "amount": simulated_amount,
            "timestamp": datetime.utcnow().isoformat()
        })

    # Calculate pot
    total_pot = sum(tx["amount"] for tx in entries)
    winner = random.choice(entries) if entries else {"txid": "none", "amount": 0}

    payout = {
        "live_pot_total": total_pot,
        "payout_to_winner": round(total_pot * 0.75, 2),
        "rollover_to_next_round": round(total_pot * 0.20, 2),
        "creator_fee": round(total_pot * 0.05, 2),
        "winner": winner,
        "creator_address": CREATOR_ADDRESS
    }

    # Save to JSON files
    with open("/mnt/data/lottery_entries.json", "w") as f:
        json.dump(entries, f, indent=2)

    with open("/mnt/data/lottery_status.json", "w") as f:
        json.dump(payout, f, indent=2)

    result = {
        "total_entries": len(entries),
        "winner": winner,
        "lottery_status": payout
    }

except Exception as e:
    result = {"error": str(e)}

result
