import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

app = tb.Window(themename="solar")
app.title("Project Ncrypt – NFC Drag & Drop Simulation")
app.geometry("1100x650")

# ------------------ NFC Data ------------------
user_data = {
    "name": "Ajay Sharma",
    "age": 67,
    "blood": "O+",
    "ration_card": "RAT12345",
    "next_ration": "25-Apr-2025",
    "health_balance": 3500,
    "last_claim": "12-Feb-2025",
    "pension_id": "PEN99887",
    "pension_amt": 4000,
    "last_payout": "01-Apr-2025"
}

# ------------------ Output Label ------------------
output_label = tb.Label(app, text="", wraplength=350, justify="left", font=("Segoe UI", 10))
output_label.place(x=700, y=450)

# ------------------ Service Drop Zones ------------------
def create_service_zone(title, x, y, callback):
    frame = tb.LabelFrame(app, text=title, width=300, height=100, bootstyle="info")
    frame.place(x=x, y=y)

    def drop(event):
        callback()

    frame.bind("<Enter>", drop)
    return frame

def ration_info():
    output = (
        f"🛒 Ration Centre\n\n"
        f"👤 {user_data['name']}, Age {user_data['age']}\n"
        f"Ration Card: {user_data['ration_card']}\n"
        f"Eligible: Rice, Wheat, Oil\n"
        f"Next Delivery: {user_data['next_ration']}"
    )
    output_label.config(text=output)

def health_info():
    output = (
        f"🏥 Health Hospital\n\n"
        f"👤 {user_data['name']}\n"
        f"Blood Group: {user_data['blood']}\n"
        f"Balance: ₹{user_data['health_balance']}\n"
        f"Last Claim: {user_data['last_claim']}"
    )
    output_label.config(text=output)

def pension_info():
    if user_data['age'] < 60:
        output = f"🧓 {user_data['name']} is not eligible for pension."
    else:
        output = (
            f"🧓 Pension Centre\n\n"
            f"Pension ID: {user_data['pension_id']}\n"
            f"Monthly Pension: ₹{user_data['pension_amt']}\n"
            f"Last Payout: {user_data['last_payout']}"
        )
    output_label.config(text=output)

ration_zone = create_service_zone("🛒 Ration Centre", 700, 50, ration_info)
health_zone = create_service_zone("🏥 Health Hospital", 700, 170, health_info)
pension_zone = create_service_zone("🧓 Pension Centre", 700, 290, pension_info)

# ------------------ NFC Card (Draggable) ------------------
card = tk.Label(app, text="🔷 NFC Card", bg="#222", fg="white", font=("Segoe UI", 14, "bold"), width=15, height=5)
card.place(x=100, y=250)

def start_drag(event):
    card.startX = event.x
    card.startY = event.y

def do_drag(event):
    x = card.winfo_x() - card.startX + event.x
    y = card.winfo_y() - card.startY + event.y
    card.place(x=x, y=y)

card.bind("<Button-1>", start_drag)
card.bind("<B1-Motion>", do_drag)

app.mainloop()
