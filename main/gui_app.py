import sys
import os
import json
import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style
from ttkbootstrap.widgets import Entry, Button, Label, Frame
import tkinter as tk
from tkinter import Toplevel



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.encryption import encrypt_data, decrypt_data

CARD_PATH = "data/voter_card.txt"
EXPECTED_GOV_SIGNATURE = "gov_secure_2025"

def show_fake_card_alert():
    alert = Toplevel(root)
    alert.title("⚠️ Fake Card Detected")
    alert.geometry("450x180")
    alert.configure(bg="#ff4c4c")
    Label(alert, text="❌ FAKE NFC CARD DETECTED", font=("Segoe UI", 16, "bold"), foreground="white", background="#ff4c4c").pack(pady=30)
    Button(alert, text="Dismiss", bootstyle="danger", command=alert.destroy).pack(pady=5)

def write_card(voter_id, name, age, fingerprint_hash):
    data = {
        "voter_id": voter_id,
        "name": name,
        "age": age,
        "fingerprint_hash": fingerprint_hash,
        "gov_signature": EXPECTED_GOV_SIGNATURE
    }
    encrypted = encrypt_data(data)
    with open(CARD_PATH, "w") as f:
        json.dump({"encrypted": encrypted}, f)
    messagebox.showinfo("Success", "✅ Voter data encrypted and written to NFC card.")

def read_card():
    if not os.path.exists(CARD_PATH):
        messagebox.showerror("Error", "❌ No NFC card found.")
        return

    with open(CARD_PATH, "r") as f:
        encrypted_data = json.load(f)["encrypted"]

    try:
        decrypted = decrypt_data(encrypted_data)
        entered_signature = gov_sig_entry.get().strip()
        signature_valid = (decrypted['gov_signature'] == entered_signature)

        result = f"""
🔐 Voter Data Scanned:
----------------------
🆔 Voter ID: {decrypted['voter_id']}
🙍 Name: {decrypted['name']}
🎂 Age: {decrypted['age']}
🔏 Fingerprint Hash: {decrypted['fingerprint_hash']}
{'✅ Signature: Valid' if signature_valid else '❌ Signature: Invalid Card'}
        """

        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, result)

        if not signature_valid:
            show_fake_card_alert()

    except Exception as e:
        messagebox.showerror("Error", f"⚠️ Decryption failed: {e}")


style = Style("darkly")  
root = style.master
root.title("🗳️ Project Ncrypt - NFC Voter Verification")
root.state("zoomed")

main_frame = Frame(root, padding=30)
main_frame.pack(pady=10)

Label(main_frame, text="🆔 Voter ID", font=("Segoe UI", 11)).pack(pady=4)
voter_id_entry = Entry(main_frame, width=60)
voter_id_entry.pack()

Label(main_frame, text="🙍 Name", font=("Segoe UI", 11)).pack(pady=4)
name_entry = Entry(main_frame, width=60)
name_entry.pack()

Label(main_frame, text="🎂 Age", font=("Segoe UI", 11)).pack(pady=4)
age_entry = Entry(main_frame, width=60)
age_entry.pack()

Label(main_frame, text="🔏 Fingerprint Hash", font=("Segoe UI", 11)).pack(pady=4)
fingerprint_entry = Entry(main_frame, width=60)
fingerprint_entry.pack()

Label(main_frame, text="🔐 Enter Government Signature", font=("Segoe UI", 11)).pack(pady=4)
gov_sig_entry = Entry(main_frame, width=60)
gov_sig_entry.pack()

Label(main_frame, text=f"✅ Official Gov Signature: {EXPECTED_GOV_SIGNATURE}", font=("Segoe UI", 9), foreground="gray").pack(pady=5)

Button(main_frame, text="✅ Encrypt and Write to NFC Card", bootstyle="success outline", width=40, command=lambda: write_card(
    voter_id_entry.get(),
    name_entry.get(),
    age_entry.get(),
    fingerprint_entry.get()
)).pack(pady=10)

Button(main_frame, text="📡 Scan NFC Card", bootstyle="info outline", width=40, command=read_card).pack(pady=5)

Label(main_frame, text="📋 Output:", font=("Segoe UI", 11)).pack(pady=5)
output_box = tk.Text(main_frame, height=15, width=100, font=("Consolas", 10))
output_box.pack(pady=10)

root.mainloop()
