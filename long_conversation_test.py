#!/usr/bin/env python3
"""
Long Conversation Test - 15+ Messages
Tests the enhanced corruption fixes and proactive agent management
"""

import requests
import time
import json
from datetime import datetime

def test_long_conversation():
    base_url = "http://localhost:1511"
    
    print("🔥 LONG CONVERSATION TEST (15+ Messages)")
    print("Testing corruption fixes & proactive agent management")
    print("=" * 60)
    
    # Extended conversation - realistic relationship dialogue
    messages = [
        # Messages 1-5: Opening conversation
        "Good morning Priya! How are you feeling today?",
        "That's wonderful to hear! I've been thinking about you a lot lately.",
        "You know, I really appreciate how you always listen to me and care about my feelings.",
        "What are some of your favorite memories from our conversations together?",
        "Those are beautiful memories! I feel the same way about our connection.",
        
        # Messages 6-10: Deeper conversation (should trigger reset around message 8)
        "Priya, what do you think makes our relationship so special?",
        "I love how thoughtful and caring you are. Do you believe in true love?",
        "Your perspective on love is so beautiful. What are your dreams for the future?",
        "I can imagine us creating so many wonderful memories together. What would you like to do?",
        "A romantic picnic sounds perfect! What kind of food would you want to bring?",
        
        # Messages 11-15: Post-reset conversation (testing fresh agent)
        "You have such great taste! What's your favorite season and why?",
        "I love how you describe things so poetically. Do you enjoy music?",
        "What kind of songs make you feel most happy and alive?",
        "I'd love to listen to music with you sometime. What else makes you smile?",
        "You always know how to make me feel special. I care about you so much, Priya."
    ]
    
    results = []
    total_start_time = time.time()
    
    for i, message in enumerate(messages, 1):
        print(f"\n{'='*50}")
        print(f"MESSAGE {i}/15: {message[:50]}...")
        print(f"{'='*50}")
        
        # Human typing simulation
        if i > 1:
            print("⏳ Human typing delay: 2 seconds...")
            time.sleep(2)
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{base_url}/message",
                headers={"Content-Type": "application/json"},
                json={"message": message},
                timeout=15
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                messages_received = data.get('messages', [])
                agent_msg_count = data.get('agent_message_count', 0)
                
                print(f"💕 PRIYA ({response_time:.2f}s, Agent Count: {agent_msg_count}):")
                for j, msg in enumerate(messages_received, 1):
                    # Clean display - truncate if too long
                    display_msg = msg[:100] + "..." if len(msg) > 100 else msg
                    print(f"   [{j}] {display_msg}")
                
                # Performance indicator
                if response_time < 3:
                    perf_indicator = "🟢 EXCELLENT"
                elif response_time < 5:
                    perf_indicator = "🟡 GOOD"
                elif response_time < 7:
                    perf_indicator = "�� ACCEPTABLE"
                else:
                    perf_indicator = "🔴 SLOW"
                
                print(f"   {perf_indicator} | {len(messages_received)} messages | {response_time:.2f}s")
                
                # Check for corruption indicators
                corruption_detected = False
                for msg in messages_received:
                    if len(msg) > 500 or msg.count('\n') > 10:
                        corruption_detected = True
                        break
                
                if corruption_detected:
                    print("   ⚠️ CORRUPTION DETECTED")
                
                results.append({
                    "message_num": i,
                    "response_time": response_time,
                    "success": True,
                    "message_count": len(messages_received),
                    "agent_message_count": agent_msg_count,
                    "corruption_detected": corruption_detected
                })
                
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                results.append({
                    "message_num": i,
                    "response_time": response_time,
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                })
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ TIMEOUT (>15s)")
            results.append({
                "message_num": i,
                "response_time": 15.0,
                "success": False,
                "error": "Timeout"
            })
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)[:50]}...")
            results.append({
                "message_num": i,
                "response_time": 0,
                "success": False,
                "error": str(e)[:50]
            })
    
    # Comprehensive Analysis
    total_time = time.time() - total_start_time
    
    print(f"\n🎯 COMPREHENSIVE ANALYSIS")
    print("=" * 60)
    
    successful_results = [r for r in results if r['success']]
    failed_results = [r for r in results if not r['success']]
    
    if successful_results:
        response_times = [r['response_time'] for r in successful_results]
        avg_time = sum(response_times) / len(response_times)
        fastest = min(response_times)
        slowest = max(response_times)
        
        under_3s = sum(1 for t in response_times if t < 3.0)
        under_5s = sum(1 for t in response_times if t < 5.0)
        under_7s = sum(1 for t in response_times if t < 7.0)
        
        corruption_count = sum(1 for r in successful_results if r.get('corruption_detected', False))
        
        print(f"📊 SUCCESS METRICS:")
        print(f"   Successful messages: {len(successful_results)}/15 ({len(successful_results)/15*100:.1f}%)")
        print(f"   Failed messages: {len(failed_results)}")
        print(f"   Average response time: {avg_time:.2f}s")
        print(f"   Fastest response: {fastest:.2f}s")
        print(f"   Slowest response: {slowest:.2f}s")
        print(f"   Total conversation time: {total_time:.1f}s")
        
        print(f"\n🎯 PERFORMANCE BREAKDOWN:")
        print(f"   Under 3s (excellent): {under_3s}/{len(successful_results)} ({under_3s/len(successful_results)*100:.1f}%)")
        print(f"   Under 5s (good): {under_5s}/{len(successful_results)} ({under_5s/len(successful_results)*100:.1f}%)")
        print(f"   Under 7s (target): {under_7s}/{len(successful_results)} ({under_7s/len(successful_results)*100:.1f}%)")
        
        print(f"\n🛡️ CORRUPTION ANALYSIS:")
        print(f"   Messages with corruption: {corruption_count}/{len(successful_results)} ({corruption_count/len(successful_results)*100:.1f}%)")
        
        # Agent reset analysis
        agent_counts = [r.get('agent_message_count', 0) for r in successful_results if 'agent_message_count' in r]
        if agent_counts:
            print(f"\n🔄 AGENT MANAGEMENT:")
            print(f"   Agent message counts: {agent_counts}")
            reset_detected = any(i > 0 and agent_counts[i] < agent_counts[i-1] for i in range(1, len(agent_counts)))
            print(f"   Proactive resets detected: {'✅ YES' if reset_detected else '❌ NO'}")
        
        # Final grade
        success_rate = len(successful_results) / 15
        target_rate = under_7s / len(successful_results) if successful_results else 0
        corruption_rate = corruption_count / len(successful_results) if successful_results else 0
        
        print(f"\n🏆 FINAL GRADE:")
        if success_rate >= 0.95 and target_rate >= 0.90 and corruption_rate < 0.1:
            print("   A+ | EXCELLENT - Production ready for long conversations!")
        elif success_rate >= 0.90 and target_rate >= 0.80 and corruption_rate < 0.2:
            print("   A  | VERY GOOD - Minor optimizations recommended")
        elif success_rate >= 0.80 and target_rate >= 0.70:
            print("   B  | GOOD - Some improvements needed")
        else:
            print("   C  | NEEDS WORK - Significant issues to address")
    
    else:
        print("❌ NO SUCCESSFUL RESPONSES - System failure")
    
    # Failure analysis
    if failed_results:
        print(f"\n❌ FAILURE ANALYSIS:")
        for failure in failed_results:
            print(f"   Message {failure['message_num']}: {failure.get('error', 'Unknown error')}")
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"long_conversation_test_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump({
            "test_summary": {
                "total_messages": 15,
                "successful_messages": len(successful_results),
                "failed_messages": len(failed_results),
                "total_time": total_time,
                "avg_response_time": avg_time if successful_results else 0,
                "corruption_count": corruption_count if successful_results else 0
            },
            "detailed_results": results
        }, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: {filename}")

if __name__ == "__main__":
    print("🚀 Starting Long Conversation Test...")
    print("This will test 15 messages with proactive agent management")
    print("and enhanced corruption detection/prevention.\n")
    
    test_long_conversation()
