#!/usr/bin/env python3
"""
Options Pricer Launcher
Checks dependencies and launches the GUI application
"""

import sys
import subprocess
import importlib

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = ['numpy', 'scipy', 'matplotlib']
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:", missing_packages)
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("Options Pricer - Black-Scholes Model")
    print("=" * 40)
    
    if not check_dependencies():
        sys.exit(1)
    
    try:
        from gui import main as gui_main
        print("Launching GUI application...")
        gui_main()
    except ImportError as e:
        print(f"Error importing GUI module: {e}")
        print("Make sure gui.py is in the same directory")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 