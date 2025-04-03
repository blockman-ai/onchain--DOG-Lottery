import json
import random
import hashlib
from datetime import datetime

# Path to your lottery entries file
ENTRIES_FILE = "lottery_entries.json"

def load_entries():
    try:
        with open(ENTRIES_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading entries: {e}")
        return []

def pick_winner(entries):
    if not entries:
        print("No entries found!")
        return None

    # Use current UTC time as seed (replace with block hash for production)
    seed_input = str(datetime.utcnow())
    seed = int(hashlib.sha256(seed_input.encode("utf-8")).hexdigest(), 16)
    random.seed(seed)
    
    winner = random.choice(entries)
    return winner

def main():
    entries = load_entries()
    print(f"Total entries: {len(entries)}")
    
    winner = pick_winner(entries)
    if winner:
        print("The winner is:")
        print(json.dumps(winner, indent=2))
    else:
        print("No winner could be selected.")

if __name__ == "__main__":
    main()
