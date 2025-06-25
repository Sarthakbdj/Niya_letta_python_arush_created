# Letta Agent FastAPI Server

A FastAPI server that provides a REST API for interacting with Letta AI agents. The server runs on port 1511 and includes a web-based chat interface.

## Features

- 🤖 Create and manage Letta AI agents
- 💬 Send messages to agents via REST API
- 🌐 Web-based chat interface
- 📊 Health check and monitoring endpoints
- 🔄 Automatic agent creation and management

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the project root with your Letta API key:
   ```
   LETTA_API_KEY=your_letta_api_key_here
   ```

3. **Start the server:**
   ```bash
   python server.py
   ```

   The server will start on `http://localhost:1511`

## API Endpoints

### Health Check
- **GET** `/health` - Check server status

### Agent Management
- **GET** `/agent/info` - Get current agent information
- **POST** `/agent/create` - Create a new agent
- **GET** `/agents` - List all available agents

### Messaging
- **POST** `/message` - Send a message to an agent
  ```json
  {
    "message": "Your message here",
    "agent_id": "optional_agent_id"
  }
  ```

## Web Interface

Visit `http://localhost:1511` in your browser to access the web-based chat interface. The interface provides:

- Real-time chat with your Letta agent
- Connection status monitoring
- Agent information display
- Responsive design

## Testing

Run the test script to verify the API functionality:

```bash
python test_api.py
```

## Example Usage

### Using curl

1. **Check server health:**
   ```bash
   curl http://localhost:1511/health
   ```

2. **Get agent info:**
   ```bash
   curl http://localhost:1511/agent/info
   ```

3. **Send a message:**
   ```bash
   curl -X POST http://localhost:1511/message \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello! How are you today?"}'
   ```

### Using Python requests

```python
import requests

# Send a message
response = requests.post(
    "http://localhost:1511/message",
    json={"message": "Tell me a joke"}
)

if response.status_code == 200:
    result = response.json()
    print(f"Agent response: {result['response']}")
```

## Configuration

The server uses the following configuration:

- **Port:** 1511
- **Host:** 0.0.0.0 (accessible from any IP)
- **CORS:** Enabled for all origins (configure for production)
- **Agent Model:** openai/gpt-4.1
- **Embedding Model:** openai/text-embedding-3-small

## Troubleshooting

1. **Server won't start:**
   - Check if port 1511 is available
   - Verify your LETTA_API_KEY is set correctly
   - Ensure all dependencies are installed

2. **Agent creation fails:**
   - Verify your Letta API key is valid
   - Check your internet connection
   - Ensure you have sufficient credits in your Letta account

3. **Messages not working:**
   - Check the server logs for error messages
   - Verify the agent was created successfully
   - Test with the web interface first

## Development

The server is built with:
- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Letta Client** - AI agent management

## License

This project is part of the python-ai-backend repository. 