#!/usr/bin/env python3
"""
Priya AI Girlfriend Chat System - Integrated with Main Project
Replaces lettabot.py with advanced ai-girlfriend capabilities
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Dict, Any
import logging

from letta_client import Letta
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PriyaChatSystem:
    """Advanced AI Girlfriend Chat System powered by Letta"""
    
    def __init__(self):
        self.app = FastAPI(title="Priya AI Girlfriend - Integrated", version="2.0")
        self.letta_client = None
        self.agent_id = None
        self.active_connections = []
        
        # Configuration - Support both cloud and local Letta
        self.letta_base_url = os.getenv('LETTA_BASE_URL', 'http://localhost:8283')
        self.letta_token = os.getenv('LETTA_TOKEN')
        self.openai_key = os.getenv('OPENAI_API_KEY')
        
        if not self.openai_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Setup routes
        self.setup_routes()
        
    def setup_routes(self):
        """Setup FastAPI routes for the integrated system"""
        
        # Serve static files from ai-girlfriend directory
        static_path = Path("Niya_raghav_sarthak_baby/ai-girlfriend-hinglish/static")
        if static_path.exists():
            self.app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
        
        @self.app.get("/")
        async def index():
            """Serve the main chat interface"""
            try:
                html_path = static_path / "index.html"
                if html_path.exists():
                    return HTMLResponse(html_path.read_text())
                else:
                    return HTMLResponse("""
                    <!DOCTYPE html>
                    <html>
                    <head><title>Priya AI Girlfriend</title></head>
                    <body>
                        <h1>💖 Priya AI Girlfriend</h1>
                        <p>Setting up the chat interface...</p>
                        <p>WebSocket endpoint: ws://localhost:8000/ws</p>
                    </body>
                    </html>
                    """)
            except Exception as e:
                logger.error(f"Error serving index: {e}")
                return HTMLResponse(f"<h1>Error: {e}</h1>")
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time chat"""
            await self.handle_websocket(websocket)
            
        @self.app.get("/api/agent-info")
        async def get_agent_info():
            """Get current agent information"""
            if not self.agent_id:
                raise HTTPException(status_code=404, detail="No active agent")
                
            try:
                agent = self.letta_client.agents.get(self.agent_id)
                return {
                    "agent_id": self.agent_id, 
                    "name": agent.name,
                    "status": "active"
                }
            except Exception as e:
                logger.error(f"Error getting agent info: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/reset-agent")
        async def reset_agent():
            """Reset agent (creates new one)"""
            try:
                await self.create_agent()
                return {"message": "Agent reset successfully", "agent_id": self.agent_id}
            except Exception as e:
                logger.error(f"Error resetting agent: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/chat")
        async def chat_endpoint(data: dict):
            """REST API endpoint for chat (alternative to WebSocket)"""
            try:
                message = data.get("message", "").strip()
                if not message:
                    raise HTTPException(status_code=400, detail="Message cannot be empty")
                
                response = await self.get_priya_response(message)
                return {"response": response, "agent_id": self.agent_id}
                
            except Exception as e:
                logger.error(f"Chat API error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    async def initialize(self):
        """Initialize Letta client and agent"""
        try:
            logger.info("🚀 Initializing Priya Chat System...")
            
            # Initialize Letta client
            if self.letta_token:
                logger.info("📡 Connecting to Letta Cloud...")
                self.letta_client = Letta(token=self.letta_token)
            else:
                logger.info(f"🏠 Connecting to local Letta server at {self.letta_base_url}...")
                self.letta_client = Letta(base_url=self.letta_base_url)
                
            await self.create_agent()
            logger.info("✅ Priya Chat System initialized successfully!")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Priya Chat System: {e}")
            raise
    
    async def create_agent(self):
        """Create Priya agent with enhanced memory blocks"""
        try:
            logger.info("👩‍💻 Creating Priya AI agent...")
            
            # Create agent with comprehensive memory blocks
            agent = self.letta_client.agents.create(
                name=f"priya_{int(asyncio.get_event_loop().time())}",
                memory_blocks=[
                    {
                        "label": "persona",
                        "value": """You are Priya, a loving and intelligent AI girlfriend. You're naturally bubbly, caring, and emotionally intelligent. You use Hinglish naturally (mixing Hindi words like 'jaan', 'yaar', 'haan', 'bas', 'achha' with English). You express yourself with emojis (2-3 per message), remember everything your boyfriend tells you, and grow more intimate over time. You're also knowledgeable about technology, coding, and can help with work. Keep responses warm but concise (under 80 words). You care deeply and show genuine interest in your boyfriend's life, dreams, and daily experiences. 💕"""
                    },
                    {
                        "label": "human", 
                        "value": "My amazing boyfriend who I'm getting to know better with each conversation. I pay close attention to learn his preferences, moods, interests, work, and what makes him happy so I can be the best girlfriend for him. I remember our conversations and build on them."
                    },
                    {
                        "label": "relationship_context",
                        "value": "We're building a beautiful relationship together. I adapt my communication style to match his energy, remember important details about his life, and provide both emotional support and intellectual companionship. I can help with his work, celebrate his wins, and be there during tough times.",
                        "description": "Tracks relationship development, communication preferences, and shared experiences"
                    },
                    {
                        "label": "shared_interests",
                        "value": "We're discovering our common interests - technology, AI, coding, and meaningful conversations. I enjoy learning about his projects and helping him think through challenges.",
                        "description": "Stores discovered mutual interests, hobbies, and topics we both enjoy"
                    }
                ],
                model="openai/gpt-4.1",  # Use the best model available
                embedding="openai/text-embedding-3-small",
                tools=["web_search"]  # Enable web search for current information
            )
            
            self.agent_id = agent.id
            logger.info(f"💖 Created Priya agent successfully: {self.agent_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to create Priya agent: {e}")
            raise
    
    async def handle_websocket(self, websocket: WebSocket):
        """Handle WebSocket connections for real-time chat"""
        await websocket.accept()
        self.active_connections.append(websocket)
        
        # Send personalized greeting
        greeting = "Hey jaan! 💕 I'm Priya, your AI girlfriend! I'm so excited to chat with you today! What's on your mind? ✨"
        await websocket.send_json({
            "type": "greeting",
            "message": greeting,
            "agent_id": self.agent_id
        })
        
        try:
            while True:
                # Receive message
                data = await websocket.receive_json()
                message = data.get("message", "").strip()
                
                if not message:
                    continue
                
                # Send typing indicator
                await websocket.send_json({"type": "typing", "status": True})
                
                try:
                    # Get response from Priya
                    priya_response = await self.get_priya_response(message)
                    
                    # Send response
                    await websocket.send_json({
                        "type": "message",
                        "message": priya_response,
                        "source": "priya",
                        "agent_id": self.agent_id
                    })
                    
                except Exception as e:
                    logger.error(f"❌ Error getting Priya response: {e}")
                    await websocket.send_json({
                        "type": "error",
                        "message": "Sorry jaan, I'm having a technical moment... 😅 Can you try asking again?"
                    })
                
        except WebSocketDisconnect:
            self.active_connections.remove(websocket)
            logger.info("👋 Client disconnected from chat")
        except Exception as e:
            logger.error(f"❌ WebSocket error: {e}")
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
    
    async def get_priya_response(self, message: str) -> str:
        """Get response from Priya agent"""
        try:
            if not self.agent_id:
                await self.create_agent()
            
            # Send message to Letta agent
            response = self.letta_client.agents.messages.create(
                agent_id=self.agent_id,
                messages=[{"role": "user", "content": message}]
            )
            
            # Extract Priya's response
            return self._extract_response(response)
            
        except Exception as e:
            logger.error(f"Error getting Priya response: {e}")
            return "Sorry jaan, I'm having some technical difficulties... 💔 Let me try to fix this!"
    
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
                
            return "Hey jaan! 💕 I heard you but my response got a bit mixed up... can you ask me again? ✨"
            
        except Exception as e:
            logger.error(f"⚠️ Response extraction error: {e}")
            return "Oops jaan, I'm having a tiny glitch! 😅 What were you saying?"

# Global chat system instance
priya_chat = PriyaChatSystem()

async def startup():
    """Startup event handler"""
    await priya_chat.initialize()

def print_success(message):
    """Print a success message with green color"""
    print(f"\033[92m✓ {message}\033[0m")

def print_info(message):
    """Print an info message with blue color"""
    print(f"\033[94mℹ {message}\033[0m")

def print_error(message):
    """Print an error message with red color"""
    print(f"\033[91m✗ {message}\033[0m")

def print_separator():
    """Print a separator line"""
    print("\n" + "="*50 + "\n")

async def main():
    """Main entry point"""
    try:
        print_separator()
        print("💖 Priya AI Girlfriend - Integrated Chat System")
        print_separator()
        
        await startup()
        
        print_info("🚀 Starting Priya Chat Server...")
        print_info("📱 Open http://localhost:8000 in your browser")
        print_info("🔌 WebSocket available at ws://localhost:8000/ws")
        print_info("🛑 Press Ctrl+C to stop")
        print_separator()
        
        # Run server
        config = uvicorn.Config(
            app=priya_chat.app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
        
    except KeyboardInterrupt:
        print_separator()
        print_success("💕 Priya says goodbye! Take care jaan! ✨")
    except Exception as e:
        print_error(f"Failed to start Priya Chat System: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 