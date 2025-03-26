import random
import hashlib

# Sample NFC Cards Storage
nfc_cards = [
    {"id": "1001", "genuine": True, "fingerprint_hash": "f8b4a4"},
    {"id": "1002", "genuine": True, "fingerprint_hash": "d2c9f3"},
    {"id": "2001", "genuine": False, "fingerprint_hash": "invalid"},
    {"id": "2002", "genuine": False, "fingerprint_hash": "invalid"},
]

# Return NFC card list
def get_nfc_cards():
    return nfc_cards

# Validate NFC card
def validate_nfc(nfc_id):
    for card in nfc_cards:
        if card["id"] == nfc_id:
            if card["genuine"]:
                return True, "✅ Genuine Card! Proceed to Fingerprint Scan."
            else:
                return False, "❌ Fake Card! Access Denied."
    return False, "❌ Invalid Card."

# Simulated Fingerprint Verification
def verify_fingerprint(nfc_id):
    for card in nfc_cards:
        if card["id"] == nfc_id and card["genuine"]:
            actual_fingerprint = card["fingerprint_hash"]
            entered_fingerprint = simulate_fingerprint_scan()
            return actual_fingerprint == entered_fingerprint
    return False

# Simulating a fingerprint scan by returning a matching hash for real cards
def simulate_fingerprint_scan():
    return random.choice(["f8b4a4", "d2c9f3", "invalid"])  # Fake or real fingerprints
