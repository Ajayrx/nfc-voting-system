# Project Ncrypt - Hardware Prototype

🧠 This is a simulated hardware prototype for NFC-based voter verification using:
- ✅ Government-signed NFC Cards
- 🔒 Fingerprint Hash Matching
- 🚨 Fake Card Detection

## Files
- `nfc_reader.py` – Simulates scanning NFC cards
- `fingerprint_hash.py` – Simulates fingerprint scanning
- `voter_verification.py` – Core logic combining both verifications
- `test/test_verification.py` – Runs multiple test cases
- `cards/fake_and_real_cards.json` – Optional card database

This prototype is ready to be extended to real Raspberry Pi hardware with NFC and biometric modules.

# 🚀 How to Run
## ✅ Step 1: Install Dependencies
Make sure you're inside the project root directory. Then install the required packages:

   > pip install -r requirements.txt

[Python 3.9+ recommended.]

## ▶️ Step 2: Run the GUI
Launch the full graphical simulation by running:

   > python main/gui_app.py

This will open an interactive dashboard with:

- Card input & service access
- 3D-style card interactions
- Display of user details and service eligibility