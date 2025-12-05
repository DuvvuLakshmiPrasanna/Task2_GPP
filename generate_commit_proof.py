#!/usr/bin/env python3
import subprocess, sys, base64
from pathlib import Path
from typing import Optional
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

STUDENT_KEY_PATH = Path("student_private.pem")
INSTRUCTOR_KEY_PATH = Path("instructor_public.pem")

def get_latest_commit_hash() -> str:
    out = subprocess.check_output(["git", "log", "-1", "--format=%H"], stderr=subprocess.STDOUT)
    h = out.decode().strip()
    if len(h) != 40:
        raise ValueError(f"Unexpected commit hash length: {h!r}")
    int(h,16)
    return h

def load_private_key(path: Path, password: Optional[bytes] = None):
    pem = path.read_bytes()
    return serialization.load_pem_private_key(pem, password=password, backend=default_backend())

def load_public_key(path: Path):
    pem = path.read_bytes()
    return serialization.load_pem_public_key(pem, backend=default_backend())

def sign_message(message: str, private_key) -> bytes:
    message_bytes = message.encode("ascii")
    signature = private_key.sign(
        message_bytes,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    return signature

def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return ciphertext

def main():
    try:
        commit_hash = get_latest_commit_hash()
    except Exception as e:
        print(f"ERROR getting commit hash: {e}", file=sys.stderr); sys.exit(1)

    if not STUDENT_KEY_PATH.exists():
        print("ERROR: student_private.pem not found", file=sys.stderr); sys.exit(1)

    password_bytes = None

    try:
        student_priv = load_private_key(STUDENT_KEY_PATH, password=password_bytes)
    except TypeError as e:
        print("Private key may be encrypted. If so, set password_bytes.", file=sys.stderr)
        print(f"Load error: {e}", file=sys.stderr); sys.exit(1)
    except Exception as e:
        print(f"ERROR loading private key: {e}", file=sys.stderr); sys.exit(1)

    try:
        sig = sign_message(commit_hash, student_priv)
    except Exception as e:
        print(f"ERROR signing: {e}", file=sys.stderr); sys.exit(1)

    if not INSTRUCTOR_KEY_PATH.exists():
        print("ERROR: instructor_public.pem not found", file=sys.stderr); sys.exit(1)

    try:
        instr_pub = load_public_key(INSTRUCTOR_KEY_PATH)
    except Exception as e:
        print(f"ERROR loading instructor public key: {e}", file=sys.stderr); sys.exit(1)

    try:
        encrypted = encrypt_with_public_key(sig, instr_pub)
    except Exception as e:
        print(f"ERROR encrypting signature: {e}", file=sys.stderr); sys.exit(1)

    b64 = base64.b64encode(encrypted).decode("ascii")

    Path("signature.bin").write_bytes(sig)
    Path("encrypted_signature.b64").write_text(b64)

    print(f"Commit Hash: {commit_hash}")
    print(f"Encrypted Signature (base64): {b64}")

if __name__ == "__main__":
    main()
