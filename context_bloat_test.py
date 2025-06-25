#!/usr/bin/env python3
"""
Context Bloat Test - Demonstrates Letta context retention issues
Tests both baseline (no optimizations) and optimized versions
"""

import requests
import time
import json
import threading
from typing import Dict, List, Tuple
import concurrent.futures

class ContextBloatTester:
    def __init__(self):
        self.baseline_url = "http://localhost:1512"  # Baseline bridge
        self.optimized_url = "http://localhost:1511"  # Optimized bridge
        self.test_messages = [
            "Hi! I'm Sarah and I work as a software engineer at Google.",
            "I love Python programming and I've been coding for 5 years.",
            "I also enjoy rock climbing on weekends. Do you know any good spots?",
            "My favorite food is Indian curry, especially butter chicken.",
            "I have a pet cat named Whiskers who loves to sleep on my keyboard.",
            "What's my name and what do I do for work?",  # Memory test
            "What's my favorite hobby?",  # Memory test
            "Tell me about my pet.",  # Memory test
            "I'm feeling stressed about a work deadline tomorrow.",
            "Can you remind me what programming language I prefer?",  # Memory test
            "I'm thinking of trying a new Indian restaurant tonight.",
            "Do you remember what I said about weekends?",  # Memory test
            "My manager just gave me a new project using React.",
            "Whiskers just knocked over my coffee again!",
            "What programming languages have I mentioned in our conversation?",  # Complex memory test
        ]
    
    def test_server_health(self, url: str, server_name: str) -> bool:
        """Check if server is healthy"""
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {server_name} is healthy: {data.get('service', 'Unknown')}")
                return True
            else:
                print(f"❌ {server_name} health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ {server_name} not accessible: {e}")
            return False
    
    def send_message(self, url: str, message: str, timeout: int = 30) -> Dict:
        """Send message to bridge and return response with timing"""
        start_time = time.time()
        try:
            response = requests.post(
                f"{url}/message",
                json={"message": message},
                timeout=timeout
            )
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "data": data,
                    "response_time": end_time - start_time,
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "data": None,
                    "response_time": end_time - start_time,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "data": None,
                "response_time": timeout,
                "error": f"Timeout after {timeout}s"
            }
        except Exception as e:
            end_time = time.time()
            return {
                "success": False,
                "data": None,
                "response_time": end_time - start_time,
                "error": str(e)
            }
    
    def test_conversation_flow(self, url: str, server_name: str) -> Dict:
        """Test full conversation flow and track failures"""
        print(f"\n🧪 Testing {server_name}")
        print("=" * 60)
        
        results = {
            "server_name": server_name,
            "messages_sent": 0,
            "successful_responses": 0,
            "failed_responses": 0,
            "total_response_time": 0,
            "failure_point": None,
            "memory_retention_score": 0,
            "conversation_log": [],
            "errors": []
        }
        
        memory_tests = [5, 6, 7, 9, 11, 14]  # Message indices that test memory
        memory_correct = 0
        
        for i, message in enumerate(self.test_messages):
            print(f"\n📨 Message {i+1}: {message[:50]}{'...' if len(message) > 50 else ''}")
            
            # Send message
            response = self.send_message(url, message, timeout=30)
            results["messages_sent"] += 1
            results["total_response_time"] += response["response_time"]
            
            # Log conversation
            conversation_entry = {
                "message_num": i + 1,
                "user_message": message,
                "response_time": response["response_time"],
                "success": response["success"]
            }
            
            if response["success"]:
                results["successful_responses"] += 1
                assistant_messages = response["data"].get("messages", [])
                conversation_entry["assistant_response"] = assistant_messages
                conversation_entry["message_count"] = response["data"].get("message_count", 0)
                
                print(f"✅ Response ({response['response_time']:.2f}s): {assistant_messages[0][:100]}{'...' if len(assistant_messages[0]) > 100 else ''}")
                
                # Check memory retention on specific messages
                if i in memory_tests:
                    memory_score = self.evaluate_memory_retention(message, assistant_messages, i)
                    conversation_entry["memory_score"] = memory_score
                    memory_correct += memory_score
                    print(f"🧠 Memory test: {'PASS' if memory_score > 0.5 else 'FAIL'} (score: {memory_score:.2f})")
                
            else:
                results["failed_responses"] += 1
                results["errors"].append({
                    "message_num": i + 1,
                    "error": response["error"],
                    "response_time": response["response_time"]
                })
                conversation_entry["error"] = response["error"]
                
                print(f"❌ FAILED ({response['response_time']:.2f}s): {response['error']}")
                
                # Mark failure point
                if results["failure_point"] is None:
                    results["failure_point"] = i + 1
                    print(f"🚨 FIRST FAILURE at message {i + 1}")
            
            results["conversation_log"].append(conversation_entry)
            
            # Small delay between messages
            time.sleep(0.5)
        
        # Calculate memory retention score
        if len(memory_tests) > 0:
            results["memory_retention_score"] = memory_correct / len(memory_tests)
        
        # Calculate averages
        if results["successful_responses"] > 0:
            results["avg_response_time"] = results["total_response_time"] / results["successful_responses"]
        else:
            results["avg_response_time"] = 0
        
        results["success_rate"] = results["successful_responses"] / results["messages_sent"]
        
        return results
    
    def evaluate_memory_retention(self, question: str, responses: List[str], message_index: int) -> float:
        """Evaluate how well the agent retained memory (simple heuristic)"""
        if not responses:
            return 0.0
        
        response_text = " ".join(responses).lower()
        
        # Memory evaluation based on message content
        if "what's my name" in question.lower():
            return 1.0 if "sarah" in response_text else 0.0
        elif "what do i do for work" in question.lower():
            return 1.0 if any(word in response_text for word in ["software", "engineer", "google", "programming"]) else 0.0
        elif "favorite hobby" in question.lower():
            return 1.0 if any(word in response_text for word in ["rock", "climbing", "climb"]) else 0.0
        elif "tell me about my pet" in question.lower() or "pet" in question.lower():
            return 1.0 if any(word in response_text for word in ["whiskers", "cat", "keyboard"]) else 0.0
        elif "programming language" in question.lower():
            return 1.0 if "python" in response_text else 0.0
        elif "weekends" in question.lower():
            return 1.0 if any(word in response_text for word in ["rock", "climbing", "climb"]) else 0.0
        
        # Generic memory check - if response seems relevant
        return 0.5 if len(response_text) > 10 else 0.0
    
    def print_test_summary(self, baseline_results: Dict, optimized_results: Dict):
        """Print comprehensive test summary"""
        print("\n" + "🔬" * 80)
        print("🔬 CONTEXT BLOAT TEST RESULTS")
        print("🔬" * 80)
        
        print("\n📊 PERFORMANCE COMPARISON")
        print("-" * 60)
        
        # Success rates
        print(f"Success Rate:")
        print(f"  • Baseline:  {baseline_results['success_rate']:.1%} ({baseline_results['successful_responses']}/{baseline_results['messages_sent']})")
        print(f"  • Optimized: {optimized_results['success_rate']:.1%} ({optimized_results['successful_responses']}/{optimized_results['messages_sent']})")
        
        # Response times
        print(f"\nAverage Response Time:")
        print(f"  • Baseline:  {baseline_results['avg_response_time']:.2f}s")
        print(f"  • Optimized: {optimized_results['avg_response_time']:.2f}s")
        
        # Memory retention
        print(f"\nMemory Retention Score:")
        print(f"  • Baseline:  {baseline_results['memory_retention_score']:.1%}")
        print(f"  • Optimized: {optimized_results['memory_retention_score']:.1%}")
        
        # Failure points
        print(f"\nFirst Failure Point:")
        baseline_failure = baseline_results['failure_point'] or "None"
        optimized_failure = optimized_results['failure_point'] or "None"
        print(f"  • Baseline:  Message {baseline_failure}")
        print(f"  • Optimized: Message {optimized_failure}")
        
        print("\n🎯 KEY FINDINGS")
        print("-" * 60)
        
        # Context bloat analysis
        if baseline_results['failure_point'] and baseline_results['failure_point'] <= 5:
            print("✅ CONTEXT BLOAT CONFIRMED: Baseline fails within 5 messages")
        else:
            print("⚠️  Baseline performed better than expected")
        
        # Optimization effectiveness
        improvement = optimized_results['success_rate'] - baseline_results['success_rate']
        if improvement > 0.2:
            print(f"✅ OPTIMIZATIONS EFFECTIVE: {improvement:.1%} improvement in success rate")
        else:
            print("⚠️  Optimizations show minimal improvement")
        
        # Memory retention comparison
        memory_improvement = optimized_results['memory_retention_score'] - baseline_results['memory_retention_score']
        if memory_improvement > 0.2:
            print(f"✅ MEMORY RETENTION IMPROVED: {memory_improvement:.1%} better retention")
        else:
            print("⚠️  Memory retention shows minimal improvement")
        
        print("\n📋 RECOMMENDATIONS")
        print("-" * 60)
        
        if baseline_results['failure_point'] and baseline_results['failure_point'] <= 5:
            print("1. ✅ Use optimized bridge with aggressive resets")
            print("2. ✅ Implement memory consolidation strategies")
            print("3. ✅ Monitor context growth proactively")
        else:
            print("1. 🤔 Investigate why baseline performed better than expected")
            print("2. 🤔 Consider adjusting test scenarios")
            print("3. 🤔 Review Letta server configuration")
    
    def run_comparative_test(self):
        """Run comparative test between baseline and optimized"""
        print("🚀 STARTING CONTEXT BLOAT COMPARATIVE TEST")
        print("=" * 80)
        print("This test will demonstrate:")
        print("• Raw Letta behavior (baseline) vs optimized behavior")
        print("• Context bloat issues and failure points")
        print("• Memory retention capabilities")
        print("• Response time performance")
        print()
        
        # Check server availability
        baseline_healthy = self.test_server_health(self.baseline_url, "Baseline Bridge")
        optimized_healthy = self.test_server_health(self.optimized_url, "Optimized Bridge")
        
        if not baseline_healthy and not optimized_healthy:
            print("❌ Neither server is available. Please start them first:")
            print("   Baseline:  python core/niya_bridge_baseline.py")
            print("   Optimized: python core/niya_bridge_ultra_fast.py")
            return
        
        results = {}
        
        # Test baseline if available
        if baseline_healthy:
            results["baseline"] = self.test_conversation_flow(self.baseline_url, "Baseline (No Optimizations)")
        else:
            print("⚠️  Skipping baseline test - server not available")
            results["baseline"] = {
                "server_name": "Baseline",
                "success_rate": 0.0,
                "avg_response_time": float('inf'),
                "memory_retention_score": 0.0,
                "failure_point": 1
            }
        
        # Test optimized if available
        if optimized_healthy:
            results["optimized"] = self.test_conversation_flow(self.optimized_url, "Optimized (With Resets)")
        else:
            print("⚠️  Skipping optimized test - server not available")
            results["optimized"] = {
                "server_name": "Optimized",
                "success_rate": 0.0,
                "avg_response_time": float('inf'),
                "memory_retention_score": 0.0,
                "failure_point": 1
            }
        
        # Print summary
        if results["baseline"] and results["optimized"]:
            self.print_test_summary(results["baseline"], results["optimized"])
        
        # Save detailed results
        with open(f"context_bloat_test_results_{int(time.time())}.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Detailed results saved to context_bloat_test_results_{int(time.time())}.json")

def main():
    """Main test runner"""
    tester = ContextBloatTester()
    tester.run_comparative_test()

if __name__ == "__main__":
    main() 