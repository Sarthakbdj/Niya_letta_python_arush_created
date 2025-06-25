#!/usr/bin/env python3
"""
Niya-Python Bridge with Conversation Memory
Combines aggressive reset strategy with persistent conversation memory
"""

import os
import time
import re
import json
import logging
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from letta_client import Letta
from enhanced_personality import ENHANCED_MEMORY_BLOCKS
from conversation_memory import ConversationMemory

# ULTRA-FAST logging: Error-only
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class NiyaBridgeWithMemory:
    def __init__(self):
        self.flask_app = Flask(__name__)
        CORS(self.flask_app)
        
        # Configuration
        self.base_url = os.getenv('LETTA_BASE_URL', 'http://localhost:8283')
        self.letta_client = None
        self.agent_id = None
        
        # Aggressive reset settings
        self.request_spacing = 0.1
        self.last_request_time = 0
        self.message_count = 0
        self.max_messages_before_reset = 4
        self.last_reset_time = time.time()
        self.agent_timeout = 10
        
        # Health tracking
        self.consecutive_failures = 0
        self.max_consecutive_failures = 2
        
        # NEW: Conversation Memory System
        self.memory = ConversationMemory()
        self.current_session_id = None
        
        self.setup_routes()

    def setup_routes(self):
        @self.flask_app.route('/message', methods=['POST'])
        def handle_message():
            try:
                data = request.get_json()
                user_message = data.get('message', '').strip()
                session_id = data.get('session_id', None)
                
                # Initialize session if needed
                if not session_id:
                    session_id = self.memory.start_session()
                    self.current_session_id = session_id
                elif session_id != self.current_session_id:
                    # New session - reset everything
                    self.current_session_id = session_id
                    self.message_count = 0
                    self.consecutive_failures = 0
                
                if not user_message:
                    return jsonify({
                        "messages": ["Hey jaan! What's on your mind? 💕"],
                        "total_messages": 1,
                        "success": True,
                        "session_id": session_id,
                        "error": None,
                        "is_multi_message": False
                    })
                
                # AGGRESSIVE AGENT MANAGEMENT with Memory Context
                self.message_count += 1
                should_reset = (
                    self.message_count >= self.max_messages_before_reset or
                    self.consecutive_failures >= self.max_consecutive_failures or
                    (time.time() - self.last_reset_time) > 120
                )
                
                if should_reset:
                    logger.error(f"🔄 MEMORY-AWARE reset: msg_count={self.message_count}")
                    self.create_agent_with_memory(session_id)
                    self.message_count = 0
                    self.consecutive_failures = 0
                    self.last_reset_time = time.time()
                
                # Get response with memory context
                raw_response = self.get_priya_response_with_timeout(user_message)
                
                if raw_response is None:
                    logger.error("🚨 Timeout - forcing reset with memory")
                    self.create_agent_with_memory(session_id)
                    self.message_count = 0
                    self.consecutive_failures = 0
                    raw_response = "Sorry jaan, I had a brief moment there! 💔 What were you saying?"
                
                # Process response
                cleaned_response = self._deep_clean_response(raw_response)
                messages = self._break_into_natural_messages(cleaned_response)
                
                # Store in conversation memory
                self.memory.add_message(
                    session_id, 
                    self.message_count, 
                    user_message, 
                    ' '.join(messages)
                )
                
                # Success - reset failure counter
                self.consecutive_failures = 0
                
                return jsonify({
                    "messages": messages,
                    "total_messages": len(messages),
                    "success": True,
                    "session_id": session_id,
                    "error": None,
                    "is_multi_message": len(messages) > 1,
                    "agent_message_count": self.message_count,
                    "agent_age_seconds": int(time.time() - self.last_reset_time),
                    "memory_enabled": True
                })
                
            except Exception as e:
                self.consecutive_failures += 1
                logger.error(f"❌ Error in handle_message: {e}")
                return jsonify({
                    "messages": ["Sorry jaan, technical issue! 💔 Let me try again..."],
                    "total_messages": 1,
                    "success": True,
                    "session_id": session_id,
                    "error": str(e),
                    "is_multi_message": False
                }), 500

        @self.flask_app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({
                "status": "healthy",
                "service": "Niya-Python Bridge - WITH MEMORY",
                "agent_id": self.agent_id,
                "letta_connected": bool(self.letta_client),
                "message_count": self.message_count,
                "consecutive_failures": self.consecutive_failures,
                "agent_age_seconds": int(time.time() - self.last_reset_time),
                "current_session": self.current_session_id,
                "memory_system": "enabled",
                "optimizations": {
                    "request_spacing": "0.1s",
                    "aggressive_reset": f"every_{self.max_messages_before_reset}_messages",
                    "timeout_protection": f"{self.agent_timeout}s",
                    "conversation_memory": "sqlite_database",
                    "context_injection": "enabled"
                }
            })

        @self.flask_app.route('/memory/summary/<session_id>', methods=['GET'])
        def get_memory_summary(session_id):
            """Get conversation memory summary"""
            try:
                summary = self.memory.get_conversation_summary(session_id)
                return jsonify({
                    "session_id": session_id,
                    "summary": summary,
                    "success": True
                })
            except Exception as e:
                return jsonify({"error": str(e), "success": False}), 500

        @self.flask_app.route('/reset', methods=['POST'])
        def reset_agent():
            try:
                data = request.get_json() or {}
                session_id = data.get('session_id', self.current_session_id)
                
                self.create_agent_with_memory(session_id)
                self.message_count = 0
                self.consecutive_failures = 0
                self.last_reset_time = time.time()
                
                return jsonify({
                    "message": "Agent reset with memory context",
                    "agent_id": self.agent_id,
                    "session_id": session_id,
                    "success": True
                })
            except Exception as e:
                return jsonify({"error": str(e), "success": False}), 500

    def initialize(self):
        """Initialize system"""
        try:
            self.letta_client = Letta(base_url=self.base_url)
            self.cleanup_agents()
            
            # Start with fresh session
            self.current_session_id = self.memory.start_session()
            self.create_agent_with_memory(self.current_session_id)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize: {e}")
            return False

    def create_agent_with_memory(self, session_id: str):
        """Create agent with conversation memory context"""
        try:
            # Clean up old agent
            if self.agent_id:
                try:
                    self.letta_client.agents.delete(self.agent_id)
                except:
                    pass
            
            # Get conversation context from memory
            context_prompt = self.memory.generate_context_prompt(session_id)
            
            # Enhanced memory blocks with conversation context
            memory_blocks = ENHANCED_MEMORY_BLOCKS[:1].copy()  # Base personality
            
            # Add conversation context as additional memory
            if context_prompt and "Total messages: 0" not in context_prompt:
                memory_blocks.append({
                    "label": "conversation_context",
                    "value": context_prompt
                })
            
            agent = self.letta_client.agents.create(
                name=f"priya_memory_{int(time.time())}",
                memory_blocks=memory_blocks,
                model="openai/gpt-4o-mini",
                embedding="openai/text-embedding-3-small",
                tools=[]
            )
            
            self.agent_id = agent.id
            logger.error(f"✅ Created memory-aware agent: {self.agent_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to create agent with memory: {e}")
            raise

    def get_priya_response_with_timeout(self, message: str) -> str:
        """Get response with timeout protection"""
        result = [None]
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
            logger.error(f"⏰ Agent call timed out after {self.agent_timeout}s")
            return None
        
        if exception[0]:
            logger.error(f"❌ Exception in agent call: {exception[0]}")
            return None
            
        return result[0]
    
    def get_priya_response(self, message: str) -> str:
        """Get response from agent"""
        try:
            if not self.agent_id:
                self.create_agent_with_memory(self.current_session_id)
            
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            
            if time_since_last < self.request_spacing:
                time.sleep(self.request_spacing - time_since_last)
            
            self.last_request_time = time.time()
            
            response = self.letta_client.agents.messages.create(
                agent_id=self.agent_id,
                messages=[{"role": "user", "content": message}]
            )
            
            return self._extract_response(response)
                        
        except Exception as e:
            logger.error(f"❌ Error in get_priya_response: {e}")
            raise e
    
    def _extract_response(self, response) -> str:
        """Extract response from Letta"""
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
        """Clean response to fix corruption"""
        if not raw_response:
            return "Hey jaan! 💕"
        
        try:
            # Remove excessive whitespace
            cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', raw_response)
            cleaned = re.sub(r'\s{3,}', ' ', cleaned)
            
            # Remove trailing whitespace lines
            lines = cleaned.split('\n')
            lines = [line.rstrip() for line in lines if line.strip()]
            cleaned = '\n'.join(lines)
            
            # Fix JSON artifacts
            cleaned = re.sub(r'["\{\}]+$', '', cleaned)
            cleaned = re.sub(r'^["\{\}]+', '', cleaned)
            
            # Length limit
            if len(cleaned) > 1000:
                sentences = re.split(r'[.!?]+\s+', cleaned[:1000])
                cleaned = '. '.join(sentences[:-1]) + '.'
            
            # Fallback
            if len(cleaned.strip()) < 5 or not re.search(r'[a-zA-Z]', cleaned):
                return "Hey jaan! 💕 What's on your mind? ✨"
            
            return cleaned.strip()
            
        except Exception as e:
            logger.error(f"❌ Error in _deep_clean_response: {e}")
            return "Hey jaan! 💕 I'm here for you! ✨"
    
    def _break_into_natural_messages(self, long_message: str) -> list:
        """Break into max 3 natural messages"""
        if not long_message or len(long_message) < 60:
            return [long_message] if long_message else ["Hey! 😊"]
            
        sentences = re.split(r'[.!?]+\s+', long_message.strip())
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= 3:
            return [s + '.' if not s.endswith(('.', '!', '?')) else s for s in sentences]
        
        third = len(sentences) // 3
        messages = [
            '. '.join(sentences[:third]) + '.',
            '. '.join(sentences[third:third*2]) + '.',
            '. '.join(sentences[third*2:]) + '.'
        ]
        
        return [msg for msg in messages if msg.strip()][:3]
    
    def cleanup_agents(self):
        """Clean up old agents"""
        try:
            agents = self.letta_client.agents.list()
            for agent in agents:
                try:
                    self.letta_client.agents.delete(agent.id)
                except:
                    pass
        except:
            pass
        
    def run(self, host='localhost', port=1511):
        """Run the bridge service"""
        self.flask_app.run(
            host=host, 
            port=port, 
            debug=False, 
            threaded=True,
            use_reloader=False,
            use_debugger=False
        )

# Global bridge instance
bridge = NiyaBridgeWithMemory()

def main():
    """Main entry point"""
    try:
        print("🚀" * 30)
        print("⚡ NIYA-PYTHON BRIDGE WITH MEMORY")
        print("🧠 CONVERSATION MEMORY + AGGRESSIVE RESET")
        print("🚀" * 30)
        
        if not bridge.initialize():
            print("❌ Failed to initialize")
            return
        
        print("✅ Memory-Enhanced Bridge initialized!")
        print("🔗 Backend endpoint: http://localhost:1511")
        print("🧠 MEMORY FEATURES:")
        print("   • SQLite conversation database")
        print("   • Context injection on agent reset")
        print("   • Relationship insights tracking")
        print("   • Topic and sentiment analysis")
        print("   • Automatic session management")
        print("⚡ PERFORMANCE FEATURES:")
        print("   • Aggressive reset: Every 4 messages")
        print("   • Timeout protection: 10 seconds")
        print("   • Deep message cleaning: ENABLED")
        print("🛑 Press Ctrl+C to stop")
        
        bridge.run()
        
    except KeyboardInterrupt:
        print("\n⚡ Memory-Enhanced Bridge shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
