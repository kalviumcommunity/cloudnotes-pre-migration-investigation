#!/usr/bin/env python3
"""Standalone health probe helper for the CloudNotes service.

This utility performs an HTTP GET against the running service's /health
endpoint and reports the result. It reads the target port from the
application configuration referenced by APP_CONFIG when available.
"""

import os
import sys
import json
import urllib.request
import urllib.error


def read_port_from_config():
    config_path = os.environ.get("APP_CONFIG")
    if not config_path or not os.path.exists(config_path):
        return None
    with open(config_path) as handle:
        for line in handle:
            line = line.strip()
            if line.startswith("PORT="):
                return line.split("=", 1)[1].strip()
    return None


def main():
    port = read_port_from_config() or "8080"
    url = f"http://localhost:{port}/health"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            payload = response.read().decode()
            data = json.loads(payload)
            print(json.dumps(data))
            if data.get("status") == "healthy":
                sys.exit(0)
            sys.exit(1)
    except (urllib.error.URLError, OSError) as exc:
        print(f"health check failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
