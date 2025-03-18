#!/usr/bin/env python3
"""
Launcher script for the Mental Health Pattern Recognition Assistant GUI.

This script provides a simple way to launch the GUI application from the project root.
"""

import os
import sys
import subprocess

def main():
    """Launch the GUI application."""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the GUI application
    app_path = os.path.join(script_dir, "ui", "app.py")
    
    # Check if the app file exists
    if not os.path.exists(app_path):
        print(f"Error: Could not find the application at {app_path}")
        return 1
    
    # Launch the application
    print("Launching Mental Health Pattern Recognition Assistant GUI...")
    try:
        # Use the same Python interpreter that's running this script
        python_executable = sys.executable
        subprocess.run([python_executable, app_path], check=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to launch the application: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        return 0

if __name__ == "__main__":
    sys.exit(main())
