import os


def str_to_bool(value):
    """Convert string to boolean."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes", "on")
    return bool(value)


PORT = 443

# name -> secret (32 hex chars)
USERS = {
    "tg": os.environ.get("TG_KEY", "00000000000000000000000000000001"),
    #    "tg2": "0123456789abcdef0123456789abcdef",
}

# Makes the proxy harder to detect
# Can be incompatible with very old clients
SECURE_ONLY = str_to_bool(os.environ.get("SECURE_ONLY", "True"))

# Makes the proxy even more hard to detect
# Compatible only with the recent clients
TLS_ONLY = str_to_bool(os.environ.get("TLS_ONLY", "True"))

# The domain for TLS, bad clients are proxied there
# Use random existing domain, proxy checks it on start
TLS_DOMAIN = os.environ.get("TLS_DOMAIN", "www.google.com")

# Tag for advertising, obtainable from @MTProxybot
AD_TAG = os.environ.get("AD_TAG", "3c09c680b76ee91a4c25ad51f742267d")

# SOCKS5 proxy for outgoing connections (optional)
# Uncomment and configure if you need to route traffic through a SOCKS5 proxy
SOCKS5_HOST = os.environ.get("SOCKS5_HOST", None)
SOCKS5_PORT = int(os.environ.get("SOCKS5_PORT")) if os.environ.get("SOCKS5_PORT") else None
SOCKS5_USER = os.environ.get("SOCKS5_USER", None)
SOCKS5_PASS = os.environ.get("SOCKS5_PASS", None)
