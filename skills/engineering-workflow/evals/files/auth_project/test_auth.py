from unittest.mock import patch

from auth import validate_token


@patch("auth.time.time", return_value=100)
def test_rejects_token_at_expiry(_time) -> None:
    assert validate_token(b"payload", "invalid", 100) is False


@patch("auth.time.time", return_value=100)
def test_rejects_invalid_signature_before_expiry(_time) -> None:
    assert validate_token(b"payload", "invalid", 101) is False
