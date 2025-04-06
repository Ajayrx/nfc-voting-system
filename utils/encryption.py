import sys
sys.path.append("C:\\Users\\ajays\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages")

from Crypto.Cipher import AES
import base64
import json

SECRET_KEY = b'ThisIsASecretKey'  # Must be 16/24/32 bytes

def pad(data):
    while len(data) % 16 != 0:
        data += " "
    return data

def encrypt_data(data_dict):
    data_str = json.dumps(data_dict)
    padded = pad(data_str)
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(padded.encode())
    return base64.b64encode(encrypted).decode()

def decrypt_data(enc_data):
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(enc_data)).decode().rstrip()
    return json.loads(decrypted)
