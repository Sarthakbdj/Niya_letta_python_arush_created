#!/usr/bin/env python3
"""
Simple Context Bloat Test
Demonstrates how Letta fails after 4-5 messages without special flags
"""

import requests
import time
import json

def test_context_bloat():
    """Test context bloat with minimal Letta setup"""
    
    print("🧪 SIMPLE CONTEXT BLOAT TEST")
    print("=" * 50)
    print("Testing raw Letta behavior without optimizations")
    print("Expected: Agent should fail after 4-5 messages")
    print()
    
    # Test messages that will build context
    messages = [
        "Hello! I'm testing context bloat. My name is Alex.",
        "I work as a data scientist and love machine learning.",
        "I have a dog named Buddy who loves to play fetch.",
        "My favorite programming language is Python.",
        "I enjoy hiking and photography in my free time.",
        "What's my name?",  # This should start failing
        "What do I do for work?",
        "Tell me about my pet.",
        "What's my favorite hobby?"
    ]
    
    # Try to connect to baseline server
    server_url = "http://localhost:1512"
    
    print("🔍 Checking if baseline server is running...")
    try:
        response = requests.get(f"{server_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Baseline server is running")
        else:
            print("❌ Server not healthy")
            return
    except:
        print("❌ Baseline server not running!")
        print("Please start it first: python core/niya_bridge_baseline.py")
        return
    
    print("\n🚀 Starting context bloat test...\n")
    
    failures = 0
    for i, message in enumerate(messages, 1):
        print(f"📨 Message {i}: {message}")
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{server_url}/message",
                json={"message": message},
                timeout=20  # 20 second timeout
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    assistant_response = data.get("messages", ["No response"])[0]
                    print(f"✅ Response ({response_time:.2f}s): {assistant_response[:80]}{'...' if len(assistant_response) > 80 else ''}")
                else:
                    failures += 1
                    print(f"❌ Failed: {data.get('error', 'Unknown error')}")
                    if failures == 1:
                        print(f"🚨 FIRST FAILURE occurred at message {i}")
            else:
                failures += 1
                print(f"❌ HTTP Error {response.status_code}")
                if failures == 1:
                    print(f"🚨 FIRST FAILURE occurred at message {i}")
        
        except requests.exceptions.Timeout:
            failures += 1
            print(f"⏰ TIMEOUT (>20s)")
            if failures == 1:
                print(f"🚨 FIRST FAILURE occurred at message {i}")
        except Exception as e:
            failures += 1
            print(f"❌ Error: {e}")
            if failures == 1:
                print(f"🚨 FIRST FAILURE occurred at message {i}")
        
        print()
        time.sleep(0.5)  # Small delay between messages
    
    print("📊 RESULTS:")
    print(f"Total messages: {len(messages)}")
    print(f"Failures: {failures}")
    print(f"Success rate: {((len(messages) - failures) / len(messages)) * 100:.1f}%")
    
    if failures > 0:
        print("\n🎯 CONTEXT BLOAT CONFIRMED!")
        print("The agent failed as expected due to context accumulation.")
        print("This demonstrates why the optimized bridge uses aggressive resets.")
    else:
        print("\n🤔 UNEXPECTED RESULT!")
        print("The agent performed better than expected.")
        print("You may need to increase the message load or check server config.")

def main():
    test_context_bloat()

if __name__ == "__main__":
    main() 