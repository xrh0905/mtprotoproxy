# Async MTProto Proxy #

[![Docker Image](https://img.shields.io/badge/docker-ghcr.io-blue)](https://github.com/xrh0905/mtprotoproxy/pkgs/container/mtprotoproxy)

Fast and simple to setup MTProto proxy written in Python.

## Starting Up ##

### Using Pre-built Docker Image (Recommended) ###

1. Pull the latest image: `docker pull ghcr.io/xrh0905/mtprotoproxy:latest`
2. *(optional, recommended)* create a *config.py* file, set **PORT**, **USERS** and **AD_TAG**
3. Run the container:
   ```bash
   docker run -d --name mtprotoproxy \
     --network host \
     -v $(pwd)/config.py:/home/tgproxy/config.py \
     ghcr.io/xrh0905/mtprotoproxy:latest
   ```
4. *(optional, get a link to share the proxy)* `docker logs mtprotoproxy`

### Building from Source ###
    
1. `git clone -b edge https://github.com/xrh0905/mtprotoproxy.git; cd mtprotoproxy`
2. *(optional, recommended)* edit *config.py*, set **PORT**, **USERS** and **AD_TAG**
3. `docker build -t mtprotoproxy .`
4. `docker-compose up -d` (or just `python3 mtprotoproxy.py` if you don't like Docker)
5. *(optional, get a link to share the proxy)* `docker-compose logs`

![Demo](https://alexbers.com/mtprotoproxy/install_demo_v2.gif)

## Using with Docker Compose ##

You can use the pre-built image with docker-compose by updating your `docker-compose.yml`:

```yaml
version: '3.8'
services:
  mtprotoproxy:
    image: ghcr.io/xrh0905/mtprotoproxy:latest
    restart: unless-stopped
    network_mode: "host"
    environment: 
      # Core configuration - replace these values with your own
      - PORT=443
      - TG_KEY=00000000000000000000000000000001
      - SECURE_ONLY=true
      - TLS_ONLY=true
      - TLS_DOMAIN=www.drive.google.com
      - AD_TAG=3c09c680b76ee91a4c25ad51f742267d
      # Optional: Performance tuning
      # - TO_CLT_BUFSIZE=65536
      # - TO_TG_BUFSIZE=65536
      # Optional: Metrics
      # - METRICS_PORT=9090
    volumes:
        - ./config.py:/home/tgproxy/config.py
```

Then run: `docker-compose up -d`

## Channel Advertising ##

To advertise a channel get a tag from **@MTProxybot** and put it to *config.py*.

## Environment Variables ##

All configuration options can be set via environment variables. This is particularly useful when running in Docker.

### Required/Core Configuration ###

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `443` | Listening port for the proxy |
| `TG_KEY` | `00000000000000000000000000000001` | User secret (32 hex characters) |
| `AD_TAG` | `3c09c680b76ee91a4c25ad51f742267d` | Tag for advertising, obtainable from @MTProxybot |

### Security Settings ###

| Variable | Default | Description |
|----------|---------|-------------|
| `SECURE_ONLY` | `true` | Makes the proxy harder to detect (incompatible with very old clients) |
| `TLS_ONLY` | `true` | Makes the proxy even harder to detect (compatible only with recent clients) |
| `TLS_DOMAIN` | `www.google.com` | Domain for TLS, bad clients are proxied there |

### SOCKS5 Proxy Settings (Optional) ###

| Variable | Default | Description |
|----------|---------|-------------|
| `SOCKS5_HOST` | `None` | SOCKS5 proxy hostname or IP address |
| `SOCKS5_PORT` | `None` | SOCKS5 proxy port |
| `SOCKS5_USER` | `None` | SOCKS5 username (optional) |
| `SOCKS5_PASS` | `None` | SOCKS5 password (optional) |

**Note:** When SOCKS5 is enabled, middle proxy advertising is automatically disabled.

### Performance Tuning (Optional) ###

| Variable | Default | Description |
|----------|---------|-------------|
| `TO_CLT_BUFSIZE` | `16384,100,131072` | Buffer size to client. Single integer or comma-separated tuple (low,users_margin,high) for adaptive sizing |
| `TO_TG_BUFSIZE` | `65536` | Buffer size to Telegram servers. Single integer or comma-separated tuple for adaptive sizing |
| `STATS_PRINT_PERIOD` | `600` | Statistics print period in seconds |
| `CLIENT_KEEPALIVE` | `600` | Client keepalive period in seconds (10 minutes) |
| `TG_CONNECT_TIMEOUT` | `10` | Telegram server connect timeout in seconds |
| `FAST_MODE` | `true` | Enable fast mode (disables some checks for better performance) |

### Network Settings (Optional) ###

| Variable | Default | Description |
|----------|---------|-------------|
| `LISTEN_ADDR_IPV4` | `0.0.0.0` | IPv4 listen address |
| `LISTEN_ADDR_IPV6` | `::` | IPv6 listen address |
| `PREFER_IPV6` | Auto-detected | Prefer IPv6 for outgoing connections |

### Prometheus Metrics (Optional) ###

| Variable | Default | Description |
|----------|---------|-------------|
| `METRICS_PORT` | `None` | Prometheus exporter listen port (set to enable metrics) |
| `METRICS_EXPORT_LINKS` | `false` | Export proxy links in metrics |

### Example with Environment Variables ###

```bash
docker run -d --name mtprotoproxy \
  --network host \
  -e PORT=8443 \
  -e TG_KEY=00000000000000000000000000000001 \
  -e SECURE_ONLY=true \
  -e TLS_ONLY=true \
  -e TLS_DOMAIN=www.google.com \
  -e AD_TAG=3c09c680b76ee91a4c25ad51f742267d \
  -e TO_CLT_BUFSIZE=65536 \
  -e TO_TG_BUFSIZE=65536 \
  -e METRICS_PORT=9090 \
  ghcr.io/xrh0905/mtprotoproxy:latest
```

## Performance ##

The proxy performance should be enough to comfortably serve about 4 000 simultaneous users on
the VDS instance with 1 CPU core and 1024MB RAM.

## More Instructions ##

- [Running without Docker](https://github.com/alexbers/mtprotoproxy/wiki/Running-Without-Docker)
- [Optimization and fine tuning](https://github.com/alexbers/mtprotoproxy/wiki/Optimization-and-Fine-Tuning)

## Advanced Usage ##

The proxy can be launched:
- with a custom config: `python3 mtprotoproxy.py [configfile]`
- several times, clients will be automaticaly balanced between instances
- with uvloop module to get an extra speed boost
- with runtime statistics exported to [Prometheus](https://prometheus.io/)

### Using SOCKS5 as Outgoing Proxy ###

You can configure the MTProto proxy to use a SOCKS5 proxy for outgoing connections to Telegram servers. This is useful when your server cannot directly connect to Telegram or you want to route traffic through another proxy.

**Note:** SOCKS5 mode is incompatible with middle proxy advertising.

#### Configuration in config.py ####

Add the following settings to your `config.py`:

```python
# SOCKS5 proxy settings (optional)
SOCKS5_HOST = "your.socks5.server.com"  # SOCKS5 proxy hostname or IP
SOCKS5_PORT = 1080                       # SOCKS5 proxy port
SOCKS5_USER = "username"                 # Optional: SOCKS5 username (set to None if not needed)
SOCKS5_PASS = "password"                 # Optional: SOCKS5 password (set to None if not needed)
```

#### Using Environment Variables ####

You can also configure SOCKS5 using environment variables:

```bash
docker run -d --name mtprotoproxy \
  --network host \
  -e SOCKS5_HOST=your.socks5.server.com \
  -e SOCKS5_PORT=1080 \
  -e SOCKS5_USER=username \
  -e SOCKS5_PASS=password \
  -v $(pwd)/config.py:/home/tgproxy/config.py \
  ghcr.io/xrh0905/mtprotoproxy:latest
```

#### Docker Compose Example with SOCKS5 ####

```yaml
version: '3.8'
services:
  mtprotoproxy:
    image: ghcr.io/xrh0905/mtprotoproxy:latest
    restart: unless-stopped
    network_mode: "host"
    environment: 
      - TG_KEY=00000000000000000000000000000001
      - SECURE_ONLY=true
      - TLS_ONLY=true
      - TLS_DOMAIN=www.drive.google.com
      # SOCKS5 proxy configuration
      - SOCKS5_HOST=your.socks5.server.com
      - SOCKS5_PORT=1080
      - SOCKS5_USER=username
      - SOCKS5_PASS=password
    volumes:
        - ./config.py:/home/tgproxy/config.py
```

**Important:** When SOCKS5 is enabled:
- The middle proxy feature is automatically disabled
- Channel advertising may not work
