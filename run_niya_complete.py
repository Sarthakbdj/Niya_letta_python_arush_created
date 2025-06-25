#!/usr/bin/env python3
"""
Complete Niya-Python Launch Script
Runs both the Niya Backend Integration (port 1511) and Priya Chat Interface (port 8000)
"""

import os
import sys
import time
import threading
import subprocess
import asyncio
from pathlib import Path
from dotenv import load_dotenv

def print_header():
    print("🚀" * 40)
    print("🌟 COMPLETE NIYA-PYTHON LAUNCH SYSTEM 🌟")
    print("🚀" * 40)
    print("🔗 Bridge Service (Port 1511) + Chat Interface (Port 8000)")
    print("💕 Priya AI Girlfriend - Full Integration")
    print()

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking system requirements...")
    
    # Load environment
    load_dotenv()
    
    # Check OpenAI API key
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key:
        print("❌ OPENAI_API_KEY not found!")
        print("📝 Please add your OpenAI API key to .env file")
        return False
    else:
        print("✅ OpenAI API key found")
    
    # Check Letta token
    letta_token = os.getenv('LETTA_TOKEN')
    if not letta_token:
        print("❌ LETTA_TOKEN not found!")
        print("📝 Please add your Letta token to .env file")
        return False
    else:
        print("✅ Letta token found")
    
    # Check required packages
    try:
        import flask
        import flask_cors
        import letta_client
        import fastapi
        import uvicorn
        import websockets
        print("✅ All required packages available")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("🔧 Run: pip install -r requirements.txt")
        return False
    
    print("✅ All requirements satisfied")
    return True

def run_bridge_service():
    """Run the Niya Bridge Service on port 1511"""
    try:
        print("🌉 Starting Niya Bridge Service...")
        subprocess.run([sys.executable, 'niya_bridge.py'], check=True)
    except Exception as e:
        print(f"❌ Bridge service error: {e}")

def run_chat_interface():
    """Run the Priya Chat Interface on port 8000"""
    try:
        print("💕 Starting Priya Chat Interface...")
        subprocess.run([sys.executable, 'priya_chat.py'], check=True)
    except Exception as e:
        print(f"❌ Chat interface error: {e}")

def run_services_parallel():
    """Run both services in parallel using threading"""
    print("🚀 Launching both services in parallel...")
    print()
    
    # Create threads for both services
    bridge_thread = threading.Thread(target=run_bridge_service, daemon=True)
    chat_thread = threading.Thread(target=run_chat_interface, daemon=True)
    
    # Start both services
    bridge_thread.start()
    print("✅ Bridge service thread started")
    
    time.sleep(2)  # Small delay between starts
    
    chat_thread.start()
    print("✅ Chat interface thread started")
    
    print()
    print("🎉 Both services are starting up...")
    print("⏳ Please wait a moment for initialization...")
    print()
    
    # Wait a bit for services to start
    time.sleep(5)
    
    print("🔗 Services should now be running:")
    print("   📡 Niya Bridge: http://localhost:1511")
    print("   💕 Priya Chat: http://localhost:8000")
    print()
    print("🛑 Press Ctrl+C to stop both services")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        print("💕 Thanks for using Niya-Python!")

def test_services():
    """Test if services are responding"""
    import requests
    import json
    
    print("🧪 Testing services...")
    
    # Test bridge service
    try:
        response = requests.get('http://localhost:1511/health', timeout=5)
        if response.status_code == 200:
            print("✅ Bridge service is responding")
        else:
            print("⚠️ Bridge service responded with error")
    except Exception as e:
        print(f"❌ Bridge service not responding: {e}")
    
    # Test bridge message endpoint
    try:
        test_message = {"message": "Hello, this is a test!"}
        response = requests.post('http://localhost:1511/message', 
                               json=test_message, 
                               timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Bridge message endpoint working")
                print(f"   Response: {data.get('response', '')[:50]}...")
            else:
                print("⚠️ Bridge returned error:", data.get('error'))
        else:
            print("❌ Bridge message endpoint failed")
    except Exception as e:
        print(f"❌ Bridge message test failed: {e}")
    
    # Test chat interface
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        if response.status_code == 200:
            print("✅ Chat interface is responding")
        else:
            print("⚠️ Chat interface responded with error")
    except Exception as e:
        print(f"❌ Chat interface not responding: {e}")

def show_integration_info():
    """Show integration information"""
    print("📋 INTEGRATION INFORMATION")
    print("=" * 50)
    print()
    print("🔗 Niya Backend Integration:")
    print("   Expected URL: http://localhost:1511")
    print("   Main Endpoint: POST /message")
    print("   Request Format: {'message': 'user message'}")
    print("   Response Format: {'success': bool, 'response': str, 'error': str}")
    print()
    print("💕 Priya Chat Interface:")
    print("   Web Interface: http://localhost:8000")
    print("   WebSocket: ws://localhost:8000/ws")
    print("   API Docs: http://localhost:8000/docs")
    print()
    print("🏗️ Architecture:")
    print("   Frontend ←→ Niya Backend (port 3002) ←→ Python Bridge (port 1511)")
    print("   Users can also chat directly at: http://localhost:8000")
    print()

def main():
    """Main entry point"""
    try:
        print_header()
        
        if not check_requirements():
            print("\n❌ Requirements not met. Please fix the issues above.")
            sys.exit(1)
        
        print()
        show_integration_info()
        
        # Check for command line arguments
        if '--test' in sys.argv:
            print("🧪 Running in test mode...")
            time.sleep(2)
            test_services()
            return
        
        if '--bridge-only' in sys.argv:
            print("🌉 Running bridge service only...")
            run_bridge_service()
            return
        
        if '--chat-only' in sys.argv:
            print("💕 Running chat interface only...")
            run_chat_interface()
            return
        
        # Default: run both services
        print("🚀 Starting complete Niya-Python system...")
        print("   This will start both services simultaneously")
        print()
        
        run_services_parallel()
        
    except KeyboardInterrupt:
        print("\n💕 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 