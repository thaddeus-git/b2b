#!/usr/bin/env python3
"""
Setup script for lead-enricher skill.

Installs required packages and creates config template.
"""

import json
import subprocess
import sys
from pathlib import Path


CONFIG_DIR = Path.home() / ".claude" / "lead-enricher"
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


def install_dependencies():
    """Install required packages if not already installed."""
    packages = ["brightdata-sdk", "pandas", "thefuzz"]

    for package in packages:
        try:
            if package == "thefuzz":
                __import__("thefuzz")
            else:
                __import__(package.replace("-", "_"))
            print(f"{package} is already installed.")
        except ImportError:
            print(f"Installing {package}...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"{package} installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install {package}: {e}", file=sys.stderr)
                return False
    return True


def main():
    """Run setup."""
    created_config = create_config()
    installed = install_dependencies()

    if installed and created_config:
        print("\n" + "=" * 60)
        print("Setup complete!")
        print("=" * 60)
        print(f"\nNext step: Add your Bright Data API key to:")
        print(f"  {CONFIG_FILE}")
        print("\nVerify with: python3 scripts/enrich.py --test")
    elif installed:
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
