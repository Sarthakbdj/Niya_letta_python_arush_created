#!/usr/bin/env python3
"""
Niya-Python Bridge Service - LOCAL LETTA + FIXED MULTI-MESSAGE
Uses existing letta_client with local server configuration
Expected by NestJS backend on port 1511
"""

import json
import logging
from typing import Dict, Any
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import re

from letta_client import Letta
from dotenv import load_dotenv
import os
from core.enhanced_personality import ENHANCED_PERSONA, ENHANCED_MEMORY_BLOCKS

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class NiyaBridge:
    """Bridge service for LOCAL Letta server with speed optimizations"""
    
    def __init__(self):
        self.flask_app = Flask(__name__)
        CORS(self.flask_app)
        
        # LOCAL SERVER CONFIGURATION - Updated for local
        self.base_url = "http://localhost:8283"
        self.letta_client = None
        self.agent_id = None
        
        # SPEED OPTIMIZATIONS FOR LOCAL SERVER
        self.request_spacing = 0.1  # Ultra-fast for local server!
        self.last_request_time = 0
        
        self.setup_routes()

    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.flask_app.route('/message', methods=['POST'])
        def handle_message():
            try:
                data = request.get_json()
                if not data or 'message' not in data:
                    return jsonify({'error': 'Message is required'}), 400
                
                user_message = data['message']
                logger.info(f"📨 Processing message: {user_message[:50]}...")
                
                # Get single response from LOCAL Letta (FAST)
                response = self.get_priya_response(user_message)
                
                # Break into natural messages (LOCAL PROCESSING - NO LETTA PRESSURE)
                messages = self._break_into_natural_messages(response)
                
                # STRICT LIMIT TO MAX 3 MESSAGES (NO MORE SPAM!)
                if len(messages) > 3:
                    messages = messages[:3]
                    # Add continuation hint to last message if needed
                    if messages and not messages[-1].endswith(('...', '😊', '💕', '✨')):
                        messages[-1] += " 😊"
                
                result = {
                    "messages": messages,
                    "total_messages": len(messages),
                    "agent_id": self.agent_id,
                    "response_time": f"{time.time() - self.last_request_time:.2f}s",
                    "server_type": "LOCAL"
                }
                
                logger.info(f"✅ Sent {len(messages)} messages to backend")
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"❌ Error handling message: {e}")
                return jsonify({
                    "messages": ["Sorry jaan, technical issue! 💔 Try again?"],
                    "total_messages": 1,
                    "error": str(e),
                    "server_type": "LOCAL"
                }), 500

        @self.flask_app.route('/health', methods=['GET'])
        def health_check():
            try:
                return jsonify({
                    "status": "healthy",
                    "local_letta_server": "running",
                    "agent_id": self.agent_id,
                    "mode": "LOCAL_SERVER",
                    "base_url": self.base_url
                })
            except Exception as e:
                return jsonify({
                    "status": "unhealthy", 
                    "error": str(e),
                    "mode": "LOCAL_SERVER"
                }), 500

        @self.flask_app.route('/reset', methods=['POST'])
        def reset_agent():
            try:
                old_agent = self.agent_id
                self.create_agent()
                return jsonify({
                    "message": "Agent reset successfully",
                    "old_agent_id": old_agent,
                    "new_agent_id": self.agent_id,
                    "server_type": "LOCAL"
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.flask_app.route('/cleanup', methods=['POST'])
        def cleanup_all_agents():
            try:
                count = self.cleanup_agents()
                self.agent_id = None
                return jsonify({
                    "message": f"Cleaned up {count} agents",
                    "agents_removed": count,
                    "server_type": "LOCAL"
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    def initialize(self):
        """Initialize LOCAL Letta client"""
        try:
            logger.info(f"🔗 Connecting to LOCAL Letta server: {self.base_url}")
            
            # Initialize Letta client for LOCAL server
            self.letta_client = Letta(base_url=self.base_url)
            
            # Clean up any old agents first
            self.cleanup_agents()
            
            # Create new agent
            self.create_agent()
            
            logger.info("✅ LOCAL Letta Bridge initialized successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize LOCAL bridge: {e}")
            return False

    def create_agent(self):
        """Create LOCAL Priya agent - SPEED OPTIMIZED"""
        try:
            logger.info("💖 Creating LOCAL Priya agent...")
            
            # SPEED OPTIMIZATION: Minimal memory blocks for LOCAL server
            agent = self.letta_client.agents.create(
                name="PriyaLocal",
                persona=ENHANCED_PERSONA,
                human="loving boyfriend who adores Priya",
                memory=ENHANCED_MEMORY_BLOCKS[:1],  # Only 1 memory block for max speed
                llm_config={"model": "gpt-4o-mini"},
                embedding_config=None,
                tools=[]
            )
            
            self.agent_id = agent.id
            logger.info(f"💖 Created LOCAL Priya agent: {self.agent_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to create LOCAL Priya agent: {e}")
            raise
    
    def get_priya_response(self, message: str) -> str:
        """Get response from LOCAL Priya agent - MAXIMUM SPEED"""
        try:
            if not self.agent_id:
                self.create_agent()
            
            # SPEED: Minimal request spacing for LOCAL server (0.1s)
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            
            if time_since_last < self.request_spacing:
                wait_time = self.request_spacing - time_since_last
                time.sleep(wait_time)
            
            self.last_request_time = time.time()
            
            # LOCAL SERVER: Send message
            response = self.letta_client.agents.messages.create(
                agent_id=self.agent_id,
                messages=[{"role": "user", "content": message}]
            )
            
            return self._extract_response(response)
                        
        except Exception as e:
            logger.error(f"❌ Error getting LOCAL Priya response: {e}")
            return "Sorry jaan, I'm having some technical difficulties right now... 💔"
    
    def _extract_response(self, response) -> str:
        """Extract Priya's response from LOCAL server"""
        try:
            for msg in response.messages:
                if hasattr(msg, 'message_type') and msg.message_type == "assistant_message":
                    return msg.content
                elif hasattr(msg, 'role') and msg.role == "assistant":
                    return msg.content
            
            return "Hey jaan! 💕 I'm here for you! ✨"
            
        except Exception as e:
            return "Hey! 😊 I'm having a tiny technical moment, what were you saying?"
    
    def _break_into_natural_messages(self, long_message: str) -> list:
        """Break into MAX 3 natural messages - FIXED SPAM ISSUE!"""
        if not long_message:
            return ["Hey! 😊"]
            
        cleaned = long_message.strip()
        
        # If short enough, return as single message
        if len(cleaned) < 60:
            return [cleaned]
        
        # For longer messages, intelligently split into MAX 3 parts
        # Strategy: Split on natural break points but ensure max 3 messages
        
        # Try splitting on sentences first
        sentence_breaks = re.split(r'[.!?]+\s+', cleaned)
        sentence_breaks = [s.strip() for s in sentence_breaks if s.strip()]
        
        if len(sentence_breaks) <= 3:
            # Perfect! Each sentence is a message
            result = []
            for sentence in sentence_breaks:
                if sentence and not sentence.endswith(('.', '!', '?')):
                    sentence += '.'
                result.append(sentence)
            return result[:3]  # Ensure max 3
        
        # Too many sentences - group them into 3 messages
        messages = []
        total_sentences = len(sentence_breaks)
        sentences_per_group = total_sentences // 3
        remainder = total_sentences % 3
        
        start_idx = 0
        for i in range(3):
            # Calculate sentences for this group
            group_size = sentences_per_group + (1 if i < remainder else 0)
            end_idx = start_idx + group_size
            
            # Combine sentences for this message
            group_sentences = sentence_breaks[start_idx:end_idx]
            combined = '. '.join(group_sentences)
            
            if combined and not combined.endswith(('.', '!', '?')):
                combined += '.'
                
            messages.append(combined)
            start_idx = end_idx
        
        # Clean up and ensure max 3
        result = [msg.strip() for msg in messages if msg.strip()]
        return result[:3]
    
    def cleanup_agents(self):
        """Clean up all existing agents on LOCAL server"""
        try:
            if not self.letta_client:
                return 0
                
            logger.info("🧹 Cleaning up LOCAL agents...")
            
            agents = self.letta_client.agents.list()
            logger.info(f"Found {len(agents)} existing LOCAL agents")
            
            cleaned_count = 0
            for agent in agents:
                try:
                    self.letta_client.agents.delete(agent.id)
                    logger.info(f"🗑️ Deleted LOCAL agent: {agent.id}")
                    cleaned_count += 1
                except Exception as e:
                    logger.warning(f"⚠️ Could not delete LOCAL agent {agent.id}: {e}")
            
            logger.info(f"✅ LOCAL agent cleanup completed - removed {cleaned_count} agents")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"❌ Failed to cleanup LOCAL agents: {e}")
            return 0
        
    def run(self, host='localhost', port=1511):
        """Run the LOCAL bridge service"""
        logger.info(f"🌉 Starting LOCAL Niya-Python Bridge on {host}:{port}")
        self.flask_app.run(host=host, port=port, debug=False, threaded=True)

# Global bridge instance
bridge = NiyaBridge()

def main():
    """Main entry point for LOCAL server"""
    try:
        print("🌉" * 30)
        print("🔗 Niya-Python Bridge Service")
        print("⚡ LOCAL LETTA + FIXED MULTI-MESSAGE")
        print("🌉" * 30)
        print()
        
        if not bridge.initialize():
            print("❌ Failed to initialize LOCAL bridge service")
            return
        
        print("✅ LOCAL Bridge initialized successfully!")
        print("🔗 Expected by Niya Backend on: http://localhost:1511")
        print("📡 Main endpoint: POST /message")
        print("🏥 Health check: GET /health")
        print("🔄 Reset agent: POST /reset")
        print("🧹 Cleanup agents: POST /cleanup")
        print()
        print("⚡ LOCAL SERVER OPTIMIZATIONS:")
        print("   • Request spacing: 0.1s (ultra-fast local)")
        print("   • Memory blocks: 1 (minimal)")
        print("   • No embedding processing")
        print("   • Local Letta server (no network delays)")
        print()
        print("📱 MULTI-MESSAGE FIXES:")
        print("   • STRICT MAX 3 messages (no more spam!)")
        print("   • Natural message breaking")
        print("   • Local processing (no Letta pressure)")
        print("   • Backend compatible format")
        print()
        print("🛑 Press Ctrl+C to stop")
        
        bridge.run()
        
    except KeyboardInterrupt:
        print("\n💕 LOCAL Niya Bridge shutting down gracefully...")
        print("👋 Priya says goodbye for now!")
    except Exception as e:
        print(f"❌ LOCAL Bridge service error: {e}")

if __name__ == "__main__":
    main()
