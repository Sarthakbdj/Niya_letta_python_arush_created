# AI Bridge Server Integration Guide

## Overview
The AI Bridge Server (`bridge_server.py`) runs on **port 3001** and provides AI functionality to integrate with your existing app:
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:3002
- **AI Bridge**: http://localhost:3005

## API Endpoints

### Main AI Chat Endpoint
```
POST http://localhost:3005/api/ai/chat
```

**Request Body:**
```json
{
  "message": "Hello, how are you?",
  "user_id": "optional_user_id",
  "agent_type": "priya"  // "priya", "expert", or "general"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Success",
  "response": "Hey jaan! 💕 I'm doing great! How are you doing today? ✨"
}
```

### Health Check
```
GET http://localhost:3005/health
```

### WebSocket Connection
```
ws://localhost:3005/ws
```

### Bridge to Your Backend
```
GET  http://localhost:3005/api/bridge/{your_backend_path}
POST http://localhost:3005/api/bridge/{your_backend_path}
```

## Frontend Integration Examples

### React/JavaScript Example
```javascript
// AI Chat Service
class AIService {
  constructor() {
    this.baseURL = 'http://localhost:3005';
  }

  async sendMessage(message, userId = null, agentType = 'priya') {
    try {
      const response = await fetch(`${this.baseURL}/api/ai/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          user_id: userId,
          agent_type: agentType
        })
      });

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('AI Service Error:', error);
      return { success: false, error: error.message };
    }
  }

  connectWebSocket(onMessage) {
    const ws = new WebSocket(`ws://localhost:3005/ws`);
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };

    ws.onopen = () => {
      console.log('Connected to AI Bridge Server');
    };

    return ws;
  }
}

// Usage in your React component
const aiService = new AIService();

// Send a message to Priya AI girlfriend
const response = await aiService.sendMessage("Hi Priya!", "user123", "priya");
console.log(response.response); // "Hey jaan! 💕 You said: 'Hi Priya!'..."

// Send a message to Expert agent
const expertResponse = await aiService.sendMessage("Explain quantum computing", "user123", "expert");
console.log(expertResponse.response);
```

### React Component Example
```jsx
import React, { useState, useEffect } from 'react';

const AIChat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [agentType, setAgentType] = useState('priya');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { type: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
             const response = await fetch('http://localhost:3005/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          agent_type: agentType,
          user_id: 'current_user' // Use your user ID system
        })
      });

      const data = await response.json();
      
      if (data.success) {
        const aiMessage = { type: 'ai', content: data.response, agent: agentType };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        const errorMessage = { type: 'error', content: data.error };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      const errorMessage = { type: 'error', content: 'Connection failed' };
      setMessages(prev => [...prev, errorMessage]);
    }

    setInput('');
    setLoading(false);
  };

  return (
    <div className="ai-chat">
      <div className="agent-selector">
        <label>
          <input
            type="radio"
            value="priya"
            checked={agentType === 'priya'}
            onChange={(e) => setAgentType(e.target.value)}
          />
          Priya (AI Girlfriend) 💕
        </label>
        <label>
          <input
            type="radio"
            value="expert"
            checked={agentType === 'expert'}
            onChange={(e) => setAgentType(e.target.value)}
          />
          Expert Assistant 🧠
        </label>
      </div>

      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.type}`}>
            {msg.type === 'ai' && <strong>{msg.agent}: </strong>}
            {msg.content}
          </div>
        ))}
      </div>

      <div className="input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder={`Message ${agentType}...`}
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading || !input.trim()}>
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
};

export default AIChat;
```

## Running the Integration

1. **Start your existing backend** (port 3002):
   ```bash
   # Your existing backend command
   ```

2. **Start your existing frontend** (port 5173):
   ```bash
   # Your existing frontend command (probably npm run dev or similar)
   ```

3. **Start the AI Bridge Server** (port 3001):
   ```bash
   cd /path/to/Niya-python
   python bridge_server.py
   ```

## Environment Setup

Make sure you have a `.env` file with:
```env
OPENAI_API_KEY=your_openai_key
LETTA_TOKEN=your_letta_token  # Optional
PINECONE_API_KEY=your_pinecone_key  # Optional
```

## Testing the Integration

1. **Health Check:**
   ```bash
       curl http://localhost:3005/health
   ```

2. **Test AI Chat:**
   ```bash
       curl -X POST http://localhost:3005/api/ai/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello!", "agent_type": "priya"}'
   ```

3. **Test Backend Bridge:**
   ```bash
       curl http://localhost:3005/api/bridge/your-endpoint
   ```

## Agent Types

- **`priya`**: AI girlfriend with Hinglish responses, emojis, caring personality
- **`expert`**: Professional assistant for detailed questions and explanations  
- **`general`**: Basic chat assistant for general purposes

## Customization

You can modify the agent personalities in `bridge_server.py` by editing the memory blocks in the `_get_or_create_agent` method.

## Troubleshooting

- Ensure all three ports (3005, 3002, 5173) are available
- Check CORS settings if having frontend connection issues
- Verify environment variables are set correctly
- Check server logs for specific error messages 