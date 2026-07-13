#!/usr/bin/env python3
"""CloudNotes service entry point.

Reads configuration from the APP_CONFIG environment variable, logs its
startup activity to logs/service.log, loads the referenced configuration
file and starts a simple HTTP server exposing a /health endpoint.
"""

import os
import sys
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "service.log")


def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def load_config(path):
    """Parse a simple KEY=VALUE configuration file."""
    config = {}
    with open(path) as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()
    return config


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = b'{"status":"healthy"}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        logging.info("request %s", self.path)


def main():
    setup_logging()

    config_path = os.environ.get("APP_CONFIG")
    if not config_path:
        logging.error('required environment variable "APP_CONFIG" is not set')
        logging.critical("cannot locate configuration, shutting down")
        print(
            'ERROR required environment variable "APP_CONFIG" is not set',
            file=sys.stderr,
        )
        print("FATAL cannot locate configuration, shutting down", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(config_path):
        logging.error("configuration file not found: %s", config_path)
        logging.critical("cannot locate configuration, shutting down")
        print(f"ERROR configuration file not found: {config_path}", file=sys.stderr)
        print("FATAL cannot locate configuration, shutting down", file=sys.stderr)
        sys.exit(1)

    config = load_config(config_path)
    logging.info("loaded configuration from %s", config_path)

    host = config.get("HOST", "0.0.0.0")
    port = int(config.get("PORT", "8080"))

    logging.info("starting CloudNotes service on %s:%s", host, port)
    server = ThreadingHTTPServer((host, port), HealthHandler)
    print(f"CloudNotes service listening on {host}:{port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("shutdown requested, stopping service")
        server.shutdown()


if __name__ == "__main__":
    main()
