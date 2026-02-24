#!/usr/bin/env python3
"""
Setup script for google-search skill.

Installs the required brightdata-sdk package and creates config template.
"""

import json
import subprocess
import sys
from pathlib import Path


CONFIG_DIR = Path.home() / ".claude" / "google-search"
CONFIG_FILE = CONFIG_DIR / "config.json"
CONFIG_TEMPLATE = {
    "api_key": "",
    "note": "Add your Bright Data SERP API key here"
}


def create_config():
    """Create config directory and config.json template if not exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w") as f:
            json.dump(CONFIG_TEMPLATE, f, indent=2)
        print(f"Created config file: {CONFIG_FILE}")
        print("Please edit this file and add your Bright Data SERP API key.")
        return True
    else:
        print(f"Config file already exists: {CONFIG_FILE}")
        return False


def install_sdk():
    """Install brightdata-sdk if not already installed."""
    try:
        import brightdata
        print("brightdata-sdk is already installed.")
        return True
    except ImportError:
        pass

    print("Installing brightdata-sdk...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "brightdata-sdk"])
        print("brightdata-sdk installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install brightdata-sdk: {e}", file=sys.stderr)
        return False


def main():
    """Run setup."""
    created_config = create_config()
    installed_sdk = install_sdk()

    if installed_sdk and created_config:
        print("\n✅ Setup complete!")
        print(f"Next step: Edit {CONFIG_FILE} and add your API key.")
    elif installed_sdk:
        print("\n✅ Setup complete!")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
