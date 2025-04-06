# Encrypts and writes real voter data to card
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.encryption import encrypt_data
import json

def write_to_card():
    voter_data = {
        "voter_id": "VOTER123",
        "name": "Ajay Kumar",
        "age": 23,
        "fingerprint_hash": "ef797c8118f02dfb...",  # This is a hashed fingerprint
        "gov_signature": "valid"
    }

    encrypted = encrypt_data(voter_data)
    
    # Simulate writing to NFC by saving locally
    with open("data/voter_card.txt", "w") as f:
        f.write(encrypted)
    
    print("[💾] Encrypted voter data written to simulated NFC card.")

if __name__ == "__main__":
    write_to_card()
