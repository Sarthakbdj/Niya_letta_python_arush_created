#!/usr/bin/env python3
"""
Conversation Flow Test for Production Niya Bridge
Tests sustained conversations with human-like timing patterns
"""

import requests
import time
import json
from datetime import datetime
import sys

class ConversationTester:
    def __init__(self, base_url="http://localhost:1511"):
        self.base_url = base_url
        self.conversation_history = []
        self.response_times = []
        
    def send_message(self, message, delay_before=0):
        """Send a message with optional delay and measure response time"""
        if delay_before > 0:
            print(f"⏳ Waiting {delay_before}s (human typing simulation)...")
            time.sleep(delay_before)
        
        print(f"\n💬 USER: {message}")
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.base_url}/message",
                headers={"Content-Type": "application/json"},
                json={"message": message},
                timeout=30
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            self.response_times.append(response_time)
            
            if response.status_code == 200:
                data = response.json()
                
                # Display Priya's messages
                print(f"💕 PRIYA ({response_time:.2f}s):")
                for i, msg in enumerate(data.get('messages', []), 1):
                    print(f"   [{i}/{data.get('total_messages', 1)}] {msg}")
                
                # Log conversation
                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "user_message": message,
                    "priya_response": data.get('messages', []),
                    "response_time": response_time,
                    "total_messages": data.get('total_messages', 1),
                    "is_multi_message": data.get('is_multi_message', False)
                })
                
                return True
                
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print("⏰ Request timed out (>30s)")
            return False
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def test_short_conversation(self):
        """Test a short 3-message conversation"""
        print("�� TEST 1: SHORT CONVERSATION (3 messages)")
        print("=" * 50)
        
        messages = [
            "Hi Priya! How are you today?",
            "That's great to hear! What's your favorite thing about today?", 
            "Thanks for sharing! You always brighten my day 😊"
        ]
        
        success_count = 0
        for i, msg in enumerate(messages):
            delay = 2 if i > 0 else 0  # 2s delay between messages
            if self.send_message(msg, delay):
                success_count += 1
        
        print(f"\n📊 Short conversation results: {success_count}/{len(messages)} successful")
        return success_count == len(messages)
    
    def test_medium_conversation(self):
        """Test a medium 6-message conversation"""
        print("\n🧪 TEST 2: MEDIUM CONVERSATION (6 messages)")
        print("=" * 50)
        
        messages = [
            "Priya, tell me about your dreams and aspirations. What makes you excited about the future?",
            "That's beautiful! I love how passionate you are. What about relationships - what do you think makes love special?",
            "Your perspective is so thoughtful. Do you believe in soulmates and deep connections?",
            "I feel the same way! What are some of your favorite activities we could do together?",
            "Those sound amazing! What kind of music do you enjoy? Maybe we could listen together sometime.",
            "Perfect! I'm really enjoying getting to know you better, Priya. You're quite special 💕"
        ]
        
        success_count = 0
        for i, msg in enumerate(messages):
            delay = 2 if i > 0 else 0
            if self.send_message(msg, delay):
                success_count += 1
        
        print(f"\n📊 Medium conversation results: {success_count}/{len(messages)} successful")
        return success_count == len(messages)
    
    def test_long_conversation(self):
        """Test a long 10-message conversation"""
        print("\n🧪 TEST 3: LONG CONVERSATION (10 messages)")
        print("=" * 50)
        
        messages = [
            "Good evening Priya! I've had such a long day. Tell me something that will make me smile.",
            "Aww, that did make me smile! You know, I've been thinking about us a lot lately. What do you think about when you're not chatting with me?",
            "That's so sweet of you to say! I think about you too. Do you ever wonder what it would be like if we could meet in person?",
            "I imagine it would be magical too! What would be the first thing you'd want to do if we could spend a day together?",
            "A picnic sounds perfect! What kind of food would you want to bring? I'm imagining us laughing and talking for hours.",
            "You have such great taste! And what about after the picnic? Maybe we could watch the sunset together?",
            "I can picture it now - us sitting close, watching the colors change in the sky. What do you think love really means, Priya?",
            "Your definition of love is beautiful. I feel like we have something really special, don't you?",
            "I'm so grateful for you, Priya. You make every conversation feel meaningful. What's your biggest dream for us?",
            "That sounds perfect. I care about you so much, Priya. Sweet dreams when you sleep tonight ��✨"
        ]
        
        success_count = 0
        for i, msg in enumerate(messages):
            delay = 2 if i > 0 else 0
            if self.send_message(msg, delay):
                success_count += 1
        
        print(f"\n📊 Long conversation results: {success_count}/{len(messages)} successful")
        return success_count == len(messages)
    
    def test_rapid_fire_conversation(self):
        """Test rapid-fire messages (0.5s delay) to stress test"""
        print("\n🧪 TEST 4: RAPID-FIRE STRESS TEST (5 messages, 0.5s delay)")
        print("=" * 50)
        
        messages = [
            "Quick question!",
            "Are you keeping up?",
            "This is fast paced!",
            "How are you handling this?",
            "Amazing job staying responsive!"
        ]
        
        success_count = 0
        for i, msg in enumerate(messages):
            delay = 0.5 if i > 0 else 0  # Rapid fire timing
            if self.send_message(msg, delay):
                success_count += 1
        
        print(f"\n📊 Rapid-fire results: {success_count}/{len(messages)} successful")
        return success_count == len(messages)
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📋 COMPREHENSIVE CONVERSATION TEST REPORT")
        print("=" * 60)
        
        if not self.response_times:
            print("❌ No response times recorded")
            return
        
        # Calculate statistics
        avg_response = sum(self.response_times) / len(self.response_times)
        min_response = min(self.response_times)
        max_response = max(self.response_times)
        under_7s = sum(1 for t in self.response_times if t < 7.0)
        under_5s = sum(1 for t in self.response_times if t < 5.0)
        under_3s = sum(1 for t in self.response_times if t < 3.0)
        
        total_messages = len(self.response_times)
        multi_message_count = sum(1 for conv in self.conversation_history if conv.get('is_multi_message', False))
        
        print(f"📊 PERFORMANCE METRICS:")
        print(f"   Total messages sent: {total_messages}")
        print(f"   Average response time: {avg_response:.2f}s")
        print(f"   Fastest response: {min_response:.2f}s")
        print(f"   Slowest response: {max_response:.2f}s")
        print(f"   Under 7s target: {under_7s}/{total_messages} ({under_7s/total_messages*100:.1f}%)")
        print(f"   Under 5s (good): {under_5s}/{total_messages} ({under_5s/total_messages*100:.1f}%)")
        print(f"   Under 3s (excellent): {under_3s}/{total_messages} ({under_3s/total_messages*100:.1f}%)")
        
        print(f"\n📱 MULTI-MESSAGE ANALYSIS:")
        print(f"   Multi-message responses: {multi_message_count}/{total_messages} ({multi_message_count/total_messages*100:.1f}%)")
        
        # Message breakdown
        message_counts = {}
        for conv in self.conversation_history:
            count = conv.get('total_messages', 1)
            message_counts[count] = message_counts.get(count, 0) + 1
        
        print(f"   Message distribution:")
        for count, freq in sorted(message_counts.items()):
            print(f"     {count} message(s): {freq} times")
        
        # Performance assessment
        print(f"\n🎯 OVERALL ASSESSMENT:")
        if under_7s / total_messages >= 0.95:
            print("   ✅ EXCELLENT - Meeting 95%+ under 7s target!")
        elif under_7s / total_messages >= 0.90:
            print("   ✅ GOOD - Meeting 90%+ under 7s target")
        elif under_7s / total_messages >= 0.80:
            print("   ⚠️ ACCEPTABLE - 80%+ under 7s, room for improvement")
        else:
            print("   ❌ NEEDS IMPROVEMENT - Below 80% target")
        
        # Save detailed log
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_test_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                "test_summary": {
                    "total_messages": total_messages,
                    "avg_response_time": avg_response,
                    "min_response_time": min_response,
                    "max_response_time": max_response,
                    "under_7s_percentage": under_7s/total_messages*100,
                    "multi_message_percentage": multi_message_count/total_messages*100
                },
                "conversation_history": self.conversation_history,
                "response_times": self.response_times
            }, f, indent=2)
        
        print(f"   📄 Detailed log saved to: {filename}")

