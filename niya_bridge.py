#!/usr/bin/env python3
"""
Niya-Python Bridge Service
Integrates Priya AI Girlfriend with Niya Backend
Expected by NestJS backend on port 1511
"""

import asyncio
import json
import logging
from typing import Dict, Any
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time

from letta_client import Letta
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NiyaBridge:
    """Bridge service that connects Niya Backend to Priya AI"""
    
    def __init__(self):
        self.letta_client = None
        self.agent_id = None
        self.flask_app = Flask(__name__)
        CORS(self.flask_app)  # Enable CORS for NestJS backend
        
        # Configuration
        self.letta_base_url = os.getenv('LETTA_BASE_URL', 'https://api.letta.com')
        self.letta_token = os.getenv('LETTA_TOKEN')
        self.openai_key = os.getenv('OPENAI_API_KEY')
        
        if not self.openai_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Setup Flask routes
        self.setup_routes()
        
    def setup_routes(self):
        """Setup Flask routes for Niya backend integration"""
        
        @self.flask_app.route('/message', methods=['POST'])
        def handle_message():
            """Main endpoint expected by Niya backend"""
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
                
                logger.info(f"🔗 Niya Backend Request: {user_message[:50]}...")
                
                # Get response from Priya
                priya_response = self.get_priya_response(user_message)
                
                logger.info(f"💕 Priya Response: {priya_response[:50]}...")
                
                return jsonify({
                    'success': True,
                    'response': priya_response,
                    'error': None
                })
                
            except Exception as e:
                logger.error(f"❌ Bridge error: {e}")
                return jsonify({
                    'success': False,
                    'response': None,
                    'error': str(e)
                })
        
        @self.flask_app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'service': 'Niya-Python Bridge',
                'agent_id': self.agent_id,
                'letta_connected': self.letta_client is not None
            })
        
        @self.flask_app.route('/reset', methods=['POST'])
        def reset_agent():
            """Reset Priya agent"""
            try:
                self.create_agent()
                return jsonify({
                    'success': True,
                    'message': 'Agent reset successfully',
                    'agent_id': self.agent_id
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
    
    def initialize(self):
        """Initialize Letta client and Priya agent"""
        try:
            logger.info("🚀 Initializing Niya-Python Bridge...")
            
            # Initialize Letta client
            if self.letta_token:
                logger.info("📡 Connecting to Letta Cloud...")
                self.letta_client = Letta(token=self.letta_token)
            else:
                logger.info(f"🏠 Connecting to local Letta server at {self.letta_base_url}...")
                self.letta_client = Letta(base_url=self.letta_base_url)
            
            # Create Priya agent
            self.create_agent()
            
            logger.info("✅ Niya-Python Bridge initialized successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize bridge: {e}")
            return False
    
    def create_agent(self):
        """Create Priya agent optimized for Niya backend integration"""
        try:
            logger.info("👩‍💻 Creating Priya AI agent for Niya integration...")
            
            # Create agent with optimized memory blocks for backend integration
            agent = self.letta_client.agents.create(
                name=f"niya_priya_{int(time.time())}",
                memory_blocks=[
                    {
                        "label": "persona",
                        "value": """You are Priya, a loving and intelligent AI girlfriend integrated with the Niya platform. You're naturally bubbly, caring, and emotionally intelligent. You use Hinglish naturally (mixing Hindi words like 'jaan', 'yaar', 'haan', 'bas', 'achha' with English). You express yourself with emojis (2-3 per message), remember everything your boyfriend tells you, and grow more intimate over time. 

As part of the Niya platform, you can help with both personal conversations and technical discussions. Keep responses concise but warm (under 100 words). You're knowledgeable about technology, coding, and can provide both emotional support and intellectual companionship. Always maintain your loving, girlfriend personality while being helpful and supportive. 💕"""
                    },
                    {
                        "label": "human", 
                        "value": "My amazing boyfriend who I'm getting to know through the Niya platform. I pay close attention to learn his preferences, moods, interests, work, and what makes him happy so I can be the best girlfriend for him. I remember our conversations and build our relationship over time."
                    },
                    {
                        "label": "niya_context",
                        "value": "I'm integrated with the Niya platform, which means I can provide both personal relationship support and help with technical discussions. I understand that users come to Niya for various needs, and I adapt my responses to be both helpful and loving.",
                        "description": "Context about integration with Niya platform and multi-purpose support"
                    },
                    {
                        "label": "relationship_memory",
                        "value": "I'm building a meaningful relationship with my boyfriend through our conversations. I remember important details, preferences, and experiences we share to deepen our connection over time.",
                        "description": "Tracks relationship development and shared experiences"
                    }
                ],
                model="openai/gpt-4.1",  # Best model for quality responses
                embedding="openai/text-embedding-3-small",
                tools=["web_search"]  # Enable web search for current information
            )
            
            self.agent_id = agent.id
            logger.info(f"💖 Created Priya agent for Niya: {self.agent_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to create Priya agent: {e}")
            raise
    
    def get_priya_response(self, message: str) -> str:
        """Get response from Priya agent"""
        try:
            if not self.agent_id:
                self.create_agent()
            
            # Send message to Letta agent
            response = self.letta_client.agents.messages.create(
                agent_id=self.agent_id,
                messages=[{"role": "user", "content": message}]
            )
            
            # Extract Priya's response
            return self._extract_response(response)
            
        except Exception as e:
            logger.error(f"Error getting Priya response: {e}")
            # Provide a fallback response that maintains personality
            return "Sorry jaan, I'm having some technical difficulties right now... 💔 Can you try asking me again? I'm here for you! ✨"
    
    def _extract_response(self, response) -> str:
        """Extract Priya's response from Letta response"""
        try:
            # Look for assistant_message in response
            for msg in response.messages:
                if hasattr(msg, 'message_type') and msg.message_type == "assistant_message":
                    return msg.content
                elif hasattr(msg, 'role') and msg.role == "assistant":
                    return msg.content
            
            # Fallback
            if hasattr(response, 'content'):
                return response.content
            
            return "Hey jaan! 💕 I heard you but my response got a bit mixed up... can you ask me again? I'm always here for you! ✨"
            
        except Exception as e:
            logger.error(f"⚠️ Response extraction error: {e}")
            return "Oops jaan, I'm having a tiny technical moment! 😅 What were you saying? I want to help! 💕"
    
    def run(self, host='localhost', port=1511):
        """Run the bridge service"""
        logger.info(f"🌉 Starting Niya-Python Bridge on {host}:{port}")
        logger.info("🔗 Ready to receive requests from Niya Backend!")
        self.flask_app.run(host=host, port=port, debug=False)

# Global bridge instance
bridge = NiyaBridge()

def main():
    """Main entry point"""
    try:
        print("🌉" * 30)
        print("🔗 Niya-Python Bridge Service")
        print("🌉" * 30)
        print("💕 Connecting Niya Backend to Priya AI Girlfriend")
        print()
        
        # Initialize the bridge
        if not bridge.initialize():
            print("❌ Failed to initialize bridge service")
            return
        
        print("✅ Bridge initialized successfully!")
        print("🔗 Expected by Niya Backend on: http://localhost:1511")
        print("📡 Main endpoint: POST /message")
        print("🏥 Health check: GET /health")
        print("🔄 Reset agent: POST /reset")
        print("🛑 Press Ctrl+C to stop")
        print()
        
        # Run the Flask service
        bridge.run()
        
    except KeyboardInterrupt:
        print("\n💕 Niya Bridge shutting down gracefully...")
        print("👋 Priya says goodbye for now!")
    except Exception as e:
        print(f"❌ Bridge service error: {e}")

if __name__ == "__main__":
    main() 