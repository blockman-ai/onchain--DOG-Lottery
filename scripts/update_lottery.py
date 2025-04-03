import json
import random
from datetime import datetime, timedelta

# Simulated data (replace with API data later)
transactions = [
    {"txid": "tx001", "amount": 10},
    {"txid": "tx002", "amount": 20},
    {"txid": "tx003", "amount": 30}
]

# Calculate pot distribution
total_pot = sum(tx["amount"] for tx in transactions)
winner_payout = round(total_pot * 0.75, 2)
rollover = round(total_pot * 0.20, 2)
creator_fee = round(total_pot * 0.05, 2)
winner = random.choice(transactions)

# 1. Save lottery_status.json
lottery_status = {
    "live_pot_total": total_pot,
    "payout_to_winner": winner_payout,
    "rollover_to_next_round": rollover,
    "creator_fee": creator_fee,
    "winner": winner
}

with open("lottery_status.json", "w") as f:
    json.dump(lottery_status, f, indent=2)

# 2. Save lottery_entries.json
for tx in transactions:
    tx["timestamp"] = datetime.utcnow().isoformat()

with open("lottery_entries.json", "w") as f:
    json.dump(transactions, f, indent=2)
