#!/usr/bin/env python3
"""
Aggressive Reset Test - 10 Messages
Tests the new aggressive reset strategy (every 4 messages)
with timeout protection
"""

import requests
import time
import json

def test_aggressive_reset():
    base_url = "http://localhost:1511"
    
    print("🔥 AGGRESSIVE RESET TEST (10 Messages)")
    print("Testing every-4-message reset + timeout protection")
    print("=" * 55)
    
    # Focused conversation - should trigger 2 resets (at msg 4 and 8)
    messages = [
        "Hi Priya! How are you today?",
        "That's wonderful! What's your favorite color?", 
        "Beautiful choice! Do you like music?",
        "What kind of songs make you happy?",  # Reset should happen here (msg 4)
        
        "That sounds amazing! Tell me about your dreams.",
        "I love your perspective! What makes you smile?",
        "You're so thoughtful! Do you believe in love?", 
        "Your view on love is beautiful! What are your hobbies?",  # Reset should happen here (msg 8)
        
        "Those hobbies sound fun! What's your favorite season?",
        "Perfect choice! You always know what to say 💕"
    ]
    
    results = []
    
    for i, message in enumerate(messages, 1):
        print(f"\n{'='*40}")
        print(f"MESSAGE {i}/10: {message}")
        print(f"{'='*40}")
        
        # Human typing delay
        if i > 1:
            print("⏳ 2s typing delay...")
            time.sleep(2)
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{base_url}/message",
                headers={"Content-Type": "application/json"},
                json={"message": message},
                timeout=12  # Reasonable timeout
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                messages_received = data.get('messages', [])
                agent_msg_count = data.get('agent_message_count', 0)
                agent_age = data.get('agent_age_seconds', 0)
                
                print(f"💕 PRIYA ({response_time:.2f}s):")
                print(f"   Agent: Count={agent_msg_count}, Age={agent_age}s")
                
                for j, msg in enumerate(messages_received, 1):
                    display_msg = msg[:70] + "..." if len(msg) > 70 else msg
                    print(f"   [{j}] {display_msg}")
                
                # Performance indicator
                if response_time < 3:
                    perf = "🟢 EXCELLENT"
                elif response_time < 5:
                    perf = "🟡 GOOD"
                elif response_time < 7:
                    perf = "🟠 ACCEPTABLE"
                else:
                    perf = "🔴 SLOW"
                
                print(f"   {perf} | {len(messages_received)} msgs | {response_time:.2f}s")
                
                # Detect resets (agent_msg_count resets to 1)
                reset_detected = agent_msg_count == 1 and i > 1
                if reset_detected:
                    print(f"   🔄 AGENT RESET DETECTED!")
                
                results.append({
                    "message_num": i,
                    "response_time": response_time,
                    "success": True,
                    "agent_msg_count": agent_msg_count,
                    "agent_age": agent_age,
                    "reset_detected": reset_detected,
                    "message_count": len(messages_received)
                })
                
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                results.append({
                    "message_num": i,
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                })
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ TIMEOUT")
            results.append({
                "message_num": i,
                "success": False,
                "error": "Timeout"
            })
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)[:50]}...")
            results.append({
                "message_num": i,
                "success": False,
                "error": str(e)[:50]
            })
    
    # Analysis
    print(f"\n🎯 AGGRESSIVE RESET ANALYSIS")
    print("=" * 55)
    
    successful_results = [r for r in results if r['success']]
    failed_results = [r for r in results if not r['success']]
    
    if successful_results:
        response_times = [r['response_time'] for r in successful_results]
        avg_time = sum(response_times) / len(response_times)
        
        under_7s = sum(1 for t in response_times if t < 7.0)
        resets_detected = sum(1 for r in successful_results if r.get('reset_detected', False))
        
        print(f"📊 SUCCESS METRICS:")
        print(f"   Successful: {len(successful_results)}/10 ({len(successful_results)/10*100:.0f}%)")
        print(f"   Failed: {len(failed_results)}")
        print(f"   Average time: {avg_time:.2f}s")
        print(f"   Under 7s: {under_7s}/{len(successful_results)} ({under_7s/len(successful_results)*100:.0f}%)")
        
        print(f"\n🔄 RESET ANALYSIS:")
        print(f"   Resets detected: {resets_detected}")
        print(f"   Expected resets: 2 (at messages 4 & 8)")
        
        # Show agent progression
        agent_counts = [r.get('agent_msg_count', 0) for r in successful_results]
        print(f"   Agent message counts: {agent_counts}")
        
        # Final assessment
        success_rate = len(successful_results) / 10
        performance_rate = under_7s / len(successful_results) if successful_results else 0
        
        print(f"\n🏆 FINAL ASSESSMENT:")
        if success_rate >= 0.9 and performance_rate >= 0.8:
            if resets_detected >= 1:
                print("   A+ | EXCELLENT - Aggressive reset strategy working!")
            else:
                print("   A  | VERY GOOD - Performance excellent, reset strategy unclear")
        elif success_rate >= 0.7 and performance_rate >= 0.7:
            print("   B  | GOOD - Decent performance, some issues")
        else:
            print("   C  | NEEDS WORK - Significant problems remain")
    
    else:
        print("❌ COMPLETE FAILURE - No successful responses")
    
    if failed_results:
        print(f"\n❌ FAILURES:")
        for failure in failed_results:
            print(f"   Msg {failure['message_num']}: {failure.get('error', 'Unknown')}")

if __name__ == "__main__":
    print("🚀 Starting Aggressive Reset Test...")
    print("This will test the new 4-message reset strategy\n")
    
    test_aggressive_reset()
