import os


def str_to_bool(value):
    """Convert string to boolean."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes", "on")
    return bool(value)


# Listening port for the proxy
PORT = int(os.environ.get("PORT", 443))

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
SOCKS5_PORT = int(os.environ.get("SOCKS5_PORT", 0)) if os.environ.get("SOCKS5_PORT", "").isdigit() else None
SOCKS5_USER = os.environ.get("SOCKS5_USER", None)
SOCKS5_PASS = os.environ.get("SOCKS5_PASS", None)

# Buffer sizes (optional performance tuning)
# max socket buffer size to the client direction, the more the faster, but more RAM hungry
# Can be a single integer or a string like "16384,100,131072" for adaptive sizing (low,users_margin,high)
_to_clt_bufsize_env = os.environ.get("TO_CLT_BUFSIZE", None)
if _to_clt_bufsize_env:
    if "," in _to_clt_bufsize_env:
        TO_CLT_BUFSIZE = tuple(int(x.strip()) for x in _to_clt_bufsize_env.split(","))
    else:
        TO_CLT_BUFSIZE = int(_to_clt_bufsize_env)

# max socket buffer size to the telegram servers direction, also can be the tuple
_to_tg_bufsize_env = os.environ.get("TO_TG_BUFSIZE", None)
if _to_tg_bufsize_env:
    if "," in _to_tg_bufsize_env:
        TO_TG_BUFSIZE = tuple(int(x.strip()) for x in _to_tg_bufsize_env.split(","))
    else:
        TO_TG_BUFSIZE = int(_to_tg_bufsize_env)

# Performance and timing settings (optional)
# Statistics print period in seconds
_stats_print_period = os.environ.get("STATS_PRINT_PERIOD", None)
if _stats_print_period:
    STATS_PRINT_PERIOD = int(_stats_print_period)

# Client keepalive period in seconds
_client_keepalive = os.environ.get("CLIENT_KEEPALIVE", None)
if _client_keepalive:
    CLIENT_KEEPALIVE = int(_client_keepalive)

# Telegram server connect timeout in seconds
_tg_connect_timeout = os.environ.get("TG_CONNECT_TIMEOUT", None)
if _tg_connect_timeout:
    TG_CONNECT_TIMEOUT = int(_tg_connect_timeout)

# Network settings (optional)
# IPv4 listen address
_listen_addr_ipv4 = os.environ.get("LISTEN_ADDR_IPV4", None)
if _listen_addr_ipv4:
    LISTEN_ADDR_IPV4 = _listen_addr_ipv4

# IPv6 listen address
_listen_addr_ipv6 = os.environ.get("LISTEN_ADDR_IPV6", None)
if _listen_addr_ipv6:
    LISTEN_ADDR_IPV6 = _listen_addr_ipv6

# Prefer IPv6 for outgoing connections
_prefer_ipv6 = os.environ.get("PREFER_IPV6", None)
if _prefer_ipv6:
    PREFER_IPV6 = str_to_bool(_prefer_ipv6)

# Enable fast mode (disables some checks for better performance)
_fast_mode = os.environ.get("FAST_MODE", None)
if _fast_mode:
    FAST_MODE = str_to_bool(_fast_mode)

# Prometheus metrics settings (optional)
# Prometheus exporter listen port (None to disable)
_metrics_port = os.environ.get("METRICS_PORT", None)
if _metrics_port:
    METRICS_PORT = int(_metrics_port)

# Export proxy links in metrics
_metrics_export_links = os.environ.get("METRICS_EXPORT_LINKS", None)
if _metrics_export_links:
    METRICS_EXPORT_LINKS = str_to_bool(_metrics_export_links)
