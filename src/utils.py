import hashlib
import secrets
import string
from datetime import datetime, timedelta

def generate_short_code(length: int = 6) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def is_expired(expires_at: datetime) -> bool:
    if not expires_at:
        return False
    return datetime.now() > expires_at

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()