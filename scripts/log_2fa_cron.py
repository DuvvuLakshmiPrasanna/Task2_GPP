#!/usr/bin/env python3
import os
import base64
import binascii
from datetime import datetime, timezone
import pyotp

SEED_FILE = "/data/seed.txt"

def read_seed_hex():
    try:
        with open(SEED_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def hex_to_base32(hex_seed):
    try:
        raw_bytes = binascii.unhexlify(hex_seed)
        return base64.b32encode(raw_bytes).decode("utf-8")
    except Exception:
        return None

def main():
    seed_hex = read_seed_hex()
    if not seed_hex:
        print("ERROR: seed.txt not found or empty")
        return

    seed_b32 = hex_to_base32(seed_hex)
    if not seed_b32:
        print("ERROR: Failed to convert hex to base32")
        return

    totp = pyotp.TOTP(seed_b32, digits=6)
    code = totp.now()

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    print(f"{timestamp} - 2FA Code: {code}")

if __name__ == "__main__":
    main()
