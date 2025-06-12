import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import serial
import serial.tools.list_ports
from datetime import datetime
import time

class CardWriterApp:
    def __init__(self, root):
        self.root = root
        root.title("Government Voter Card Issuance")
        root.geometry("600x550")

        self.arduino = None
        self.port_var = tk.StringVar()

        self.create_widgets()
        self.detect_ports()

    def create_widgets(self):
        ttk.Label(self.root, text="VOTER CARD PERSONALIZATION",
                  font=("Arial", 14, "bold")).pack(pady=10)

        conn_frame = ttk.LabelFrame(self.root, text="Arduino Connection")
        conn_frame.pack(fill=tk.X, padx=20, pady=5)

        ttk.Label(conn_frame, text="Select Port:").grid(row=0, column=0, padx=5)
        self.port_combo = ttk.Combobox(conn_frame, textvariable=self.port_var, width=20)
        self.port_combo.grid(row=0, column=1, padx=5)

        ttk.Button(conn_frame, text="Refresh Ports", command=self.detect_ports).grid(row=0, column=2, padx=5)
        ttk.Button(conn_frame, text="Connect", command=self.connect_arduino).grid(row=0, column=3, padx=5)
        ttk.Button(conn_frame, text="Disconnect", command=self.disconnect_arduino).grid(row=0, column=4, padx=5)
        ttk.Button(conn_frame, text="Reset Arduino", command=self.reset_arduino).grid(row=0, column=5, padx=5)
        


        self.conn_status = ttk.Label(conn_frame, text="Status: Not connected", foreground="red")
        self.conn_status.grid(row=1, column=0, columnspan=6, pady=5)

        log_frame = ttk.LabelFrame(self.root, text="Communication Log")
        log_frame.pack(fill=tk.BOTH, padx=20, pady=5, expand=True)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=8)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.config(state=tk.DISABLED)

        form = ttk.LabelFrame(self.root, text="Voter Information")
        form.pack(fill=tk.X, padx=20, pady=10)

        fields = [
            ("Name", 0, 30),
            ("Voter ID", 1, 20),
            ("Age", 2, 5),
            ("Constituency", 3, 20),
            ("Fingerprint Hash (10-12 digits)", 4, 20)
        ]

        self.entries = {}
        for field, row, width in fields:
            ttk.Label(form, text=field + ":").grid(row=row, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(form, width=width)
            entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=5)
            self.entries[field] = entry

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame, text="Write Card", command=self.write_card).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Exit", command=self.root.destroy).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text="Read Card", command=self.read_card).grid(row=0, column=3, padx=10)

    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def detect_ports(self):
        self.log_message("Scanning for available ports...")
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo['values'] = ports
        if ports:
            self.port_var.set(ports[0])
            self.log_message(f"Found ports: {', '.join(ports)}")
        else:
            self.log_message("No serial ports found")

    def connect_arduino(self):
        port = self.port_var.get()
        if not port:
            self.log_message("Error: No port selected")
            return

        try:
            if self.arduino and self.arduino.is_open:
                self.arduino.close()

            self.arduino = serial.Serial(port, 115200, timeout=0.1)
            self.arduino.setDTR(False)
            time.sleep(0.05)
            self.arduino.setDTR(True)

            self.log_message(f"Attempting connection to {port}...")
            time.sleep(1.5)
            self.arduino.reset_input_buffer()

            read_buffer = ""
            start_time = time.time()
            while time.time() - start_time < 5:
                if self.arduino.in_waiting > 0:
                    char = self.arduino.read(1).decode(errors='ignore')
                    read_buffer += char
                    if "READY" in read_buffer:
                        self.arduino.timeout = 3
                        self.conn_status.config(text=f"Status: Connected to {port}", foreground="green")
                        self.log_message(f"Connected to {port} - Arduino is READY. Full buffer: '{read_buffer.strip()}'")
                        return
                time.sleep(0.01)

            self.arduino.close()
            self.arduino = None
            self.conn_status.config(text="Status: Connection failed", foreground="red")
            self.log_message(f"Connection failed: 'READY' not received. Received: '{read_buffer.strip()}'")

        except Exception as e:
            if self.arduino and self.arduino.is_open:
                self.arduino.close()
            self.arduino = None
            self.log_message(f"Connection error: {str(e)}")

    def disconnect_arduino(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
        self.arduino = None
        self.conn_status.config(text="Status: Disconnected", foreground="red")
        self.log_message("Disconnected from Arduino")

    def reset_arduino(self):
        if self.arduino and self.arduino.is_open:
            try:
                self.arduino.setDTR(False)
                time.sleep(0.1)
                self.arduino.setDTR(True)
                self.log_message("Reset signal sent to Arduino")
            except Exception as e:
                self.log_message(f"Error resetting Arduino: {str(e)}")
        else:
            self.log_message("Arduino not connected")

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.log_message("Form cleared")

    def check_connection(self):
        if not self.arduino or not self.arduino.is_open:
            self.log_message("Error: Arduino not connected")
            return False
    
        try:
            self.arduino.write(b"PING\n")
            response = self.arduino.readline().decode().strip()
            if response == "ALIVE":
                return True
            else:
                self.conn_status.config(text="Status: Connection lost", foreground="red")
                self.log_message(f"Ping failed. Received: {response}")
                return False
        except Exception as e:
            self.conn_status.config(text="Status: Connection lost", foreground="red")
            self.log_message(f"Communication error: {str(e)}")
            return False
    
    def write_card(self):
        if not self.check_connection():
            return
    
    # Get the data from the entries
        name = self.entries["Name"].get().strip()
        voter_id = self.entries["Voter ID"].get().strip()
        age = self.entries["Age"].get().strip()
        constituency = self.entries["Constituency"].get().strip()
        fingerprint = self.entries["Fingerprint Hash (10-12 digits)"].get().strip()
    
        if not all([name, voter_id, age, constituency, fingerprint]):
            self.log_message("Error: All fields must be filled")
            return
    
    # Format the data
        data_string = f"{name}|{voter_id}|{age}|{constituency}|{fingerprint}\n"
    
        try:
        # Notify Arduino to be ready for card information
            self.arduino.write(b"WRITE\n")
            response = self.arduino.readline().decode().strip()

            if response == "GOT_WRITE":
                self.log_message("Arduino acknowledged, sending card data...")
                self.arduino.write(data_string.encode())
            
            # Wait for response from Arduino
                final_response = self.arduino.readline().decode().strip()
            
                if final_response == "SUCCESS":
                    messagebox.showinfo("Success", f"Card written successfully!\\nIssued: {voter_id}")
                    self.clear_form()
                elif final_response.startswith("ERROR:"):
                    messagebox.showerror("Error", f"Arduino error: {final_response[6:]}")
                else:
                    messagebox.showerror("Error", f"Arduino returned unexpected: {final_response}")
        
            else:
                self.log_message(f"Unexpected response from Arduino: {response}")
                messagebox.showerror("Error", f"Unexpected response from Arduino: {response}")
        
        except serial.SerialException as e:
            self.log_message(f"Serial communication error: {e}")
            messagebox.showerror("Error", f"Serial communication error: {e}")
        except Exception as e:
            self.log_message(f"General error: {e}")
            messagebox.showerror("Error", f"General error: {e}")

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.log_message("Form cleared.")


    def read_card(self):
        if not self.arduino or not self.arduino.is_open:
            self.log_message("Cannot read card: Arduino not connected.")
            return

        try:
            self.arduino.reset_input_buffer()
            self.log_message("Waiting for card...")

            start_time = time.time()
            buffer = ""
            card_lines = []

            while time.time() - start_time < 10:
                if self.arduino.in_waiting > 0:
                    line = self.arduino.readline().decode(errors='ignore').strip()
                    if line:
                        self.log_message(f"> {line}")
                        if line.startswith("BLOCK"):
                            card_lines.append(line)
                else:
                    time.sleep(0.05)

            if card_lines:
                # Optionally parse blocks to auto-fill form (if format is consistent)
                self.log_message("Card read successfully.")
            else:
                self.log_message("No card data received.")

        except Exception as e:
            self.log_message(f"Error reading card: {str(e)}")


# Main loop
if __name__ == "__main__":
    root = tk.Tk()
    app = CardWriterApp(root)
    root.mainloop()
