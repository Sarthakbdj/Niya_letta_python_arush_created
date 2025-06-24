from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
from letta_client import Letta
import uvicorn

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Letta Agent API",
    description="API for interacting with Letta AI agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models for request/response
class MessageRequest(BaseModel):
    message: str
    agent_id: Optional[str] = None

class MessageResponse(BaseModel):
    success: bool
    message: str
    agent_id: Optional[str] = None
    response: Optional[str] = None
    error: Optional[str] = None

class AgentInfo(BaseModel):
    id: str
    name: str
    model: str
    status: str

# Global variables
client = None
current_agent = None

def get_client():
    """Get or initialize the Letta client"""
    global client
    if client is None:
        api_key = os.getenv("LETTA_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="LETTA_API_KEY not found in environment variables")
        client = Letta(token=api_key)
    return client

def get_or_create_agent():
    """Get existing agent or create a new one"""
    global current_agent
    if current_agent is None:
        client = get_client()
        try:
            # Create a new agent
            current_agent = client.agents.create(
                model="openai/gpt-4.1",
                embedding="openai/text-embedding-3-small",
                memory_blocks=[
                    {
                        "label": "human",
                        "value": "The human's name is Chad. They like vibe coding."
                    },
                    {
                        "label": "persona",
                        "value": "My name is Sam, the all-knowing sentient AI."
                    }
                ],
                tools=["web_search", "run_code"]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create agent: {str(e)}")
    return current_agent

@app.get("/")
async def root():
    """Root endpoint - serve the chat interface"""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "Letta Agent API is running!", "status": "active"}

@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {"message": "Letta Agent API is running!", "status": "active"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Letta Agent API"}

@app.post("/agent/create", response_model=AgentInfo)
async def create_agent():
    """Create a new Letta agent"""
    try:
        agent = get_or_create_agent()
        return AgentInfo(
            id=agent.id,
            name=agent.name,
            model=agent.model,
            status="active"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agent/info", response_model=AgentInfo)
async def get_agent_info():
    """Get information about the current agent"""
    try:
        agent = get_or_create_agent()
        return AgentInfo(
            id=agent.id,
            name=agent.name,
            model=agent.model,
            status="active"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    """Send a message to the Letta agent"""
    try:
        client = get_client()
        agent = get_or_create_agent()
        
        # Use provided agent_id if specified, otherwise use current agent
        agent_id = request.agent_id if request.agent_id else agent.id
        
        # Send message to agent
        response = client.agents.messages.create(
            agent_id=agent_id,
            messages=[{"role": "user", "content": request.message}],
        )
        
        # Get the last message from the response
        last_message = response.messages[-1].content if response.messages else "No response received"
        
        return MessageResponse(
            success=True,
            message="Message sent successfully",
            agent_id=agent_id,
            response=last_message
        )
        
    except Exception as e:
        return MessageResponse(
            success=False,
            message="Failed to send message",
            error=str(e)
        )

@app.get("/agents", response_model=List[AgentInfo])
async def list_agents():
    """List all available agents"""
    try:
        client = get_client()
        agents = client.agents.list()
        
        agent_list = []
        for agent in agents:
            agent_list.append(AgentInfo(
                id=agent.id,
                name=agent.name,
                model=agent.model,
                status="active"
            ))
        
        return agent_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1511) 