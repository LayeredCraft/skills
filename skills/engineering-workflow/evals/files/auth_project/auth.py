import hashlib
import hmac
import time


def validate_token(payload: bytes, signature: str, expires_at: int) -> bool:
    if expires_at <= int(time.time()):
        return False

    expected = hmac.new(b"fixture-key", payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
