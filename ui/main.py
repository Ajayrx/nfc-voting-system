import tkinter as tk
from tkinter import messagebox
import logic  # Import logic for NFC and fingerprint validation

selected_card = None  # Store the selected NFC card globally

# Function to handle NFC selection
def select_nfc(card_id):
    global selected_card
    is_valid, message = logic.validate_nfc(card_id)
    
    if is_valid:
        selected_card = card_id  # Store selected card
        messagebox.showinfo("Success", message)
        proceed_to_fingerprint()  # Move to fingerprint step
    else:
        messagebox.showerror("Error", message)

# Function to move to fingerprint verification
def proceed_to_fingerprint():
    lbl_status.config(text="✅ NFC Verified! Proceed to Fingerprint", fg="green")
    btn_fingerprint.config(state=tk.NORMAL)  # Enable fingerprint button

# Function to verify fingerprint
def verify_fingerprint():
    global selected_card
    if selected_card:
        is_match = logic.verify_fingerprint(selected_card)
        if is_match:
            messagebox.showinfo("Success", "✅ Fingerprint Matched! You can vote.")
            lbl_status.config(text="✅ Fingerprint Matched! Proceed to Voting.", fg="blue")
        else:
            messagebox.showerror("Error", "Fingerprint Mismatch! Try Again.")
            lbl_status.config(text="❌ Fingerprint Mismatch! Try Again.", fg="red")

# Tkinter UI Setup
root = tk.Tk()
root.title("NFC-Based Voting System")
root.geometry("500x400")

# Title Label
lbl_title = tk.Label(root, text="Tap Your NFC Card", font=("Arial", 14, "bold"))
lbl_title.pack(pady=10)

# NFC Card Buttons
frame_cards = tk.Frame(root)
frame_cards.pack()

# Generate NFC Cards
nfc_cards = logic.get_nfc_cards()  # Use pre-generated cards
card_buttons = []

for card in nfc_cards:
    btn = tk.Button(
        frame_cards, text=f"NFC Card {card['id']}", 
        width=15, height=3, 
        bg="lightblue" if card["genuine"] else "red",
        command=lambda c=card['id']: select_nfc(c)
    )
    btn.pack(side=tk.LEFT, padx=10, pady=10)
    card_buttons.append(btn)

# Status Label
lbl_status = tk.Label(root, text="", font=("Arial", 12))
lbl_status.pack(pady=10)

# Fingerprint Verification Button (Initially Disabled)
btn_fingerprint = tk.Button(root, text="Verify Fingerprint", state=tk.DISABLED, command=verify_fingerprint)
btn_fingerprint.pack(pady=10)

# Run Tkinter Main Loop
root.mainloop()
