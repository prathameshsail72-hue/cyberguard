#!/usr/bin/env python3
"""
CYBERGUARD 3.0 Pro - Unified Desktop Application Launcher
Modern Glassmorphism Cybersecurity Operations & Threat Intelligence Suite in PyQt6.
"""

import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import main as launch_app

if __name__ == "__main__":
    launch_app()
