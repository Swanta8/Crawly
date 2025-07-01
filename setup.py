#!/usr/bin/env python3
"""
Setup script for SiteTester GUI Application
Automatically creates virtual environment and installs dependencies
"""

import subprocess
import sys
import os
import venv
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, shell=True)
        print(f"✅ {description} completed")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        sys.exit(1)


def main():
    """Main setup function"""
    print("🚀 Setting up SiteTester GUI Application...")
    
    project_root = Path(__file__).parent
    venv_dir = project_root / "venv"
    
    # Create virtual environment if it doesn't exist
    if not venv_dir.exists():
        print("📦 Creating virtual environment...")
        venv.create(venv_dir, with_pip=True)
        print("✅ Virtual environment created")
    else:
        print("ℹ️  Virtual environment already exists")
    
    # Determine paths based on OS
    if sys.platform == "win32":
        python_path = venv_dir / "Scripts" / "python"
        pip_path = venv_dir / "Scripts" / "pip"
    else:
        python_path = venv_dir / "bin" / "python"
        pip_path = venv_dir / "bin" / "pip"
    
    # Upgrade pip
    run_command(f'"{pip_path}" install --upgrade pip', "Upgrading pip")
    
    # Install requirements
    if (project_root / "requirements.txt").exists():
        run_command(f'"{pip_path}" install -r requirements.txt', "Installing requirements")
    else:
        print("⚠️  No requirements.txt found, installing basic packages...")
        packages = ["playwright>=1.40.0", "rich>=13.0.0", "pyinstaller>=6.0.0"]
        for package in packages:
            run_command(f'"{pip_path}" install "{package}"', f"Installing {package}")
    
    # Install Playwright browsers
    run_command(f'"{python_path}" -m playwright install', "Installing Playwright browsers")
    
    # Create logs directory
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    print("📁 Logs directory created")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📖 Next steps:")
    print("1. Run the application: python main.py")
    print("2. Or build standalone app: python build.py")
    print(f"3. Scripts directory: {project_root / 'scripts'}")
    print(f"4. Logs will be saved to: {logs_dir}")


if __name__ == "__main__":
    main() 