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
      # Replace these values with your own configuration
      - TG_KEY=00000000000000000000000000000001
      - SECURE_ONLY=true
      - TLS_ONLY=true
      - TLS_DOMAIN=www.drive.google.com
      - AD_TAG=3c09c680b76ee91a4c25ad51f742267d
    volumes:
        - ./config.py:/home/tgproxy/config.py
```

Then run: `docker-compose up -d`

## Channel Advertising ##

To advertise a channel get a tag from **@MTProxybot** and put it to *config.py*.

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

**Note:** SOCKS5 mode is incompatible with middle proxy advertising and uvloop.

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
- uvloop acceleration is not available
- Channel advertising may not work
