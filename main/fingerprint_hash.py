# Placeholder for fingerprint capture, later link with actual sensor

import hashlib

def capture_fingerprint():
    return input("Place your finger: ")

def hash_fingerprint(data):
    return hashlib.sha256(data.encode()).hexdigest()
