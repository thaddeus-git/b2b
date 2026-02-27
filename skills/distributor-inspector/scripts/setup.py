#!/usr/bin/env python3
"""
Setup script for distributor-inspector skill.

Installs the required brightdata-sdk package and creates config template.
"""

import json
import subprocess
import sys
from pathlib import Path


CONFIG_DIR = Path.home() / ".claude" / "distributor-inspector"
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
        print("\n" + "=" * 60)
        print("Setup complete!")
        print("=" * 60)
        print(f"\nNext step: Add your Bright Data API key to:")
        print(f"  {CONFIG_FILE}")
        print("\nHow to get your API key:")
        print("  1. Go to https://brightdata.com/cp/api_tokens")
        print("  2. Log in or create a free account")
        print("  3. Copy your API token")
        print("  4. Paste it in the config file as 'api_key' value")
        print("\nVerify with: python3 scripts/search.py 'test' 'US' 'en' '5'")
    elif installed_sdk:
        print("\n" + "=" * 60)
        print("Setup complete!")
        print("=" * 60)
        if CONFIG_FILE.exists():
            print(f"\nConfig file: {CONFIG_FILE}")
            print("Make sure your API key is configured.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
