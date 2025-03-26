import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # For image handling
import logic

def reveal_card(index, buttons, lbl_message, proceed_button, card_images):
    """ Handle card selection logic and update UI. """
    card = logic.generated_cards[index]
    
    if not card["is_real"]:
        lbl_message.config(text=f"❌ Fake Card! Reason: {card['reason']}", fg="red")
        buttons[index].config(image=card_images["fake"])  # Change to fake card image
    elif card["already_voted"]:
        lbl_message.config(text="⚠️ Already Voted!", fg="orange")
        buttons[index].config(image=card_images["voted"])  # Change to already voted card image
    else:
        lbl_message.config(text="✅ Valid Card! Proceed to Fingerprint", fg="green")
        buttons[index].config(image=card_images["real"])  # Change to real card image
        proceed_button.config(state=tk.NORMAL)  # Enable fingerprint step
    
    # Reset all buttons to default image
    for i, btn in enumerate(buttons):
        if i != index:
            btn.config(image=card_images["default"])

def create_ui(root, proceed_to_fingerprint):
    """ Create the main UI for NFC card selection. """
    root.title("NFC Voting System")
    root.geometry("600x500")

    lbl_title = tk.Label(root, text="Tap Your NFC Card", font=("Arial", 16, "bold"))
    lbl_title.pack(pady=10)

    frame = tk.Frame(root)
    frame.pack()

    # Load images
    card_images = {
        "default": ImageTk.PhotoImage(Image.open("images/card_default.jpg").resize((100, 150))),
        "real": ImageTk.PhotoImage(Image.open("images/card_revealed_real.jpg").resize((100, 150))),
        "fake": ImageTk.PhotoImage(Image.open("images/card_revealed_fake.jpg").resize((100, 150))),
        "voted": ImageTk.PhotoImage(Image.open("images/card_revealed_voted.jng").resize((100, 150))),
    }

    buttons = []
    for i in range(4):
        btn = tk.Button(frame, image=card_images["default"], command=lambda i=i: reveal_card(i, buttons, lbl_message, btn_proceed, card_images))
        btn.grid(row=0, column=i, padx=10, pady=10)
        buttons.append(btn)

    lbl_message = tk.Label(root, text="Select a card to proceed", font=("Arial", 12))
    lbl_message.pack(pady=10)

    btn_proceed = tk.Button(root, text="Proceed to Fingerprint", state=tk.DISABLED, command=proceed_to_fingerprint)
    btn_proceed.pack(pady=20)

    return lbl_message, btn_proceed
