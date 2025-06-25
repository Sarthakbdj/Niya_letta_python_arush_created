#!/usr/bin/env python3
"""
Memory-Enhanced Conversation Test
Tests conversation memory persistence across agent resets
"""

import requests
import time
import json

def test_memory_enhanced_conversation():
    base_url = "http://localhost:1511"
    
    print("🧠 MEMORY-ENHANCED CONVERSATION TEST")
    print("Testing conversation memory across agent resets")
    print("=" * 60)
    
    # Test conversation that builds context over multiple resets
    messages = [
        # Messages 1-4: Build initial context (should trigger reset after 4)
        "Hi Priya! My name is Alex and I love playing guitar.",
        "Yes, I play rock and blues mostly. My favorite color is blue.",
        "I'm really into astronomy too. I love stargazing on clear nights.",
        "That's right! I have a telescope. Do you have any hobbies?",  # Reset here
        
        # Messages 5-8: Test memory retention (should remember Alex, guitar, blue, astronomy)
        "Alex here again! Do you remember what instrument I play?",
        "Exactly! And do you recall my favorite color?",
        "Perfect memory! What about my other hobby with the night sky?",
        "Amazing! You remembered everything. What's your favorite season?",  # Reset here
        
        # Messages 9-12: Test deeper memory building
        "Hi Priya! Alex again. Since you know I love astronomy, what do you think about space?",
        "That's beautiful! Do you remember what music genres I like?",
        "Spot on! With my blue guitar and love for stars, I feel we have a connection.",
        "You're so thoughtful! I feel like you really know me now."
    ]
    
    results = []
    session_id = None
    
    for i, message in enumerate(messages, 1):
        print(f"\n{'='*50}")
        print(f"MESSAGE {i}/12: {message}")
        print(f"{'='*50}")
        
        if i > 1:
            print("⏳ 2s typing delay...")
            time.sleep(2)
        
        start_time = time.time()
        
        try:
            payload = {"message": message}
            if session_id:
                payload["session_id"] = session_id
            
            response = requests.post(
                f"{base_url}/message",
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=15
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Get session ID from first response
                if not session_id:
                    session_id = data.get('session_id')
                    print(f"📝 Session ID: {session_id}")
                
                messages_received = data.get('messages', [])
                agent_msg_count = data.get('agent_message_count', 0)
                agent_age = data.get('agent_age_seconds', 0)
                memory_enabled = data.get('memory_enabled', False)
                
                print(f"�� PRIYA ({response_time:.2f}s, Memory: {memory_enabled}):")
                print(f"   Agent: Count={agent_msg_count}, Age={agent_age}s")
                
                for j, msg in enumerate(messages_received, 1):
                    display_msg = msg[:80] + "..." if len(msg) > 80 else msg
                    print(f"   [{j}] {display_msg}")
                
                # Performance indicator
                if response_time < 3:
                    perf = "🟢 EXCELLENT"
                elif response_time < 5:
                    perf = "🟡 GOOD"
                else:
                    perf = "🟠 ACCEPTABLE"
                
                print(f"   {perf} | {len(messages_received)} msgs | {response_time:.2f}s")
                
                # Check for memory evidence in responses
                memory_evidence = []
                full_response = ' '.join(messages_received).lower()
                
                # Look for memory indicators
                if i >= 5:  # After first reset
                    if "guitar" in full_response:
                        memory_evidence.append("🎸 Remembers guitar")
                    if "blue" in full_response:
                        memory_evidence.append("💙 Remembers blue")
                    if "astronomy" in full_response or "star" in full_response or "telescope" in full_response:
                        memory_evidence.append("🌟 Remembers astronomy")
                    if "alex" in full_response:
                        memory_evidence.append("👤 Remembers name")
                
                if memory_evidence:
                    print(f"   🧠 Memory Evidence: {', '.join(memory_evidence)}")
                
                # Detect resets
                reset_detected = agent_msg_count == 1 and i > 1
                if reset_detected:
                    print(f"   🔄 AGENT RESET DETECTED!")
                
                results.append({
                    "message_num": i,
                    "response_time": response_time,
                    "success": True,
                    "agent_msg_count": agent_msg_count,
                    "reset_detected": reset_detected,
                    "memory_evidence": memory_evidence,
                    "memory_enabled": memory_enabled
                })
                
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                results.append({
                    "message_num": i,
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                })
                
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)[:50]}...")
            results.append({
                "message_num": i,
                "success": False,
                "error": str(e)[:50]
            })
    
    # Get memory summary
    if session_id:
        try:
            memory_response = requests.get(f"{base_url}/memory/summary/{session_id}")
            if memory_response.status_code == 200:
                memory_data = memory_response.json()
                print(f"\n🧠 MEMORY SUMMARY:")
                print(f"   Session: {session_id}")
                summary = memory_data.get('summary', {})
                print(f"   Total messages: {summary.get('total_messages', 0)}")
                print(f"   Recent topics: {summary.get('recent_topics', [])}")
                print(f"   User preferences: {summary.get('user_preferences', [])}")
                print(f"   Key memories: {summary.get('key_memories', [])}")
        except:
            print(f"\n⚠️ Could not retrieve memory summary")
    
    # Analysis
    print(f"\n🎯 MEMORY-ENHANCED ANALYSIS")
    print("=" * 60)
    
    successful_results = [r for r in results if r['success']]
    failed_results = [r for r in results if not r['success']]
    
    if successful_results:
        response_times = [r['response_time'] for r in successful_results]
        avg_time = sum(response_times) / len(response_times)
        
        under_7s = sum(1 for t in response_times if t < 7.0)
        resets_detected = sum(1 for r in successful_results if r.get('reset_detected', False))
        
        # Memory analysis
        memory_messages = [r for r in successful_results[4:] if r.get('memory_evidence')]  # After first reset
        memory_retention_rate = len(memory_messages) / max(1, len(successful_results[4:]))
        
        print(f"📊 PERFORMANCE METRICS:")
        print(f"   Successful: {len(successful_results)}/12 ({len(successful_results)/12*100:.0f}%)")
        print(f"   Average time: {avg_time:.2f}s")
        print(f"   Under 7s: {under_7s}/{len(successful_results)} ({under_7s/len(successful_results)*100:.0f}%)")
        
        print(f"\n🔄 RESET ANALYSIS:")
        print(f"   Resets detected: {resets_detected}")
        print(f"   Expected resets: 2-3 (every 4 messages)")
        
        print(f"\n🧠 MEMORY ANALYSIS:")
        print(f"   Memory retention rate: {memory_retention_rate*100:.0f}%")
        print(f"   Messages with memory evidence: {len(memory_messages)}")
        
        # Show memory evidence timeline
        print(f"\n📈 MEMORY EVIDENCE TIMELINE:")
        for result in successful_results[4:]:  # After first reset
            evidence = result.get('memory_evidence', [])
            if evidence:
                print(f"   Message {result['message_num']}: {', '.join(evidence)}")
        
        # Final assessment
        success_rate = len(successful_results) / 12
        performance_rate = under_7s / len(successful_results) if successful_results else 0
        
        print(f"\n🏆 FINAL ASSESSMENT:")
        if success_rate >= 0.9 and performance_rate >= 0.8 and memory_retention_rate >= 0.5:
            print("   A+ | EXCELLENT - Memory system working perfectly!")
        elif success_rate >= 0.8 and performance_rate >= 0.7 and memory_retention_rate >= 0.3:
            print("   A  | VERY GOOD - Strong performance with good memory")
        elif success_rate >= 0.7 and performance_rate >= 0.6:
            print("   B  | GOOD - Decent performance, memory needs improvement")
        else:
            print("   C  | NEEDS WORK - Significant issues remain")
    
    else:
        print("❌ COMPLETE FAILURE - No successful responses")
    
    if failed_results:
        print(f"\n❌ FAILURES:")
        for failure in failed_results:
            print(f"   Msg {failure['message_num']}: {failure.get('error', 'Unknown')}")

if __name__ == "__main__":
    print("🚀 Starting Memory-Enhanced Test...")
    print("This tests conversation memory across agent resets\n")
    
    test_memory_enhanced_conversation()
