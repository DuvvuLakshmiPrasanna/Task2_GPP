import pyotp
from pathlib import Path

SEED_FILE = Path("/data/seed.txt")
CRON_LOG_FILE = Path("/cron/last_code.txt")

if SEED_FILE.exists():
    with SEED_FILE.open("r") as f:
        seed = f.read().strip()
    totp = pyotp.TOTP(seed)
    code = totp.now()
    with CRON_LOG_FILE.open("w") as f:
        f.write(code)