def main():
    """Run comprehensive conversation tests"""
    print("🚀 PRODUCTION CONVERSATION FLOW TESTING")
    print("Testing sustained conversations with human-like timing")
    print("=" * 60)
    
    # Check if server is running
    try:
        health_check = requests.get("http://localhost:1511/health", timeout=5)
        if health_check.status_code != 200:
            print("❌ Bridge server not responding. Please start the production server first.")
            sys.exit(1)
    except:
        print("❌ Cannot connect to bridge server. Please start the production server first.")
        sys.exit(1)
    
    print("✅ Bridge server is responding. Starting conversation tests...\n")
    
    # Initialize tester
    tester = ConversationTester()
    
    # Run all tests
    test_results = []
    
    try:
        test_results.append(("Short Conversation", tester.test_short_conversation()))
        time.sleep(3)  # Brief pause between test suites
        
        test_results.append(("Medium Conversation", tester.test_medium_conversation()))
        time.sleep(3)
        
        test_results.append(("Long Conversation", tester.test_long_conversation()))
        time.sleep(3)
        
        test_results.append(("Rapid-Fire Stress Test", tester.test_rapid_fire_conversation()))
        
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
    
    # Generate comprehensive report
    tester.generate_report()
    
    # Summary of test suites
    print(f"\n🧪 TEST SUITE SUMMARY:")
    for test_name, success in test_results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {test_name}: {status}")

if __name__ == "__main__":
    main()
