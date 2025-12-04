from pathlib import Path
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

# --------------------------
# CONFIG
# --------------------------
PRIVATE_KEY_FILE = "student_private.pem"
SEED_FILE = Path("data/seed.txt")  # Save inside project data folder
Path("data").mkdir(parents=True, exist_ok=True)  # Create folder if missing

# --------------------------
# Load Private Key
# --------------------------
def load_private_key():
    with open(PRIVATE_KEY_FILE, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

# --------------------------
# Decrypt Seed
# --------------------------
def decrypt_seed(encrypted_seed_b64: str) -> str:
    private_key = load_private_key()
    encrypted_seed_b64 = encrypted_seed_b64.strip().replace("\n", "").replace(" ", "")
    missing_padding = len(encrypted_seed_b64) % 4
    if missing_padding != 0:
        encrypted_seed_b64 += "=" * (4 - missing_padding)

    encrypted_bytes = base64.b64decode(encrypted_seed_b64)
    decrypted_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    decrypted_seed = decrypted_bytes.decode("utf-8")
    return decrypted_seed

# --------------------------
# MAIN
# --------------------------
if __name__ == "__main__":
    # Read the encrypted seed from file
    with open("encrypted_seed.txt", "r") as f:
        encrypted_seed_b64 = f.read().strip()

    # Decrypt
    seed = decrypt_seed(encrypted_seed_b64)

    # Save decrypted seed
    with open(SEED_FILE, "w") as f:
        f.write(seed)

    print(f"Decrypted Seed: {seed}")
    print(f"Seed saved successfully at {SEED_FILE}")
