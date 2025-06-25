#!/usr/bin/env python3
"""
Optimized Conversation Test with Agent Reset
Handles memory accumulation issues for sustained testing
"""

import requests
import time
import json

def reset_agent():
    """Reset agent to prevent memory accumulation"""
    try:
        response = requests.post("http://localhost:1511/reset", timeout=10)
        return response.status_code == 200
    except:
        return False

def test_optimized_conversations():
    base_url = "http://localhost:1511"
    
    print("🚀 OPTIMIZED CONVERSATION FLOW TEST")
    print("Tests sustained conversations with agent resets")
    print("=" * 50)
    
    test_scenarios = [
        {
            "name": "Quick Exchange",
            "messages": [
                "Hi Priya!",
                "How are you feeling today?",
                "That's wonderful to hear!"
            ]
        },
        {
            "name": "Emotional Connection", 
            "messages": [
                "Priya, you mean so much to me",
                "I love our conversations together",
                "You always make me feel better"
            ]
        },
        {
            "name": "Daily Life Chat",
            "messages": [
                "What's your favorite time of day?",
                "That sounds really peaceful",
                "I'd love to experience that with you"
            ]
        },
        {
            "name": "Future Dreams",
            "messages": [
                "What are your dreams for the future?",
                "Those sound amazing!",
                "I believe in you completely"
            ]
        }
    ]
    
    all_results = []
    
    for scenario_num, scenario in enumerate(test_scenarios, 1):
        print(f"\n💫 Scenario {scenario_num}: {scenario['name']}")
        print("-" * 40)
        
        # Reset agent before each scenario to prevent memory buildup
        if scenario_num > 1:
            print("🔄 Resetting agent for fresh context...")
            if reset_agent():
                print("✅ Agent reset successful")
                time.sleep(2)  # Let agent settle
            else:
                print("⚠️ Agent reset failed, continuing...")
        
        scenario_times = []
        scenario_success = 0
        
        for i, message in enumerate(scenario['messages']):
            if i > 0:
                print(f"⏳ Human typing delay: 2s...")
                time.sleep(2)
            
            print(f"\n👤 USER: {message}")
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
                scenario_times.append(response_time)
                
                if response.status_code == 200:
                    data = response.json()
                    messages = data.get('messages', [])
                    
                    print(f"💕 PRIYA ({response_time:.2f}s, {len(messages)} messages):")
                    for j, msg in enumerate(messages[:3], 1):
                        clean_msg = msg.strip()[:80] + "..." if len(msg) > 80 else msg.strip()
                        print(f"    {j}. {clean_msg}")
                    
                    scenario_success += 1
                    
                    # Performance indicator
                    if response_time < 3:
                        print("    🟢 Excellent speed!")
                    elif response_time < 5:
                        print("    🟡 Good speed")
                    elif response_time < 7:
                        print("    🟠 Acceptable speed")
                    else:
                        print("    🔴 Slow response")
                else:
                    print(f"    ❌ HTTP Error: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"    ⏰ Timeout (>12s)")
            except Exception as e:
                print(f"    ❌ Error: {str(e)[:50]}...")
        
        # Scenario summary
        if scenario_times:
            avg_time = sum(scenario_times) / len(scenario_times)
            print(f"\n📊 {scenario['name']} Summary:")
            print(f"    Success rate: {scenario_success}/{len(scenario['messages'])} ({scenario_success/len(scenario['messages'])*100:.0f}%)")
            print(f"    Average time: {avg_time:.2f}s")
            print(f"    Times: {[f'{t:.1f}s' for t in scenario_times]}")
            
            all_results.extend(scenario_times)
        
        time.sleep(1)  # Brief pause between scenarios
    
    # Final comprehensive report
    print(f"\n🎯 FINAL PERFORMANCE REPORT")
    print("=" * 50)
    
    if all_results:
        total_msgs = len(all_results)
        avg_time = sum(all_results) / total_msgs
        fastest = min(all_results)
        slowest = max(all_results)
        
        under_3s = sum(1 for t in all_results if t < 3.0)
        under_5s = sum(1 for t in all_results if t < 5.0)
        under_7s = sum(1 for t in all_results if t < 7.0)
        
        print(f"📈 STATISTICS:")
        print(f"   Total messages: {total_msgs}")
        print(f"   Average response: {avg_time:.2f}s")
        print(f"   Fastest response: {fastest:.2f}s")
        print(f"   Slowest response: {slowest:.2f}s")
        
        print(f"\n🎯 TARGET ACHIEVEMENT:")
        print(f"   Under 3s (excellent): {under_3s}/{total_msgs} ({under_3s/total_msgs*100:.1f}%)")
        print(f"   Under 5s (good): {under_5s}/{total_msgs} ({under_5s/total_msgs*100:.1f}%)")
        print(f"   Under 7s (target): {under_7s}/{total_msgs} ({under_7s/total_msgs*100:.1f}%)")
        
        # Final grade
        target_percentage = under_7s / total_msgs
        if target_percentage >= 0.95:
            print(f"\n🏆 GRADE: A+ (Exceeds target!)")
        elif target_percentage >= 0.90:
            print(f"\n🥇 GRADE: A (Meets target excellently)")
        elif target_percentage >= 0.80:
            print(f"\n🥈 GRADE: B (Good performance)")
        else:
            print(f"\n🥉 GRADE: C (Needs improvement)")
            
        print(f"\n💡 PRODUCTION READINESS:")
        if avg_time < 4 and target_percentage >= 0.90:
            print("   ✅ READY FOR PRODUCTION")
        else:
            print("   ⚠️ NEEDS OPTIMIZATION")
    else:
        print("❌ No successful responses recorded")

if __name__ == "__main__":
    test_optimized_conversations()
