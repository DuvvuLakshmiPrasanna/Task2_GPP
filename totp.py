import pyotp
import base64

# ------------------------------
# 1️⃣ Convert hex seed to Base32 and generate TOTP
# ------------------------------
def generate_totp_code(hex_seed: str) -> str:
    # Convert hex to bytes
    seed_bytes = bytes.fromhex(hex_seed)
    
    # Convert bytes to base32 string
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    
    # Create TOTP object (SHA-1, 30s, 6 digits)
    totp = pyotp.TOTP(base32_seed)
    
    # Generate current TOTP code
    return totp.now()


# ------------------------------
# 2️⃣ Verify a TOTP code
# ------------------------------
def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    # Convert hex to bytes
    seed_bytes = bytes.fromhex(hex_seed)
    
    # Convert bytes to base32 string
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    
    # Create TOTP object
    totp = pyotp.TOTP(base32_seed)
    
    # Verify code with window tolerance (±30s default)
    return totp.verify(code, valid_window=valid_window)


# ------------------------------
# Example usage
# ------------------------------
if __name__ == "__main__":
    # Read seed from Step 5
    with open("/data/seed.txt", "r") as f:
        hex_seed = f.read().strip()
    
    # Generate TOTP code
    code = generate_totp_code(hex_seed)
    print("Current TOTP Code:", code)
    
    # Verify code (example)
    is_valid = verify_totp_code(hex_seed, code)
    print("Verification result:", is_valid)
