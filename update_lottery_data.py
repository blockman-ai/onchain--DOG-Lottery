import requests, json, random
from datetime import datetime, timedelta
from decimal import Decimal
import os

LOTTERY_ADDRESS = "bc1psewn5hprrlhhcze9x9lcpd74wmpy26cwaxpzc270v8x0h9kt3kls6hrax4"
CREATOR_ADDRESS = "bc1prhcdy4ytncv8xgq0xwtqg0gfk2t38asddq3ex7xxa43dxhrfhkhsn6yhk9"
API_URL = f"https://open-api.unisat.io/v1/indexer/address/{LOTTERY_ADDRESS}/rune/txs"
WINNERS_FILE = "winners_history.json"

headers = {"accept": "application/json"}
entries = []
cutoff_time = datetime.utcnow() - timedelta(hours=24)

def convert_rune_amount(raw_amount: str) -> float:
    return float(Decimal(raw_amount) / Decimal(1e9))

try:
    res = requests.get(API_URL, headers=headers)
    txs = res.json()["data"]["transactions"]

    for tx in txs:
        tx_time = datetime.utcfromtimestamp(tx.get("blocktime", datetime.utcnow().timestamp()))
        if tx_time >= cutoff_time:
            for t in tx.get("transfers", []):
                if t["tick"] == "DOG" and t["to"] == LOTTERY_ADDRESS:
                    entries.append({
                        "txid": tx["txid"],
                        "amount": round(convert_rune_amount(t["amount"]), 4),
                        "timestamp": tx_time.isoformat()
                    })

    total = sum(e["amount"] for e in entries)
    winner = random.choice(entries) if entries else {"txid": "none", "amount": 0}

    status = {
        "live_pot_total": total,
        "payout_to_winner": round(total * 0.75, 4),
        "rollover_to_next_round": round(total * 0.20, 4),
        "creator_fee": round(total * 0.05, 4),
        "winner": winner,
        "creator_address": CREATOR_ADDRESS
    }

    with open("lottery_entries.json", "w") as f:
        json.dump(entries, f, indent=2)

    with open("lottery_status.json", "w") as f:
        json.dump(status, f, indent=2)

    # Track winner per day
    today = datetime.utcnow().strftime('%Y-%m-%d')
    winners = {}
    if os.path.exists(WINNERS_FILE):
        with open(WINNERS_FILE, "r") as f:
            winners = json.load(f)
    winners[today] = winner
    with open(WINNERS_FILE, "w") as f:
        json.dump(winners, f, indent=2)

except Exception as e:
    print("Error:", e)
