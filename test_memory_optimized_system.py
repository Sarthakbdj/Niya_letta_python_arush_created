#!/usr/bin/env python3
"""
Test Memory-Optimized System
Comprehensive test of advanced memory features including:
- Specialized memory blocks
- Intelligent consolidation
- Adaptive learning with confidence
- Smart context injection
- Memory health monitoring
- Predictive memory loading
"""

import time
import json
import requests
from datetime import datetime
from typing import List, Dict

class MemoryOptimizedTester:
    def __init__(self, base_url: str = "http://localhost:1511"):
        self.base_url = base_url
        self.test_results = []
        
    def run_comprehensive_test(self):
        """Run comprehensive test of all memory optimization features"""
        
        print("🧠 MEMORY-OPTIMIZED SYSTEM TEST")
        print("=" * 50)
        print("Testing advanced memory features:")
        print("✓ Specialized memory blocks")
        print("✓ Intelligent consolidation") 
        print("✓ Adaptive learning with confidence")
        print("✓ Smart context injection")
        print("✓ Memory health monitoring")
        print("✓ Predictive memory loading")
        print("=" * 50)
        
        # Test conversation with rich personal information
        test_messages = [
            "Hi! My name is Sarah and I'm really excited to chat with you today!",
            "I'm a software engineer at Google, and I absolutely love coding in Python. It's my favorite programming language!",
            "I live in San Francisco with my boyfriend Mark. We've been together for 3 years now.",
            "My biggest hobby is rock climbing. I go to the climbing gym 3 times a week and I love outdoor climbing too!",
            "I'm feeling a bit stressed about work lately. We have a big project deadline coming up next week.",
            "But I'm also really excited because Mark and I are planning a trip to Yosemite next month for some outdoor climbing!",
            "I have a pet cat named Luna who's absolutely adorable. She's a black and white tuxedo cat.",
            "What about you? Do you remember what I told you about my work and hobbies?",
            "I'm curious - can you tell me about my relationship status and my pet?",
            "Let's talk about something different. What do you think about artificial intelligence?",
            "Actually, going back to personal stuff - I mentioned I love Python programming. Do you remember that?",
            "I'm feeling much better now after talking with you. You seem to remember things about me well!",
            "One more test - can you remind me what my boyfriend's name is and where I work?",
            "This has been a great conversation! I'm impressed with your memory capabilities.",
            "Before we end, can you summarize what you've learned about me today?"
        ]
        
        start_time = time.time()
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n📝 Message {i}/15: {message[:50]}...")
            
            # Send message
            response_data = self.send_message(message)
            
            if response_data:
                # Display response
                responses = response_data.get('response', [])
                for j, resp in enumerate(responses, 1):
                    print(f"🤖 Priya {j}: {resp}")
                
                # Show memory metrics
                memory_health = response_data.get('memory_health', 0)
                memory_details = response_data.get('memory_details', {})
                conversation_stage = response_data.get('conversation_stage', 'unknown')
                
                print(f"🧠 Memory Health: {memory_health:.2f}")
                print(f"📊 Stage: {conversation_stage}")
                print(f"🎯 Retention: {memory_details.get('retention_score', 0):.2f}")
                print(f"🔄 Consistency: {memory_details.get('consistency_score', 0):.2f}")
                print(f"⚡ Learning: {memory_details.get('learning_velocity', 0):.2f}")
                
                # Store results
                self.test_results.append({
                    'message_num': i,
                    'user_message': message,
                    'priya_responses': responses,
                    'response_time': response_data.get('response_time', 0),
                    'memory_health': memory_health,
                    'memory_details': memory_details,
                    'conversation_stage': conversation_stage,
                    'message_count': response_data.get('message_count', 0)
                })
                
                # Check for memory references in key messages
                if i in [8, 9, 11, 13]:  # Memory test messages
                    self.analyze_memory_retention(i, message, responses)
                
            else:
                print("❌ Failed to get response")
                break
            
            # Small delay between messages
            time.sleep(1)
        
        # Final analysis
        total_time = time.time() - start_time
        self.generate_comprehensive_report(total_time)

    def send_message(self, message: str) -> Dict:
        """Send message to bridge and return response"""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={"message": message},
                timeout=20
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return None

    def analyze_memory_retention(self, message_num: int, user_message: str, responses: List[str]):
        """Analyze memory retention in responses"""
        
        # Key facts to look for
        memory_targets = {
            'name': ['sarah', 'Sarah'],
            'job': ['software engineer', 'google', 'Google', 'coding', 'python', 'Python'],
            'relationship': ['boyfriend', 'mark', 'Mark', '3 years'],
            'hobby': ['rock climbing', 'climbing', 'gym'],
            'pet': ['cat', 'luna', 'Luna', 'tuxedo'],
            'location': ['san francisco', 'San Francisco']
        }
        
        response_text = ' '.join(responses).lower()
        
        found_memories = []
        for category, keywords in memory_targets.items():
            if any(keyword.lower() in response_text for keyword in keywords):
                found_memories.append(category)
        
        print(f"🎯 Memory Check: Found {len(found_memories)} categories: {found_memories}")
        
        return found_memories

    def get_memory_status(self) -> Dict:
        """Get detailed memory system status"""
        try:
            response = requests.get(f"{self.base_url}/memory/status")
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}

    def get_stored_facts(self) -> Dict:
        """Get stored user facts"""
        try:
            response = requests.get(f"{self.base_url}/memory/facts")
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}

    def generate_comprehensive_report(self, total_time: float):
        """Generate comprehensive test report"""
        
        print("\n" + "=" * 60)
        print("🧠 MEMORY-OPTIMIZED SYSTEM TEST RESULTS")
        print("=" * 60)
        
        # Basic statistics
        total_messages = len(self.test_results)
        successful_messages = len([r for r in self.test_results if r['priya_responses']])
        avg_response_time = sum([r['response_time'] for r in self.test_results]) / len(self.test_results)
        
        print(f"📊 PERFORMANCE METRICS:")
        print(f"   Total messages: {total_messages}")
        print(f"   Successful responses: {successful_messages}/{total_messages} ({successful_messages/total_messages*100:.1f}%)")
        print(f"   Average response time: {avg_response_time:.2f}s")
        print(f"   Total test time: {total_time:.2f}s")
        
        # Memory health evolution
        memory_healths = [r['memory_health'] for r in self.test_results if 'memory_health' in r]
        if memory_healths:
            print(f"\n🧠 MEMORY HEALTH EVOLUTION:")
            print(f"   Initial health: {memory_healths[0]:.2f}")
            print(f"   Final health: {memory_healths[-1]:.2f}")
            print(f"   Average health: {sum(memory_healths)/len(memory_healths):.2f}")
            print(f"   Health improvement: {memory_healths[-1] - memory_healths[0]:+.2f}")
        
        # Memory retention analysis
        memory_test_messages = [4, 8, 9, 11, 13]  # Messages that test memory
        retention_scores = []
        
        for msg_num in memory_test_messages:
            if msg_num <= len(self.test_results):
                result = self.test_results[msg_num - 1]
                responses = result['priya_responses']
                memories_found = self.analyze_memory_retention(msg_num, result['user_message'], responses)
                retention_score = len(memories_found) / 6  # 6 categories total
                retention_scores.append(retention_score)
        
        if retention_scores:
            avg_retention = sum(retention_scores) / len(retention_scores)
            print(f"\n🎯 MEMORY RETENTION ANALYSIS:")
            print(f"   Average retention score: {avg_retention:.2f} ({avg_retention*100:.1f}%)")
            print(f"   Memory test results: {[f'{s:.2f}' for s in retention_scores]}")
        
        # Conversation stage progression
        stages = [r['conversation_stage'] for r in self.test_results if 'conversation_stage' in r]
        unique_stages = list(set(stages))
        print(f"\n📈 CONVERSATION STAGE PROGRESSION:")
        print(f"   Stages detected: {unique_stages}")
        print(f"   Stage transitions: {len(unique_stages)} different stages")
        
        # Get final memory status
        memory_status = self.get_memory_status()
        if memory_status:
            print(f"\n📋 FINAL MEMORY STATUS:")
            print(f"   Session ID: {memory_status.get('session_id', 'unknown')}")
            print(f"   Message count: {memory_status.get('message_count', 0)}")
            print(f"   Current stage: {memory_status.get('conversation_stage', 'unknown')}")
            
            health_metrics = memory_status.get('memory_health', {})
            if health_metrics:
                print(f"   Overall health: {health_metrics.get('overall_health', 0):.2f}")
                print(f"   Retention score: {health_metrics.get('retention_score', 0):.2f}")
                print(f"   Consistency score: {health_metrics.get('consistency_score', 0):.2f}")
                print(f"   Learning velocity: {health_metrics.get('learning_velocity', 0):.2f}")
        
        # Get stored facts
        facts_data = self.get_stored_facts()
        if facts_data:
            facts = facts_data.get('facts', [])
            print(f"\n📚 STORED FACTS SUMMARY:")
            print(f"   Total facts stored: {len(facts)}")
            
            # Group by category
            categories = {}
            for fact in facts:
                cat = fact.get('category', 'unknown')
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(fact)
            
            for category, cat_facts in categories.items():
                avg_confidence = sum([f['confidence'] for f in cat_facts]) / len(cat_facts)
                print(f"   {category}: {len(cat_facts)} facts (avg confidence: {avg_confidence:.2f})")
            
            # Show high-confidence facts
            high_conf_facts = [f for f in facts if f['confidence'] > 0.8]
            print(f"\n�� HIGH-CONFIDENCE FACTS ({len(high_conf_facts)}):")
            for fact in high_conf_facts[:10]:  # Show top 10
                print(f"   {fact['key_phrase']}: {fact['value']} (confidence: {fact['confidence']:.2f})")
        
        # Performance assessment
        print(f"\n🏆 OVERALL ASSESSMENT:")
        
        # Success criteria
        criteria = {
            "Response success rate": (successful_messages / total_messages) >= 0.95,
            "Average response time": avg_response_time <= 7.0,
            "Memory retention": avg_retention >= 0.6 if retention_scores else False,
            "Memory health": memory_healths[-1] >= 0.6 if memory_healths else False
        }
        
        passed_criteria = sum(criteria.values())
        total_criteria = len(criteria)
        
        for criterion, passed in criteria.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {criterion}: {status}")
        
        print(f"\n🎯 FINAL SCORE: {passed_criteria}/{total_criteria} ({passed_criteria/total_criteria*100:.1f}%)")
        
        if passed_criteria == total_criteria:
            print("🏆 EXCELLENT! All optimization criteria met!")
        elif passed_criteria >= total_criteria * 0.75:
            print("✅ GOOD! Most optimization criteria met!")
        else:
            print("⚠️  NEEDS IMPROVEMENT: Some optimization criteria not met")
        
        print("=" * 60)

if __name__ == "__main__":
    print("🚀 Starting Memory-Optimized System Test...")
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(3)
    
    # Run test
    tester = MemoryOptimizedTester()
    tester.run_comprehensive_test()
    
    print("\n✅ Memory-optimized system test completed!")
