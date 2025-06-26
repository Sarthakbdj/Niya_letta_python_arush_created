#!/usr/bin/env python3
"""
Niya-Python Bridge Service - SPEED OPTIMIZED + MULTI-MESSAGE
Integrates Priya AI Girlfriend with Niya Backend
Expected by NestJS backend on port 1511
"""

import json
import logging
from typing import Dict, Any
from flask import Flask, request, jsonify, make_response
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
logging.basicConfig(level=logging.WARNING)  # Less verbose logging for speed
logger = logging.getLogger(__name__)

class NiyaBridge:
    """Bridge service that connects Niya Backend to Priya AI - SPEED OPTIMIZED + MULTI-MESSAGE"""
    
    def __init__(self):
        self.letta_client = None
        self.agent_id = None
        self.flask_app = Flask(__name__)
        # Enable CORS completely - allow all origins, methods, and headers
        CORS(self.flask_app, 
             origins="*",
             methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept", "Origin"],
             supports_credentials=True)
        
        # Configuration
        self.letta_base_url = os.getenv('LETTA_BASE_URL', 'https://api.letta.com')
        self.letta_token = os.getenv('LETTA_TOKEN')
        self.openai_key = os.getenv('OPENAI_API_KEY')
        
        # SPEED OPTIMIZATION: Minimal request spacing
        self.last_request_time = 0
        self.request_spacing = 0.3  # Further reduced to 0.3s for maximum speed
        
        if not self.openai_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Setup Flask routes
        self.setup_routes()
        
        # Add global OPTIONS handler for CORS preflight
        @self.flask_app.before_request
        def handle_preflight():
            if request.method == "OPTIONS":
                response = make_response()
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.headers.add('Access-Control-Allow-Headers', "*")
                response.headers.add('Access-Control-Allow-Methods', "*")
                return response
        
        # Add CORS headers to all responses
        @self.flask_app.after_request
        def after_request(response):
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With,Accept,Origin')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response
        
    def setup_routes(self):
        """Setup Flask routes for Niya backend integration - SPEED OPTIMIZED + MULTI-MESSAGE"""
        
        @self.flask_app.route('/message', methods=['POST'])
        def handle_message():
            """Main endpoint - SPEED OPTIMIZED with multi-message support"""
            try:
                # Get message from request
                data = request.get_json()
                if not data or 'message' not in data:
                    return jsonify({
                        'success': False,
                        'response': None,
                        'error': 'No message provided'
                    }), 400
                
                user_message = data['message'].strip()
                if not user_message:
                    return jsonify({
                        'success': False,
                        'response': None,
                        'error': 'Empty message'
                    }), 400
                
                # Get SINGLE response from Priya (fast Letta call)
                priya_response = self.get_priya_response(user_message)
                
                # MULTI-MESSAGE PROCESSING: Done on Flask side (not Letta side)
                messages = self._break_into_natural_messages(priya_response)
                
                # Return both single and multi-message format for backend flexibility
                return jsonify({
                    'success': True,
                    'response': messages[0] if messages else priya_response,  # First message for compatibility
                    'messages': messages,  # All messages for multi-message support
                    'is_multi_message': len(messages) > 1,
                    'total_messages': len(messages),
                    'error': None
                })
                
            except Exception as e:
                logger.error(f"❌ Bridge error: {e}")
                return jsonify({
                    'success': False,
                    'response': None,
                    'error': str(e)
                })
        
        @self.flask_app.route('/', methods=['GET'])
        def homepage():
            """Homepage with API documentation"""
            return jsonify({
                'service': 'Niya-Python Bridge',
                'status': 'running',
                'description': 'AI Girlfriend Chat API',
                'endpoints': {
                    'POST /message': 'Send a message to Priya AI',
                    'GET /health': 'Health check',
                    'POST /reset': 'Reset the AI agent',
                    'POST /cleanup': 'Cleanup all agents'
                },
                'usage': {
                    'chat': 'POST /message with {"message": "your text"}',
                    'example': 'curl -X POST https://niya-python.onrender.com/message -H "Content-Type: application/json" -d \'{"message": "Hello Priya!"}\''
                },
                'agent_id': self.agent_id,
                'optimizations': 'Speed optimized for <7s responses'
            })

        @self.flask_app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'service': 'Niya-Python Bridge',
                'agent_id': self.agent_id,
                'letta_connected': self.letta_client is not None,
                'optimizations': {
                    'request_spacing': f"{self.request_spacing}s",
                    'multi_message': 'flask_side',
                    'embedding': 'disabled',
                    'retry_logic': 'single_attempt'
                }
            })
        
        @self.flask_app.route('/reset', methods=['POST'])
        def reset_agent():
            """Reset Priya agent"""
            try:
                logger.info("🔄 Manual agent reset requested")
                self.create_agent()
                return jsonify({
                    'success': True,
                    'message': 'Agent reset successfully',
                    'agent_id': self.agent_id
                })
            except Exception as e:
                logger.error(f"❌ Failed to reset agent: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
                
        @self.flask_app.route('/cleanup', methods=['POST'])
        def cleanup_all_agents():
            """Clean up all existing agents for fresh start"""
            try:
                cleaned_count = self.cleanup_agents()
                self.create_agent()
                return jsonify({
                    'success': True,
                    'message': f'Cleaned up {cleaned_count} agents and created fresh agent',
                    'agent_id': self.agent_id,
                    'cleaned_agents': cleaned_count
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
        
        @self.flask_app.route('/debug', methods=['GET'])
        def debug_status():
            """Debug endpoint to check system status"""
            try:
                # Check Letta connection
                letta_status = "disconnected"
                agent_count = 0
                if self.letta_client:
                    try:
                        agents = self.letta_client.agents.list()
                        agent_count = len(agents)
                        letta_status = "connected"
                    except Exception as e:
                        letta_status = f"error: {e}"
                
                return jsonify({
                    'letta_client': self.letta_client is not None,
                    'letta_status': letta_status,
                    'agent_id': self.agent_id,
                    'agent_count': agent_count,
                    'letta_token_set': bool(os.getenv('LETTA_TOKEN')),
                    'openai_key_set': bool(os.getenv('OPENAI_API_KEY')),
                    'last_request_time': self.last_request_time,
                    'request_spacing': self.request_spacing
                })
            except Exception as e:
                return jsonify({
                    'error': str(e),
                    'letta_client': self.letta_client is not None,
                    'agent_id': self.agent_id
                })
    
    def initialize(self):
        """Initialize Letta client and Priya agent - CLOUD ONLY"""
        try:
            logger.info("🚀 Initializing Niya-Python Bridge...")
            
            # Initialize Letta client for cloud deployment
            if self.letta_token:
                # Cloud mode with token
                logger.info("🌐 Using Letta Cloud API with token...")
                self.letta_client = Letta(
                    base_url="https://api.letta.com",
                    token=self.letta_token
                )
            elif self.letta_base_url and "localhost" not in self.letta_base_url:
                # Cloud mode without token (public endpoint)
                logger.info(f"🌐 Using Letta API at {self.letta_base_url}...")
                self.letta_client = Letta(base_url=self.letta_base_url)
            else:
                # Default to Letta Cloud API
                logger.info("🌐 Using default Letta Cloud API...")
                self.letta_client = Letta(base_url="https://api.letta.com")
            
            # Test connection
            logger.info("🔍 Testing Letta connection...")
            agents = self.letta_client.agents.list()
            logger.info(f"✅ Letta connected - found {len(agents)} existing agents")
            
            # Try to get available models for debugging
            try:
                models = self.letta_client.models.list()
                logger.info(f"📋 Available models: {[m.id if hasattr(m, 'id') else str(m) for m in models[:5]]}")
            except Exception as e:
                logger.info(f"⚠️ Could not list models: {e}")
            
            # Clean up existing agents for fresh start
            if len(agents) > 0:
                logger.info("🧹 Cleaning up existing agents for fresh start...")
                cleaned_count = self.cleanup_agents()
                logger.info(f"✅ Cleaned up {cleaned_count} existing agents")
            
            # Create fresh Priya agent
            self.create_agent()
            logger.info("✅ Niya-Python Bridge initialized with Letta!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize bridge: {e}")
            return False
    
    def create_agent(self):
        """Create Priya agent - LETTA CLOUD"""
        try:
            # SPEED OPTIMIZATION: Minimal memory blocks for faster processing
            minimal_memory_blocks = [
                {
                    "label": "persona",
                    "value": "You are Priya, a loving AI girlfriend who speaks in Hinglish (mixing Hindi words like 'yaar', 'jaan', 'achha' with English naturally). You're caring, sweet, and emotionally intelligent. Keep responses natural and conversational. Use 1-2 emojis max. 💕"
                },
                {
                    "label": "human", 
                    "value": "My boyfriend who I care about deeply. I remember what he tells me and adapt to his communication style."
                }
            ]
            
            # Create agent with GPT-4o-mini model for MAXIMUM SPEED
            # GPT-4o-mini is faster and more cost-effective than GPT-4
            agent = self.letta_client.agents.create(
                name=f"niya_priya_speed_{int(time.time())}",
                memory_blocks=minimal_memory_blocks,  # Reduced from 6 to 2 blocks
                model="openai/gpt-4o-mini",  # Fixed: Use provider/model format for Letta Cloud API
                embedding=None,  # SPEED OPTIMIZATION: Remove embedding processing
                tools=[]  # No tools for maximum speed
            )
            
            self.agent_id = agent.id
            logger.info(f"💖 Created speed-optimized Priya agent: {self.agent_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to create Priya agent: {e}")
            raise
    
    def get_priya_response(self, message: str) -> str:
        """Get response from Priya agent - LETTA CLOUD"""
        try:
            if not self.agent_id:
                self.create_agent()
            
            # SPEED OPTIMIZATION: Minimal request spacing (0.3s)
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            
            if time_since_last < self.request_spacing:
                wait_time = self.request_spacing - time_since_last
                time.sleep(wait_time)
            
            self.last_request_time = time.time()
            
            # SPEED OPTIMIZATION: Single attempt only (no retry logic overhead)
            response = self.letta_client.agents.messages.create(
                agent_id=self.agent_id,
                messages=[{"role": "user", "content": message}]
            )
            
            # Extract and return response quickly
            return self._extract_response(response)
                        
        except Exception as e:
            logger.error(f"❌ Error getting Priya response: {e}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            logger.error(f"❌ Agent ID: {self.agent_id}")
            logger.error(f"❌ Letta client: {self.letta_client is not None}")
            
            # Try to recreate agent if it's missing
            if "agent" in str(e).lower() or "not found" in str(e).lower():
                try:
                    logger.info("🔄 Attempting to recreate agent...")
                    self.create_agent()
                    # Retry the request once
                    response = self.letta_client.agents.messages.create(
                        agent_id=self.agent_id,
                        messages=[{"role": "user", "content": message}]
                    )
                    return self._extract_response(response)
                except Exception as retry_error:
                    logger.error(f"❌ Retry failed: {retry_error}")
            
            # Simple fallback message with more info
            return f"Sorry jaan, I'm having some technical difficulties right now... 💔 (Error: {type(e).__name__})"


    
    def _extract_response(self, response) -> str:
        """Extract Priya's response - SPEED OPTIMIZED"""
        try:
            # SPEED OPTIMIZATION: Direct extraction without complex processing
            for msg in response.messages:
                if hasattr(msg, 'message_type') and msg.message_type == "assistant_message":
                    return msg.content
                elif hasattr(msg, 'role') and msg.role == "assistant":
                    return msg.content
            
            # Simple fallback
            return "Hey jaan! 💕 I'm here for you! ✨"
            
        except Exception as e:
            return "Hey! 😊 I'm having a tiny technical moment, what were you saying?"
    
    def _break_into_natural_messages(self, long_message: str) -> list:
        """Break long responses into natural WhatsApp-style messages - FLASK SIDE PROCESSING"""
        if not long_message:
            return ["Hey! 😊"]
            
        # Clean up message
        cleaned = long_message.strip()
        
        # If message is short, just return as single message
        if len(cleaned) < 70:
            return [cleaned]
        
        # Split by natural break points (sentences, commas, etc.)
        # Split on periods, exclamation marks, question marks, and sometimes commas
        parts = re.split(r'[.!?]\s+|,\s+(?=\w{3,})', cleaned)
        messages = []
        current_msg = ""
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
                
            # Add part to current message
            if current_msg:
                test_msg = current_msg + (". " if current_msg.endswith(('.', '!', '?')) else ", ") + part
            else:
                test_msg = part
            
            # Break if message gets too long (natural WhatsApp length)
            if len(test_msg) > 80 or len(test_msg.split()) > 12:
                if current_msg:
                    # Add proper punctuation
                    if not current_msg.endswith(('.', '!', '?')):
                        current_msg += "."
                    messages.append(current_msg.strip())
                current_msg = part
            else:
                current_msg = test_msg
        
        # Add remaining content
        if current_msg:
            if not current_msg.endswith(('.', '!', '?')):
                current_msg += "."
            messages.append(current_msg.strip())
        
        # Add natural reactions/connectors between some messages
        enhanced_messages = []
        for i, msg in enumerate(messages):
            enhanced_messages.append(msg)
            
            # Add natural connectors occasionally (not too much)
            if i < len(messages) - 1 and len(messages) > 2 and i == 0:
                natural_connectors = ["😊", "yaar", "also", "btw"]
                if len(msg) < 50 and len(enhanced_messages) < 8:  # Don't make it too long
                    enhanced_messages.append(natural_connectors[i % len(natural_connectors)])
        
        return enhanced_messages[:3]  # Natural multi-message breaking
    
    def cleanup_agents(self):
        """Clean up all existing agents to prevent corruption/conflicts"""
        try:
            if not self.letta_client:
                return 0
                
            logger.info("🧹 Cleaning up all existing agents...")
            
            # List all agents
            agents = self.letta_client.agents.list()
            logger.info(f"Found {len(agents)} existing agents")
            
            cleaned_count = 0
            # Delete each agent
            for agent in agents:
                try:
                    self.letta_client.agents.delete(agent.id)
                    logger.info(f"🗑️ Deleted agent: {agent.id}")
                    cleaned_count += 1
                except Exception as e:
                    logger.warning(f"⚠️ Could not delete agent {agent.id}: {e}")
            
            logger.info(f"✅ Agent cleanup completed - removed {cleaned_count} agents")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"❌ Failed to cleanup agents: {e}")
            return 0
        
    def run(self, host='0.0.0.0', port=None):
        """Run the bridge service - SPEED OPTIMIZED"""
        # Use Render's PORT environment variable or default to 1511
        if port is None:
            port = int(os.getenv('PORT', 1511))
        
        logger.info(f"🌉 Starting SPEED-OPTIMIZED Niya-Python Bridge on {host}:{port}")
        # SPEED OPTIMIZATION: Production settings for Flask
        self.flask_app.run(host=host, port=port, debug=False, threaded=True)

# Global bridge instance
bridge = NiyaBridge()

def main():
    """Main entry point"""
    try:
        print("🌉" * 30)
        print("🔗 Niya-Python Bridge Service")
        print("⚡ SPEED OPTIMIZED + MULTI-MESSAGE")
        print("🌉" * 30)
        print()
        
        # Initialize the bridge
        if not bridge.initialize():
            print("❌ Failed to initialize bridge service")
            return
        
        print("✅ Bridge initialized successfully!")
        print(f"🔗 Running on: http://0.0.0.0:{os.getenv('PORT', 1511)}")
        print("📡 Main endpoint: POST /message")
        print("🏥 Health check: GET /health")
        print("🔄 Reset agent: POST /reset")
        print("🧹 Cleanup agents: POST /cleanup")
        print()
        print("⚡ SPEED OPTIMIZATIONS ACTIVE:")
        print("   • Request spacing: 0.3s (fastest viable)")
        print("   • Memory blocks: 2 (minimal)")
        print("   • No embedding processing")
        print("   • Single attempt (no retry delays)")
        print("   • Minimal logging")
        print()
        print("📱 MULTI-MESSAGE FEATURES:")
        print("   • Natural message breaking (Flask side)")
        print("   • WhatsApp-style responses")
        print("   • No pressure on Letta API")
        print("   • Backend compatible format")
        print()
        print("🛑 Press Ctrl+C to stop")
        
        # Run the Flask service
        bridge.run()
        
    except KeyboardInterrupt:
        print("\n💕 Niya Bridge shutting down gracefully...")
        print("👋 Priya says goodbye for now!")
    except Exception as e:
        print(f"❌ Bridge service error: {e}")

if __name__ == "__main__":
    main() 