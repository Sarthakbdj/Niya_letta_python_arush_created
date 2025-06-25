#!/usr/bin/env python3
"""
Main Niya-Python Launcher - BRIDGE SERVICE ONLY
Optimized entry point for Niya Frontend → Backend → Python Bridge integration
"""

import sys
import os
import subprocess
from pathlib import Path

def print_header():
    print("🌉" * 40)
    print("🌟 NIYA-PYTHON BRIDGE SYSTEM 🌟")
    print("⚡ SPEED OPTIMIZED FOR <7s RESPONSES")
    print("🌉" * 40)
    print("🔗 AI Girlfriend Integration (Bridge Only)")
    print("💕 Frontend → Backend → Python Bridge → Priya AI")
    print()

def print_usage():
    print("📋 USAGE:")
    print("  python run_niya.py                    # Start bridge service (default)")
    print("  python run_niya.py --bridge          # Start bridge service only")
    print("  python run_niya.py --test            # Test integration flow")
    print("  python run_niya.py --monitor         # Monitor activity")
    print("  python run_niya.py --help            # Show this help")
    print()

def print_system_info():
    print("🏗️ SYSTEM ARCHITECTURE:")
    print("   Frontend (React/Vue) → Niya Backend (NestJS:3002) → Python Bridge (Flask:1511)")
    print()
    print("🔧 CORE FILES:")
    print("   📁 core/niya_bridge.py           - Main bridge service (SPEED OPTIMIZED + MULTI-MESSAGE)")
    print("   📁 core/enhanced_personality.py  - AI personality configuration")
    print("   📁 testing/test_frontend_flow.py - Integration testing")
    print()
    print("⚙️ CONFIGURATION:")
    print("   🌐 Cloud Mode: Set LETTA_TOKEN in .env for Letta Cloud (RECOMMENDED)")
    print("   🏠 Local Mode: Set LETTA_BASE_URL for local Letta server")
    print("   🎯 Target: 95%+ responses under 7 seconds")
    print()
    print("⚡ SPEED OPTIMIZATIONS:")
    print("   • Request spacing: 0.3s (85% faster)")
    print("   • Memory blocks: 2 (reduced from 6)")
    print("   • No embedding processing")
    print("   • Single attempt (no retry delays)")
    print("   • Minimal logging")
    print("   • Auto agent cleanup on startup")
    print()
    print("📱 MULTI-MESSAGE FEATURES:")
    print("   • Natural message breaking (Flask side)")
    print("   • WhatsApp-style responses")
    print("   • No pressure on Letta API")
    print("   • Backend compatible format")
    print()

def run_bridge():
    """Run the main bridge service - SPEED OPTIMIZED + MULTI-MESSAGE"""
    print("🌉 Starting SPEED-OPTIMIZED Niya Bridge Service (Port 1511)...")
    print("🔗 This connects your Niya Backend to Enhanced Priya AI")
    print("⚡ Optimized for 95%+ responses under 7 seconds")
    print("📱 Multi-message support with no Letta API pressure")
    print()
    
    try:
        # Set PYTHONPATH to include current directory for imports
        env = os.environ.copy()
        env['PYTHONPATH'] = str(Path.cwd())
        subprocess.run([sys.executable, 'core/niya_bridge.py'], check=True, env=env)
    except Exception as e:
        print(f"❌ Bridge service error: {e}")

def run_test():
    """Run integration tests"""
    print("🧪 Running Integration Tests...")
    print("🔗 Testing: Frontend → Backend → Python Bridge Flow")
    print()
    
    try:
        sys.path.insert(0, str(Path.cwd()))
        subprocess.run([sys.executable, 'testing/test_frontend_flow.py'], check=True)
    except Exception as e:
        print(f"❌ Test error: {e}")

def run_monitor():
    """Run activity monitor"""
    print("👀 Starting Activity Monitor...")
    print("🔍 Watching for messages from Niya Frontend users")
    print()
    
    try:
        sys.path.insert(0, str(Path.cwd()))
        subprocess.run([sys.executable, 'testing/monitor_messages.py'], check=True)
    except Exception as e:
        print(f"❌ Monitor error: {e}")

def main():
    """Main entry point - BRIDGE ONLY"""
    print_header()
    
    # Parse command line arguments
    if len(sys.argv) == 1 or '--bridge' in sys.argv:
        print_system_info()
        run_bridge()
    elif '--test' in sys.argv:
        run_test()
    elif '--monitor' in sys.argv:
        run_monitor()
    elif '--help' in sys.argv or '-h' in sys.argv:
        print_system_info()
        print_usage()
    else:
        print("❌ Unknown option. Use --help for usage information.")
        print("💡 This version only supports bridge service (no chat interface)")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n💕 Niya-Python shutting down gracefully...")
        print("👋 Thanks for using the speed-optimized AI girlfriend system!") 