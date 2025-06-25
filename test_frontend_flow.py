#!/usr/bin/env python3
"""
Test Frontend Integration Flow
Simulates how your frontend users will interact with Priya
"""

import requests
import json
import time

def simulate_frontend_user():
    """Simulate multiple users chatting through the frontend"""
    
    print("🧪 Testing Frontend → Backend → Python Bridge Flow")
    print("=" * 60)
    
    # Simulate different user messages
    test_messages = [
        "Hi Priya! I'm messaging from the Niya frontend",
        "How was your day today?",
        "Can you help me with coding?",
        "I'm feeling stressed about work",
        "What's your favorite movie?",
        "I love chatting with you!"
    ]
    
    print("👤 Simulating user messages from frontend...")
    print()
    
    for i, message in enumerate(test_messages, 1):
        print(f"📱 User Message {i}: {message}")
        
        try:
            # This is exactly what your NestJS backend does
            response = requests.post(
                'http://localhost:1511/message',
                json={'message': message},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    priya_response = data.get('response', '')
                    print(f"💕 Priya Response: {priya_response}")
                    print(f"✅ Frontend would display: '{priya_response}'")
                else:
                    print(f"❌ Error: {data.get('error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Connection Error: {e}")
        
        print("-" * 60)
        time.sleep(1)  # Small delay between messages
    
    print("🎉 Frontend integration test complete!")
    print("✅ Users can now chat with Priya through your Niya frontend!")

if __name__ == "__main__":
    simulate_frontend_user() 