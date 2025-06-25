#!/usr/bin/env python3
"""
Real-time Message Monitor
Shows live activity from your Niya frontend users
"""

import requests
import time
import json
from datetime import datetime

def check_bridge_status():
    """Check if bridge is receiving messages"""
    try:
        response = requests.get('http://localhost:1511/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Bridge Status: {data['status']}")
            print(f"🤖 Agent ID: {data['agent_id']}")
            print(f"🔗 Letta Connected: {data['letta_connected']}")
            return True
    except Exception as e:
        print(f"❌ Bridge not responding: {e}")
        return False

def send_test_ping():
    """Send a test message to check activity"""
    try:
        test_message = f"Ping test at {datetime.now().strftime('%H:%M:%S')}"
        response = requests.post(
            'http://localhost:1511/message',
            json={'message': test_message},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"📨 Test Response: {data['response'][:50]}...")
                return True
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def monitor_activity():
    """Monitor for real-time activity"""
    print("🔍 NIYA FRONTEND MESSAGE MONITOR")
    print("=" * 50)
    print("👀 Watching for messages from your frontend users...")
    print("🔄 Sending periodic pings to check activity...")
    print("🛑 Press Ctrl+C to stop monitoring")
    print()
    
    last_check = time.time()
    ping_interval = 30  # Send ping every 30 seconds
    
    while True:
        try:
            current_time = time.time()
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Check bridge status
            if not check_bridge_status():
                print(f"⚠️  [{timestamp}] Bridge service appears to be down!")
                time.sleep(5)
                continue
            
            # Send periodic ping
            if current_time - last_check > ping_interval:
                print(f"📡 [{timestamp}] Sending ping to check activity...")
                if send_test_ping():
                    print(f"✅ [{timestamp}] Bridge is responding normally")
                else:
                    print(f"❌ [{timestamp}] Bridge ping failed")
                last_check = current_time
            
            print(f"⏰ [{timestamp}] Monitoring... (waiting for frontend messages)")
            
            # Show instructions
            if current_time % 60 < 5:  # Every minute
                print("💡 To see frontend messages:")
                print("   1. Start your Niya backend: npm run start:dev")
                print("   2. Start your frontend: npm run dev") 
                print("   3. Users chat normally - messages will appear here!")
                print()
            
            time.sleep(5)
            
        except KeyboardInterrupt:
            print(f"\n🛑 [{datetime.now().strftime('%H:%M:%S')}] Monitoring stopped")
            break
        except Exception as e:
            print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] Monitor error: {e}")
            time.sleep(5)

def show_current_status():
    """Show current system status"""
    print("📊 CURRENT SYSTEM STATUS")
    print("=" * 30)
    
    # Check bridge
    print("🌉 Python Bridge (Port 1511):")
    if check_bridge_status():
        print("   ✅ Running and healthy")
    else:
        print("   ❌ Not responding")
    
    # Check if backend might be running
    try:
        response = requests.get('http://localhost:3002/health', timeout=2)
        print("🏢 Niya Backend (Port 3002):")
        print("   ✅ Appears to be running")
    except:
        print("🏢 Niya Backend (Port 3002):")
        print("   ❌ Not detected (start with: npm run start:dev)")
    
    # Check if frontend might be running  
    try:
        response = requests.get('http://localhost:5173/', timeout=2)
        print("🌐 Frontend (Port 5173):")
        print("   ✅ Appears to be running")
    except:
        print("🌐 Frontend (Port 5173):")
        print("   ❌ Not detected (start with: npm run dev)")
    
    print()

if __name__ == "__main__":
    try:
        show_current_status()
        print()
        monitor_activity()
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped by user")
    except Exception as e:
        print(f"❌ Monitor failed: {e}") 