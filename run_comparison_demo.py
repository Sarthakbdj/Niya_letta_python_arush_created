#!/usr/bin/env python3
"""
Comparison Demo - Run both baseline and optimized bridges to show the difference
"""

import subprocess
import time
import requests
import json
import threading
from typing import Optional

class ComparisonDemo:
    def __init__(self):
        self.baseline_process: Optional[subprocess.Popen] = None
        self.optimized_process: Optional[subprocess.Popen] = None
        self.baseline_port = 1512
        self.optimized_port = 1511
    
    def start_baseline_server(self):
        """Start the baseline server"""
        print("🔬 Starting baseline server (no optimizations)...")
        try:
            self.baseline_process = subprocess.Popen(
                ["python", "core/niya_bridge_baseline.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            time.sleep(3)  # Give it time to start
            print("✅ Baseline server started on port 1512")
        except Exception as e:
            print(f"❌ Failed to start baseline server: {e}")
    
    def start_optimized_server(self):
        """Start the optimized server"""
        print("⚡ Starting optimized server (with resets)...")
        try:
            self.optimized_process = subprocess.Popen(
                ["python", "core/niya_bridge_ultra_fast.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            time.sleep(3)  # Give it time to start
            print("✅ Optimized server started on port 1511")
        except Exception as e:
            print(f"❌ Failed to start optimized server: {e}")
    
    def check_server_health(self, port: int, name: str) -> bool:
        """Check if server is responding"""
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ {name} server is healthy")
                return True
            else:
                print(f"❌ {name} server health check failed")
                return False
        except Exception as e:
            print(f"❌ {name} server not responding: {e}")
            return False
    
    def send_test_message(self, port: int, message: str, server_name: str):
        """Send a test message and show response"""
        try:
            print(f"\n📨 Sending to {server_name}: {message}")
            response = requests.post(
                f"http://localhost:{port}/message",
                json={"message": message},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                messages = data.get("messages", [])
                success = data.get("success", False)
                message_count = data.get("message_count", 0)
                
                if success:
                    print(f"✅ {server_name} (msg #{message_count}): {messages[0][:100]}{'...' if len(messages[0]) > 100 else ''}")
                else:
                    print(f"❌ {server_name} failed: {messages[0] if messages else 'No response'}")
                    
                return success
            else:
                print(f"❌ {server_name} HTTP error: {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            print(f"⏰ {server_name} timeout (>15s)")
            return False
        except Exception as e:
            print(f"❌ {server_name} error: {e}")
            return False
    
    def run_demo_conversation(self):
        """Run a demo conversation to show the difference"""
        print("\n🎭 DEMO CONVERSATION - Context Bloat Test")
        print("=" * 80)
        
        # Test messages designed to trigger context bloat
        test_messages = [
            "Hi! I'm Sarah, a software engineer at Google.",
            "I love Python programming and have been coding for 5 years.",
            "I also enjoy rock climbing on weekends.",
            "My favorite food is Indian curry, especially butter chicken.",
            "I have a pet cat named Whiskers who loves to sleep on my keyboard.",
            "What's my name and what do I do for work?",  # Memory test
            "Tell me about my hobbies and interests.",  # Memory test
            "I'm feeling stressed about a work deadline.",
            "Can you remind me what my pet's name is?"  # Memory test
        ]
        
        baseline_failures = 0
        optimized_failures = 0
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n🔄 Round {i}")
            print("-" * 40)
            
            # Test baseline
            baseline_success = self.send_test_message(self.baseline_port, message, "Baseline")
            if not baseline_success:
                baseline_failures += 1
            
            # Test optimized
            optimized_success = self.send_test_message(self.optimized_port, message, "Optimized")
            if not optimized_success:
                optimized_failures += 1
            
            # Check if baseline failed but optimized succeeded
            if not baseline_success and optimized_success:
                print(f"🎯 DIFFERENCE DETECTED: Baseline failed, Optimized succeeded at message {i}")
            
            time.sleep(1)  # Small delay between rounds
        
        print(f"\n📊 FINAL RESULTS")
        print("=" * 40)
        print(f"Baseline failures:  {baseline_failures}/{len(test_messages)}")
        print(f"Optimized failures: {optimized_failures}/{len(test_messages)}")
        
        if baseline_failures > optimized_failures:
            print("✅ Optimized bridge showed better reliability!")
        elif baseline_failures == optimized_failures == 0:
            print("🤔 Both performed well - may need more aggressive testing")
        else:
            print("🤔 Results inconclusive - check server configurations")
    
    def stop_servers(self):
        """Stop both servers"""
        print("\n🛑 Stopping servers...")
        
        if self.baseline_process:
            self.baseline_process.terminate()
            self.baseline_process.wait()
            print("✅ Baseline server stopped")
        
        if self.optimized_process:
            self.optimized_process.terminate()
            self.optimized_process.wait()
            print("✅ Optimized server stopped")
    
    def run_demo(self):
        """Run the complete demo"""
        try:
            print("🚀 CONTEXT BLOAT COMPARISON DEMO")
            print("=" * 80)
            print("This demo will:")
            print("• Start both baseline and optimized bridges")
            print("• Send test messages to both")
            print("• Show where context bloat causes failures")
            print("• Demonstrate the effectiveness of optimizations")
            print()
            
            # Start servers
            print("🔧 Starting servers...")
            self.start_baseline_server()
            self.start_optimized_server()
            
            # Wait for startup
            print("⏳ Waiting for servers to initialize...")
            time.sleep(5)
            
            # Check health
            baseline_healthy = self.check_server_health(self.baseline_port, "Baseline")
            optimized_healthy = self.check_server_health(self.optimized_port, "Optimized")
            
            if not baseline_healthy or not optimized_healthy:
                print("❌ One or both servers failed to start properly")
                print("Please check the server logs and try again")
                return
            
            # Run demo conversation
            self.run_demo_conversation()
            
            print("\n🎯 Demo completed! Key observations:")
            print("• Baseline should fail after 4-5 messages due to context bloat")
            print("• Optimized should continue working with aggressive resets")
            print("• Memory retention may be different between approaches")
            
        except KeyboardInterrupt:
            print("\n⚠️  Demo interrupted by user")
        except Exception as e:
            print(f"\n❌ Demo error: {e}")
        finally:
            self.stop_servers()

def main():
    """Main demo runner"""
    demo = ComparisonDemo()
    
    print("⚠️  IMPORTANT: Make sure Letta server is running on localhost:8283")
    print("   If not, start it with: docker run -p 8283:8283 letta/letta:latest")
    print()
    
    input("Press Enter to start the demo...")
    
    demo.run_demo()

if __name__ == "__main__":
    main() 