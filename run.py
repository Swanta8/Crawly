#!/usr/bin/env python3
"""
Quick run script for SiteTester GUI Application
Automatically checks environment and starts the application
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Main run function"""
    project_root = Path(__file__).parent
    venv_dir = project_root / "venv"
    
    # Check if virtual environment exists
    if not venv_dir.exists():
        print("🔧 Virtual environment not found. Running setup...")
        try:
            subprocess.run([sys.executable, "setup.py"], check=True)
        except subprocess.CalledProcessError:
            print("❌ Setup failed. Please run setup.py manually.")
            sys.exit(1)
    
    # Run the main application
    print("🚀 Starting SiteTester GUI...")
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")


if __name__ == "__main__":
    main() 