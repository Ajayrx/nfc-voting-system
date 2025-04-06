# it handle's both NFC and fingerprint validation

from main.nfc_reader import read_nfc_card
from utils.encryption import decrypt_data
from main.fingerprint_hash import capture_fingerprint, hash_fingerprint

def verify_voter():
    print("\n[🔍] Scanning NFC card...")
    encrypted_data = read_nfc_card()
    decrypted = decrypt_data(encrypted_data)

    print("\n📇 Voter Info:")
    print(f" - ID: {decrypted['voter_id']}")
    print(f" - Name: {decrypted['name']}")

    if decrypted["gov_signature"] != "valid":
        print("[❌] FAKE CARD DETECTED")
        return

    print("\n✋ Please scan your fingerprint...")
    user_fp = capture_fingerprint()
    user_hash = hash_fingerprint(user_fp)

    if user_hash == decrypted["fingerprint_hash"]:
        print("[✅] Fingerprint match. Vote allowed.")
    else:
        print("[❌] Fingerprint mismatch. Access denied.")

if __name__ == "__main__":
    verify_voter()
