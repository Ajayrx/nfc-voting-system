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

# 📁 Project Structure

nfc-voting-system/
├── data/
│   ├── voters.json                # Encrypted voter & service data
│   └── voter_card.txt             # Simulated NFC card dump
├── main/
│   ├── gui_app.py                 # ✅ GUI Simulation App (Interactive)  -- Voting
|   |── gui.py                     # -- Gov services
│   ├── nfc_reader.py              # NFC scan & validation logic
│   ├── write_to_nfc.py            # Writing voter data to NFC card
│   ├── voter_verification.py      # Fingerprint + card verification logic
│   └── fingerprint_hash.py        # Hashing user's fingerprint input
├── models/
│   └── fingerprint_match_model.tflite  # Fingerprint ML model [Working on]
├── utils/
│   └── encryption.py              # Data encryption/decryption functions
├── tests/
│   └── test_verification.py       # Test scripts
├── requirements.txt               # Project dependencies
└── README.md                      # You are here

# 🚀 How to Run
## ✅ Step 1: Install Dependencies
Make sure you're inside the project root directory. Then install the required packages:

   >pip install -r requirements.txt
[Python 3.9+ recommended.]

## ▶️ Step 2: Run the GUI
Launch the full graphical simulation by running:

   >python main/gui_app.py

This will open an interactive dashboard with:

- Card input & service access
- 3D-style card interactions
- Display of user details and service eligibility