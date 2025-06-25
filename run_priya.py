#!/usr/bin/env python3
"""
Run Priya AI Girlfriend Chat System
Simple startup script for the integrated system
"""

import os
import sys
import subprocess
import asyncio
from pathlib import Path
from dotenv import load_dotenv

def print_header():
    print("💖" * 30)
    print("🌟 Priya AI Girlfriend - Integrated System 🌟")
    print("💖" * 30)
    print("🚀 Powered by Letta | Integrated with Niya")
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
        print("⚠️ LETTA_TOKEN not found - will try local Letta server")
    else:
        print("✅ Letta token found")
    
    # Check Docker (optional)
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker is available")
        else:
            print("⚠️ Docker not found - cloud mode only")
    except FileNotFoundError:
        print("⚠️ Docker not found - cloud mode only")
    
    print("✅ Requirements check completed")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing/Updating Dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("🔧 Try running: pip install -r requirements.txt")
        return False

async def start_priya():
    """Start the Priya chat system"""
    try:
        print("🎉 Starting Priya AI Girlfriend...")
        print("📱 Open http://localhost:8000 in your browser")
        print("🔌 WebSocket available at ws://localhost:8000/ws")
        print("🛑 Press Ctrl+C to stop")
        print()
        
        # Import and run the chat system
        from priya_chat import main as priya_main
        await priya_main()
        
    except KeyboardInterrupt:
        print("\n💕 Priya says goodbye! Take care jaan! ✨")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Make sure all dependencies are installed")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting Priya: {e}")
        sys.exit(1)

def main():
    """Main entry point"""
    try:
        print_header()
        
        if not check_requirements():
            sys.exit(1)
        
        # Option to install dependencies
        if '--install' in sys.argv or '--setup' in sys.argv:
            if not install_dependencies():
                sys.exit(1)
        
        print("🚀 Launching Priya Chat System...")
        print()
        
        # Start the async system
        asyncio.run(start_priya())
        
    except KeyboardInterrupt:
        print("\n💕 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 