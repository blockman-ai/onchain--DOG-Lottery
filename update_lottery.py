import requests, json, random
from datetime import datetime, timedelta

LOTTERY_ADDRESS = "bc1psewn5hprrlhhcze9x9lcpd74wmpy26cwaxpzc270v8x0h9kt3kls6hrax4"
CREATOR_ADDRESS = "bc1prhcdy4ytncv8xgq0xwtqg0gfk2t38asddq3ex7xxa43dxhrfhkhsn6yhk9"
API_URL = f"https://open-api.unisat.io/v1/indexer/address/{LOTTERY_ADDRESS}/rune/txs"

headers = {"accept": "application/json"}
entries = []

try:
    res = requests.get(API_URL, headers=headers)
    txs = res.json()["data"]["transactions"]

    # Only include txs from the last 24 hours
    cutoff_time = datetime.utcnow() - timedelta(hours=24)

    for tx in txs:
        tx_time = datetime.utcfromtimestamp(tx.get("blocktime", datetime.utcnow().timestamp()))
        if tx_time >= cutoff_time:
            for t in tx.get("transfers", []):
                if t["tick"] == "DOG" and t["to"] == LOTTERY_ADDRESS:
                    entries.append({
                        "txid": tx["txid"],
                        "amount": int(t["amount"]),
                        "timestamp": tx_time.isoformat()
                    })

    total = sum(e["amount"] for e in entries)
    winner = random.choice(entries) if entries else {"txid": "none", "amount": 0}

    status = {
        "live_pot_total": total,
        "payout_to_winner": int(total * 0.75),
        "rollover_to_next_round": int(total * 0.20),
        "creator_fee": int(total * 0.05),
        "winner": winner,
        "creator_address": CREATOR_ADDRESS
    }

    with open("lottery_entries.json", "w") as f:
        json.dump(entries, f, indent=2)

    with open("lottery_status.json", "w") as f:
        json.dump(status, f, indent=2)

except Exception as e:
    print("Error:", e)
