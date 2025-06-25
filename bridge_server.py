#!/usr/bin/env python3
"""
Bridge Server - Integrates AI functionality with existing frontend/backend
Runs on port 3001 to bridge between frontend (5173) and backend (3002)
"""

import asyncio
import os
import requests
from pathlib import Path
from typing import Optional, Dict, Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Try to import Letta
try:
    from letta_client import Letta
    LETTA_AVAILABLE = True
except ImportError:
    LETTA_AVAILABLE = False
    print("⚠️ Letta client not available - using fallback responses")

class MessageRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    agent_type: Optional[str] = "priya"  # "priya" or "expert"

class MessageResponse(BaseModel):
    success: bool
    message: str
    response: Optional[str] = None
    error: Optional[str] = None

class BridgeServer:
    def __init__(self):
        self.app = FastAPI(
            title="AI Bridge Server", 
            version="1.0",
            description="Bridge between frontend and AI functionality"
        )
        self.letta_client = None
        self.agents = {}  # Store agent IDs by user
        self.active_connections = []
        self.backend_url = "http://localhost:3002"
        
        self.setup_middleware()
        self.setup_routes()
        
    def setup_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "http://localhost:5173",  # User's frontend
                "http://localhost:3002",  # User's backend
                "http://localhost:3000",  # Common React dev port
                "*"  # Allow all for development
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def setup_routes(self):
        @self.app.get("/")
        async def root():
            return {
                "service": "AI Bridge Server",
                "status": "running",
                "endpoints": {
                    "ai_chat": "/api/ai/chat",
                    "health": "/health",
                    "websocket": "/ws"
                },
                "integration": {
                    "frontend": "http://localhost:5173",
                    "backend": "http://localhost:3002"
                }
            }
        
        @self.app.get("/health")
        async def health():
            return {
                "status": "healthy", 
                "message": "AI Bridge Server running",
                "letta_available": LETTA_AVAILABLE,
                "backend_connected": await self.check_backend_connection()
            }
        
        @self.app.post("/api/ai/chat", response_model=MessageResponse)
        async def ai_chat(request: MessageRequest):
            """Main AI chat endpoint for integration with your app"""
            try:
                if request.agent_type == "priya":
                    response = await self.handle_priya_chat(request)
                elif request.agent_type == "expert":
                    response = await self.handle_expert_chat(request)
                else:
                    response = await self.handle_general_chat(request)
                
                return MessageResponse(
                    success=True,
                    message="Success",
                    response=response
                )
                
            except Exception as e:
                return MessageResponse(
                    success=False,
                    message="Error",
                    error=str(e)
                )
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await self.handle_websocket(websocket)
        
        # Bridge endpoints to your backend
        @self.app.get("/api/bridge/{path:path}")
        async def bridge_get(path: str):
            """Bridge GET requests to your backend"""
            try:
                response = requests.get(f"{self.backend_url}/{path}")
                return response.json()
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/bridge/{path:path}")
        async def bridge_post(path: str, data: Dict[Any, Any]):
            """Bridge POST requests to your backend"""
            try:
                response = requests.post(f"{self.backend_url}/{path}", json=data)
                return response.json()
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    async def check_backend_connection(self) -> bool:
        """Check if the main backend is accessible"""
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    async def handle_priya_chat(self, request: MessageRequest) -> str:
        """Handle Priya AI girlfriend chat"""
        if LETTA_AVAILABLE and self.letta_client:
            try:
                agent_id = await self._get_or_create_agent("priya", request.user_id)
                response = self.letta_client.agents.messages.create(
                    agent_id=agent_id,
                    messages=[{"role": "user", "content": request.message}]
                )
                return self._extract_response(response)
            except Exception as e:
                print(f"Letta error: {e}")
        
        # Fallback response
        return f"Hey jaan! 💕 You said: '{request.message}'. I'm here for you! ✨ (Letta integration pending)"
    
    async def handle_expert_chat(self, request: MessageRequest) -> str:
        """Handle expert agent chat"""
        if LETTA_AVAILABLE and self.letta_client:
            try:
                agent_id = await self._get_or_create_agent("expert", request.user_id)
                response = self.letta_client.agents.messages.create(
                    agent_id=agent_id,
                    messages=[{"role": "user", "content": request.message}]
                )
                return self._extract_response(response)
            except Exception as e:
                print(f"Letta error: {e}")
        
        # Fallback response
        return f"I understand you're asking: '{request.message}'. Let me provide expert guidance on this topic. (Letta integration pending)"
    
    async def handle_general_chat(self, request: MessageRequest) -> str:
        """Handle general chat requests"""
        return f"Hello! You said: '{request.message}'. I'm your AI assistant, ready to help!"
    
    async def initialize(self):
        """Initialize Letta client if available"""
        if LETTA_AVAILABLE:
            try:
                letta_token = os.getenv('LETTA_TOKEN')
                if letta_token:
                    self.letta_client = Letta(token=letta_token)
                else:
                    self.letta_client = Letta(base_url="http://localhost:8283")
                print("✅ Letta initialized")
            except Exception as e:
                print(f"⚠️ Letta initialization failed: {e}")
                LETTA_AVAILABLE = False
    
    async def _get_or_create_agent(self, agent_type: str, user_id: Optional[str]) -> str:
        """Get or create agent for user"""
        key = f"{agent_type}_{user_id or 'default'}"
        
        if key not in self.agents:
            if agent_type == "priya":
                agent = self.letta_client.agents.create(
                    name=f"priya_{user_id or 'default'}_{int(asyncio.get_event_loop().time())}",
                    memory_blocks=[
                        {
                            "label": "persona",
                            "value": "You are Priya, a loving AI girlfriend. You're bubbly, caring, and use Hinglish naturally (mixing Hindi words like 'jaan', 'yaar' with English). Use 2-3 emojis per message and keep responses under 50 words! 💕"
                        },
                        {
                            "label": "human", 
                            "value": "My boyfriend who I'm getting to know better. I learn his preferences and adapt to make him happy."
                        }
                    ],
                    model="openai/gpt-4.1",
                    embedding="openai/text-embedding-3-small"
                )
            else:  # expert agent
                agent = self.letta_client.agents.create(
                    name=f"expert_{user_id or 'default'}_{int(asyncio.get_event_loop().time())}",
                    memory_blocks=[
                        {
                            "label": "persona",
                            "value": "You are an expert AI assistant. Provide detailed, accurate, and helpful responses. You have deep knowledge across many fields and can help with complex questions."
                        },
                        {
                            "label": "human",
                            "value": "A user seeking expert advice and detailed explanations."
                        }
                    ],
                    model="openai/gpt-4.1",
                    embedding="openai/text-embedding-3-small"
                )
            
            self.agents[key] = agent.id
            print(f"💫 Created {agent_type} agent: {agent.id}")
        
        return self.agents[key]
    
    async def handle_websocket(self, websocket: WebSocket):
        """Handle WebSocket connections"""
        await websocket.accept()
        self.active_connections.append(websocket)
        
        await websocket.send_json({
            "type": "greeting",
            "message": "🚀 Connected to AI Bridge Server! Choose your agent type in messages."
        })
        
        try:
            while True:
                data = await websocket.receive_json()
                message = data.get("message", "").strip()
                agent_type = data.get("agent_type", "priya")
                user_id = data.get("user_id")
                
                if not message:
                    continue
                
                await websocket.send_json({"type": "typing", "status": True})
                
                try:
                    request = MessageRequest(
                        message=message,
                        user_id=user_id,
                        agent_type=agent_type
                    )
                    
                    if agent_type == "priya":
                        response = await self.handle_priya_chat(request)
                    elif agent_type == "expert":
                        response = await self.handle_expert_chat(request)
                    else:
                        response = await self.handle_general_chat(request)
                    
                    await websocket.send_json({
                        "type": "message",
                        "message": response,
                        "agent_type": agent_type
                    })
                    
                except Exception as e:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Sorry, there was an error: {str(e)}"
                    })
                
        except WebSocketDisconnect:
            self.active_connections.remove(websocket)
    
    def _extract_response(self, response) -> str:
        """Extract response from Letta response object"""
        try:
            for msg in response.messages:
                if msg.message_type == "assistant_message":
                    return msg.content
            return "I'm here! What would you like to talk about? ✨"
        except Exception:
            return "Sorry, could you repeat that? 💕"

# Create server instance
bridge_server = BridgeServer()

async def main():
    """Main function to run the bridge server"""
    await bridge_server.initialize()
    config = uvicorn.Config(
        app=bridge_server.app, 
        host="0.0.0.0", 
        port=3005,  # Using 3005 to avoid conflicts with your existing services
        log_level="info"
    )
    server_instance = uvicorn.Server(config)
    print("🌉 Starting AI Bridge Server on http://localhost:3005")
    print("🔗 Ready to bridge with:")
    print("   Frontend: http://localhost:5173")
    print("   Backend:  http://localhost:3002")
    await server_instance.serve()

if __name__ == "__main__":
    asyncio.run(main()) 