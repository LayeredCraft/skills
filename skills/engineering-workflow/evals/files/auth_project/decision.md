# Token validation decision

Validate expiry before signatures to reject stale credentials cheaply. Compare HMAC signatures with a constant-time primitive to avoid timing leakage. Expiry is exclusive: a token is invalid when current time equals `expires_at`.
