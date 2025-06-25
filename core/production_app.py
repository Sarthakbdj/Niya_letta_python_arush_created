#!/usr/bin/env python3
"""
Production WSGI Application for Niya Bridge
Optimized for Gunicorn deployment
"""

import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from niya_bridge_ultra_fast import bridge

# WSGI Application
application = bridge.flask_app

# Production initialization
if __name__ != "__main__":
    # Initialize bridge when loaded by WSGI server
    bridge.initialize()
