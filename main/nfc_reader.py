# Scans the real NFC card, decrypts and prints or display voter's info

def read_nfc_card():
    with open("data/voter_card.txt", "r") as f:
        return f.read()
