import json
import random
from datetime import datetime

# Simulated list of transactions (replace with API integration later)
transactions = [
    {"txid": "tx001", "amount": 10},
    {"txid": "tx002", "amount": 20},
    {"txid": "tx003", "amount": 30}
]

# Calculate pot totals
total_pot = sum(tx["amount"] for tx in transactions)
winner_payout = round(total_pot * 0.75, 2)
rollover = round(total_pot * 0.20, 2)
creator_fee = round(total_pot * 0.05, 2)
winner = random.choice(transactions)

# Generate JSON for dashboard
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

# Save current entries
entries_path = "/mnt/data/lottery_entries.json"
with open(entries_path, "w") as f:
    json.dump(transactions, f, indent=2)

# Save current status
status_path = "/mnt/data/lottery_status.json"
with open(status_path, "w") as f:
    json.dump(lottery_status, f, indent=2)

entries_path, status_path
