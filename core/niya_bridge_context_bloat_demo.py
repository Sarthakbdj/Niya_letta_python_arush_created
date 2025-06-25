#!/usr/bin/env python3
"""
Niya-Python Bridge Service - ULTRA FAST LOCAL OPTIMIZED
Maximum speed configuration for local Letta server
Expected by NestJS backend on port 1511
"""

import json
import logging
from typing import Dict, Any
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import re
import os
import signal
from letta_client import Letta
from dotenv import load_dotenv
from enhanced_personality import ENHANCED_PERSONA, ENHANCED_MEMORY_BLOCKS
import threading

# Load environment
load_dotenv()

# Configure minimal logging for maximum speed
logging.basicConfig(level=logging.ERROR)  # Only errors, no info/debug
logger = logging.getLogger(__name__)

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Request timed out")

class NiyaBridge:
    """Ultra-fast bridge service for LOCAL Letta server"""
    
    def __init__(self):
        self.flask_app = Flask(__name__)
        CORS(self.flask_app)
        
        # ULTRA-FAST LOCAL CONFIGURATION
        self.base_url = os.getenv('LETTA_BASE_URL', 'http://localhost:8283')
        self.letta_client = None
        self.agent_id = None
        
        # ULTRA-FAST timings for LOCAL
        self.request_spacing = 0.1  # 10x faster for local
        self.last_request_time = 0
        
        # CONTEXT BLOAT DEMO: NO reset management - let context grow
        self.message_count = 0
        self.start_time = time.time()
        # NO reset logic - agent will accumulate context until failure
        
        self.setup_routes()

    def setup_routes(self):
        """Setup Flask routes with minimal overhead"""
        
        @self.flask_app.route('/message', methods=['POST'])
        def handle_message():
            try:
                data = request.get_json()
                user_message = data.get('message', '').strip()
                
                if not user_message:
                    return jsonify({
                        "messages": ["Hey jaan! What's on your mind? 💕"],
                        "total_messages": 1,
                        "success": True,
                        "error": None,
                        "is_multi_message": False
                    })
                
                # CONTEXT BLOAT DEMO - NO reset management, just count messages
                self.message_count += 1
                
                # Get response WITHOUT timeout protection or resets
                raw_response = self.get_priya_response(user_message)
                
                # ENHANCED MESSAGE CLEANING - Fix corruption
                cleaned_response = self._deep_clean_response(raw_response)
                messages = self._break_into_natural_messages(cleaned_response)
                
                return jsonify({
                    "messages": messages,
                    "total_messages": len(messages),
                    "success": True,
                    "error": None,
                    "is_multi_message": len(messages) > 1,
                    "message_count": self.message_count,
                    "uptime_seconds": int(time.time() - self.start_time)
                })
                
            except Exception as e:
                logger.error(f"❌ Error in handle_message: {e}")
                return jsonify({
                    "messages": [f"Error: {str(e)}"],
                    "total_messages": 1,
                    "success": False,
                    "error": str(e),
                    "message_count": self.message_count
                }), 500

        @self.flask_app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({
                "status": "healthy",
                "service": "Niya-Python Bridge - CONTEXT BLOAT DEMO",
                "agent_id": self.agent_id,
                "letta_connected": bool(self.letta_client),
                "message_count": self.message_count,
                "uptime_seconds": int(time.time() - self.start_time),
                "optimizations": "NONE - Raw Letta behavior for context bloat demo",
                "context_management": "NONE - Let context grow until failure",
                "reset_strategy": "NONE - Agent never resets"
            })

        @self.flask_app.route('/reset', methods=['POST'])
        def reset_agent():
            try:
                old_agent = self.agent_id
                self.create_agent()
                self.message_count = 0
                return jsonify({
                    "message": "Agent reset manually for demo",
                    "old_agent_id": old_agent,
                    "new_agent_id": self.agent_id,
                    "success": True
                })
            except Exception as e:
                return jsonify({"error": str(e), "success": False}), 500

    def initialize(self):
        """Initialize LOCAL Letta client - ULTRA FAST"""
        try:
            # Initialize LOCAL Letta client
            self.letta_client = Letta(base_url=self.base_url)
            
            # Clean up and create agent
            self.cleanup_agents()
            self.create_agent()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize: {e}")
            return False

    def create_agent(self):
        """Create ULTRA-FAST Priya agent for LOCAL server"""
        try:
            # Clean up old agent first
            if self.agent_id:
                try:
                    self.letta_client.agents.delete(self.agent_id)
                except:
                    pass
            
            # ULTRA-FAST CONFIGURATION: Minimal everything
            minimal_memory_blocks = ENHANCED_MEMORY_BLOCKS[:1]  # Only 1 block!
            
            agent = self.letta_client.agents.create(
                name=f"priya_aggressive_{int(time.time())}",
                memory_blocks=minimal_memory_blocks,
                model="openai/gpt-4o-mini",  # Fastest model
                embedding="openai/text-embedding-3-small",  # Required format
                tools=[]  # No tools for maximum speed
            )
            
            self.agent_id = agent.id
            logger.error(f"✅ Created fresh agent: {self.agent_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to create agent: {e}")
            raise
    
    def get_priya_response_with_timeout(self, message: str) -> str:
        """Get response with aggressive timeout protection"""
        result = [None]  # Use list to allow modification in nested function
        exception = [None]
        
        def target():
            try:
                result[0] = self.get_priya_response(message)
            except Exception as e:
                exception[0] = e
        
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        thread.join(timeout=self.agent_timeout)
        
        if thread.is_alive():
            # Thread is still running - timeout occurred
            logger.error(f"⏰ Agent call timed out after {self.agent_timeout}s")
            return None
        
        if exception[0]:
            logger.error(f"❌ Exception in agent call: {exception[0]}")
            return None
            
        return result[0]
    
    def get_priya_response(self, message: str) -> str:
        """Get response - ULTRA FAST LOCAL"""
        try:
            if not self.agent_id:
                self.create_agent()
            
            # ULTRA-FAST: Minimal request spacing for LOCAL (0.1s)
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            
            if time_since_last < self.request_spacing:
                time.sleep(self.request_spacing - time_since_last)
            
            self.last_request_time = time.time()
            
            # LOCAL SERVER: Single attempt with timeout protection
            response = self.letta_client.agents.messages.create(
                agent_id=self.agent_id,
                messages=[{"role": "user", "content": message}]
            )
            
            return self._extract_response(response)
                        
        except Exception as e:
            logger.error(f"❌ Error in get_priya_response: {e}")
            raise e
    
    def _extract_response(self, response) -> str:
        """Extract response - ULTRA FAST"""
        try:
            for msg in response.messages:
                if hasattr(msg, 'message_type') and msg.message_type == "assistant_message":
                    return msg.content
                elif hasattr(msg, 'role') and msg.role == "assistant":
                    return msg.content
            return "Hey jaan! 💕 I'm here for you! ✨"
        except:
            return "Hey! 😊"
    
    def _deep_clean_response(self, raw_response: str) -> str:
        """ENHANCED: Deep clean response to fix Letta corruption issues"""
        if not raw_response:
            return "Hey jaan! 💕"
        
        try:
            # Step 1: Remove excessive whitespace (the main issue)
            cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', raw_response)  # Collapse multiple newlines
            cleaned = re.sub(r'\s{3,}', ' ', cleaned)  # Collapse multiple spaces
            
            # Step 2: Remove trailing whitespace lines
            lines = cleaned.split('\n')
            lines = [line.rstrip() for line in lines if line.strip()]
            cleaned = '\n'.join(lines)
            
            # Step 3: Fix JSON-like corruption
            cleaned = re.sub(r'["\{\}]+$', '', cleaned)  # Remove trailing JSON artifacts
            cleaned = re.sub(r'^["\{\}]+', '', cleaned)  # Remove leading JSON artifacts
            
            # Step 4: Ensure reasonable length (prevent bloat)
            if len(cleaned) > 1000:  # Truncate if too long
                sentences = re.split(r'[.!?]+\s+', cleaned[:1000])
                cleaned = '. '.join(sentences[:-1]) + '.'
            
            # Step 5: Fallback if still corrupted
            if len(cleaned.strip()) < 5 or not re.search(r'[a-zA-Z]', cleaned):
                return "Hey jaan! 💕 What's on your mind? ✨"
            
            return cleaned.strip()
            
        except Exception as e:
            logger.error(f"❌ Error in _deep_clean_response: {e}")
            return "Hey jaan! 💕 I'm here for you! ✨"
    
    def _break_into_natural_messages(self, long_message: str) -> list:
        """Break into MAX 3 natural messages - ULTRA FAST"""
        if not long_message or len(long_message) < 60:
            return [long_message] if long_message else ["Hey! 😊"]
            
        # Quick split on sentences - max 3 parts
        sentences = re.split(r'[.!?]+\s+', long_message.strip())
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= 3:
            return [s + '.' if not s.endswith(('.', '!', '?')) else s for s in sentences]
        
        # Group into 3 messages
        third = len(sentences) // 3
        messages = [
            '. '.join(sentences[:third]) + '.',
            '. '.join(sentences[third:third*2]) + '.',
            '. '.join(sentences[third*2:]) + '.'
        ]
        
        return [msg for msg in messages if msg.strip()][:3]
    
    def cleanup_agents(self):
        """Quick cleanup"""
        try:
            agents = self.letta_client.agents.list()
            for agent in agents:
                try:
                    self.letta_client.agents.delete(agent.id)
                except:
                    pass
        except:
            pass
        
    def run(self, host='localhost', port=1513):
        """Run CONTEXT BLOAT DEMO bridge service"""
        logger.error(f"🌉 Starting CONTEXT BLOAT DEMO Bridge on {host}:{port}")
        logger.error("⚠️  NO OPTIMIZATIONS - Raw Letta behavior")
        logger.error("⚠️  NO RESETS - Context will grow until failure")
        # Basic Flask configuration
        self.flask_app.run(
            host=host, 
            port=port, 
            debug=False, 
            threaded=True
        )

# Global bridge instance
bridge = NiyaBridge()

def main():
    """CONTEXT BLOAT DEMO main entry point"""
    try:
        print("🔬" * 30)
        print("🔬 CONTEXT BLOAT DEMO - Niya Bridge")
        print("⚠️  NO OPTIMIZATIONS - RAW LETTA BEHAVIOR")
        print("🔬" * 30)
        
        if not bridge.initialize():
            print("❌ Failed to initialize")
            return
        
        print("✅ Context Bloat Demo Bridge initialized!")
        print("🔗 Demo endpoint: http://localhost:1513")
        print("⚠️  DEMO CONFIGURATION:")
        print("   • NO request spacing limits")
        print("   • NO memory management")
        print("   • NO agent resets") 
        print("   • NO timeout protection")
        print("   • NO context limiting")
        print("   • Expected to FAIL after 4-5 messages")
        print("🛑 Press Ctrl+C to stop")
        
        bridge.run()
        
    except KeyboardInterrupt:
        print("\n🔬 Context Bloat Demo shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
