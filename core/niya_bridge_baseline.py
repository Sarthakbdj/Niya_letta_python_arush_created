#!/usr/bin/env python3
"""
Baseline Niya Bridge - NO SPECIAL FLAGS OR OPTIMIZATIONS
This is the raw Letta behavior without any context management or reset strategies
Used to demonstrate context bloat and retention issues
"""

import json
import logging
from typing import Dict, Any
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import os
from letta_client import Letta
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaselineNiyaBridge:
    """Baseline bridge service - NO optimizations or special flags"""
    
    def __init__(self):
        self.flask_app = Flask(__name__)
        CORS(self.flask_app)
        
        # Basic configuration - NO special settings
        self.base_url = os.getenv('LETTA_BASE_URL', 'http://localhost:8283')
        self.client = None
        self.agent_id = None
        
        # Basic tracking - NO resets or management
        self.message_count = 0
        self.start_time = time.time()
        
        self.setup_routes()

    def setup_routes(self):
        """Setup basic Flask routes"""
        
        @self.flask_app.route('/message', methods=['POST'])
        def handle_message():
            try:
                data = request.get_json()
                user_message = data.get('message', '').strip()
                
                if not user_message:
                    return jsonify({
                        "messages": ["Hello! What would you like to talk about?"],
                        "total_messages": 1,
                        "success": True,
                        "message_count": self.message_count
                    })
                
                # Increment message count (for tracking only)
                self.message_count += 1
                
                # Get raw response from Letta - NO timeouts, NO special handling
                response = self.client.agents.send_message(
                    agent_id=self.agent_id,
                    message=user_message
                )
                
                # Extract response - minimal processing
                assistant_messages = []
                if response and response.messages:
                    for msg in response.messages:
                        if hasattr(msg, 'role') and msg.role == 'assistant':
                            if hasattr(msg, 'text') and msg.text:
                                assistant_messages.append(msg.text.strip())
                
                if not assistant_messages:
                    assistant_messages = ["I hear you! Let me think about that..."]
                
                return jsonify({
                    "messages": assistant_messages,
                    "total_messages": len(assistant_messages),
                    "success": True,
                    "message_count": self.message_count,
                    "uptime_seconds": int(time.time() - self.start_time),
                    "agent_id": self.agent_id
                })
                
            except Exception as e:
                logger.error(f"Error in handle_message: {e}")
                return jsonify({
                    "messages": [f"Error occurred: {str(e)}"],
                    "total_messages": 1,
                    "success": False,
                    "error": str(e),
                    "message_count": self.message_count
                }), 500

        @self.flask_app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({
                "status": "healthy",
                "service": "Niya-Python Bridge - BASELINE (No Optimizations)",
                "agent_id": self.agent_id,
                "letta_connected": bool(self.client),
                "message_count": self.message_count,
                "uptime_seconds": int(time.time() - self.start_time),
                "optimizations": "NONE - Raw Letta behavior",
                "context_management": "NONE - Let context grow naturally",
                "reset_strategy": "NONE - Agent never resets"
            })

        @self.flask_app.route('/reset', methods=['POST'])
        def reset_agent():
            """Manual reset endpoint for testing"""
            try:
                old_agent = self.agent_id
                self.create_agent()
                self.message_count = 0  # Reset counter
                return jsonify({
                    "message": "Agent reset manually",
                    "old_agent_id": old_agent,
                    "new_agent_id": self.agent_id,
                    "success": True
                })
            except Exception as e:
                return jsonify({"error": str(e), "success": False}), 500

    def initialize(self):
        """Initialize basic Letta client"""
        try:
            logger.info("Initializing baseline Niya bridge...")
            
            # Create basic Letta client
            self.client = Letta(base_url=self.base_url)
            logger.info(f"Connected to Letta server at {self.base_url}")
            
            # Create basic agent
            self.create_agent()
            
            logger.info("Baseline bridge initialized successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize baseline bridge: {e}")
            return False

    def create_agent(self):
        """Create basic Priya agent - NO optimizations"""
        try:
            logger.info("Creating baseline Priya agent...")
            
            # Delete old agent if exists
            if self.agent_id:
                try:
                    self.client.agents.delete(self.agent_id)
                except:
                    pass
            
            # Create agent with basic configuration - NO special memory blocks
            agent = self.client.agents.create(
                name=f"priya_baseline_{int(time.time())}",
                embedding="openai/text-embedding-3-small",
                model="gpt-4o-mini",
                persona="""You are Priya, a friendly AI companion. You're warm, caring, and conversational. 
                You remember things about the user and have engaging conversations. 
                Express yourself naturally and be helpful.""",
                human="A user who wants to chat with me.",
                tools=[]
            )
            
            self.agent_id = agent.id
            logger.info(f"Created baseline agent: {self.agent_id}")
            
        except Exception as e:
            logger.error(f"Failed to create baseline agent: {e}")
            raise

    def run(self, host='localhost', port=1512):
        """Run the baseline bridge service"""
        logger.info(f"Starting BASELINE Niya-Python Bridge on {host}:{port}")
        logger.info("⚠️  NO OPTIMIZATIONS - Raw Letta behavior")
        logger.info("⚠️  NO CONTEXT MANAGEMENT - Will grow until failure")
        logger.info("⚠️  NO RESET STRATEGY - Agent persists indefinitely")
        self.flask_app.run(host=host, port=port, debug=False, threaded=True)

# Global bridge instance
bridge = BaselineNiyaBridge()

def main():
    """Main entry point for baseline testing"""
    try:
        print("🔬" * 30)
        print("🔬 BASELINE NIYA BRIDGE - NO OPTIMIZATIONS")
        print("🔬" * 30)
        print()
        print("⚠️  WARNING: This is the RAW Letta behavior")
        print("⚠️  NO special flags, NO context management, NO resets")
        print("⚠️  Expected to fail after 4-5 messages due to context bloat")
        print()
        
        if not bridge.initialize():
            print("❌ Failed to initialize baseline bridge service")
            return
        
        print("✅ Baseline bridge initialized successfully!")
        print("🔗 Running on: http://localhost:1512")
        print("📡 Main endpoint: POST /message")
        print("🏥 Health check: GET /health")
        print("🔄 Manual reset: POST /reset")
        print()
        print("🧪 TESTING PURPOSE:")
        print("   • Demonstrate context bloat issues")
        print("   • Show loss of context retention")
        print("   • Reproduce failure after 4-5 messages")
        print()
        print("🛑 Press Ctrl+C to stop")
        
        bridge.run()
        
    except KeyboardInterrupt:
        print("\n💫 Baseline bridge shutting down...")
    except Exception as e:
        print(f"❌ Baseline bridge error: {e}")

if __name__ == "__main__":
    main() 