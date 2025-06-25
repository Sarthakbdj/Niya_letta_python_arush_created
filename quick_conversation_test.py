#!/usr/bin/env python3
"""
Quick Conversation Test - Simple and reliable
Tests conversation flow with realistic timing
"""

import requests
import time
import json

def test_conversation():
    base_url = "http://localhost:1511"
    
    print("🧪 QUICK CONVERSATION FLOW TEST")
    print("=" * 40)
    
    conversations = [
        {
            "name": "Morning Chat",
            "messages": [
                "Good morning Priya! How are you?",
                "That sounds great! What are your plans today?",
                "Sounds lovely! I hope you have a wonderful day 😊"
            ]
        },
        {
            "name": "Evening Chat", 
            "messages": [
                "Hi Priya! How was your day?",
                "That's wonderful to hear! Any highlights?",
                "You always make me smile! Sweet dreams 💕"
            ]
        }
    ]
    
    all_response_times = []
    
    for conv in conversations:
        print(f"\n💬 {conv['name']}")
        print("-" * 30)
        
        for i, message in enumerate(conv['messages']):
            if i > 0:
                print(f"⏳ Waiting 2s...")
                time.sleep(2)
            
            print(f"USER: {message}")
            start_time = time.time()
            
            try:
                response = requests.post(
                    f"{base_url}/message",
                    headers={"Content-Type": "application/json"},
                    json={"message": message},
                    timeout=15  # Reduced timeout
                )
                
                end_time = time.time()
                response_time = end_time - start_time
                all_response_times.append(response_time)
                
                if response.status_code == 200:
                    data = response.json()
                    messages = data.get('messages', [])
                    
                    print(f"PRIYA ({response_time:.2f}s, {len(messages)} msgs):")
                    for j, msg in enumerate(messages[:3], 1):  # Max 3 messages
                        clean_msg = msg.strip()[:100] + "..." if len(msg) > 100 else msg.strip()
                        print(f"  [{j}] {clean_msg}")
                    
                    print(f"✅ Success - {len(messages)} messages")
                else:
                    print(f"❌ Error: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"⏰ Timeout (>15s)")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        time.sleep(3)  # Pause between conversations
    
    # Summary
    print(f"\n📊 PERFORMANCE SUMMARY")
    print("=" * 40)
    if all_response_times:
        avg_time = sum(all_response_times) / len(all_response_times)
        max_time = max(all_response_times)
        min_time = min(all_response_times)
        under_7s = sum(1 for t in all_response_times if t < 7.0)
        
        print(f"Total messages: {len(all_response_times)}")
        print(f"Average time: {avg_time:.2f}s")
        print(f"Fastest: {min_time:.2f}s")
        print(f"Slowest: {max_time:.2f}s")
        print(f"Under 7s: {under_7s}/{len(all_response_times)} ({under_7s/len(all_response_times)*100:.1f}%)")
        
        if under_7s / len(all_response_times) >= 0.95:
            print("🎯 EXCELLENT - Meeting target!")
        else:
            print("⚠️ Needs improvement")
    else:
        print("❌ No successful responses")

if __name__ == "__main__":
    test_conversation()
