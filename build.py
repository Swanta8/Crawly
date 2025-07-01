#!/usr/bin/env python3
"""
Build script for SiteTester GUI Application
Creates a standalone executable using PyInstaller
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path


def main():
    """Main build function"""
    print("🔨 Building SiteTester GUI Application...")
    
    # Get current directory
    project_root = Path(__file__).parent
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"
    
    # Clean previous builds
    if dist_dir.exists():
        print("🧹 Cleaning previous builds...")
        shutil.rmtree(dist_dir)
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    # PyInstaller command for macOS
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window (GUI app)
        "--name", "SiteTesterApp",      # App name
        "--icon", "icon.icns",          # Icon (if available)
        "--add-data", "scripts:scripts", # Include scripts directory
        "--hidden-import", "playwright",
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.ttk",
        "--hidden-import", "tkinter.scrolledtext",
        "--clean",                      # Clean PyInstaller cache
        "main.py"
    ]
    
    # Remove icon parameter if icon file doesn't exist
    if not (project_root / "icon.icns").exists():
        cmd = [arg for arg in cmd if arg != "--icon" and arg != "icon.icns"]
    
    try:
        print("🚀 Running PyInstaller...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✅ Build completed successfully!")
        print(f"📦 Executable created at: {dist_dir / 'SiteTesterApp'}")
        
        # Show build statistics
        if (dist_dir / "SiteTesterApp").exists():
            size = (dist_dir / "SiteTesterApp").stat().st_size
            size_mb = size / (1024 * 1024)
            print(f"📊 File size: {size_mb:.1f} MB")
        
    except subprocess.CalledProcessError as e:
        print("❌ Build failed!")
        print(f"Error: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        sys.exit(1)
    
    except FileNotFoundError:
        print("❌ PyInstaller not found!")
        print("Please install PyInstaller: pip install pyinstaller")
        sys.exit(1)


if __name__ == "__main__":
    main() 