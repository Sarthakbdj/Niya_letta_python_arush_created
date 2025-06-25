# Niya-Python Codebase Organization

This document provides a clear overview of the simplified codebase structure after optimization cleanup.

## Directory Structure

```
Niya-python/
├── core/                        # Core bridge service
│   ├── niya_bridge.py          # Main bridge service (Flask:1511)
│   ├── enhanced_personality.py # AI personality configuration
│   └── config.py              # Configuration management
│
├── chat/                       # Direct chat interface
│   └── priya_chat.py          # FastAPI chat interface (Port:8000)
│
├── data/                       # Data processing
│   ├── document_processor.py  # Document processing utilities
│   └── pineconedb.py         # Vector database integration
│
├── launchers/                  # System launchers
│   ├── run_niya_complete.py   # Complete system launcher
│   └── run_priya.py           # Simple chat launcher
│
├── testing/                    # Testing & monitoring
│   ├── test_frontend_flow.py  # Integration tests
│   └── monitor_messages.py    # Activity monitoring
│
├── docs/                       # Documentation
│   ├── ENHANCED_PERSONALITY_GUIDE.md
│   ├── INTEGRATION_GUIDE.md
│   ├── README_PRIYA.md
│   └── README_SERVER.md
│
├── deployment/                 # Deployment files
│   ├── docker-compose.yml     # Docker setup
│   ├── Dockerfile.bridge      # Bridge container
│   ├── Dockerfile.chat        # Chat container
│   └── static/                # Web assets
│
├── archive/                    # Archived components
│   └── Niya_raghav_sarthak_baby/
│
├── run_niya.py                # Main launcher
├── requirements.txt           # Dependencies
├── .env                      # Environment variables
├── README.md                 # Main documentation
└── CODEBASE_SUMMARY.md       # System summary
```

## Core Components

### Bridge Service (`core/niya_bridge.py`)
- **Purpose**: Main integration service for Niya backend
- **Port**: 1511
- **Performance**: 84% responses under 7 seconds
- **Configuration**: gpt-4o-mini, no tools, cloud/local mode

### Enhanced Personality (`core/enhanced_personality.py`)
- **Purpose**: AI personality and memory configuration
- **Features**: 6 memory blocks, Hinglish communication
- **Integration**: Used by both bridge and chat services

### Chat Interface (`chat/priya_chat.py`)
- **Purpose**: Direct web chat interface
- **Port**: 8000
- **Features**: WebSocket support, web UI

## Usage Patterns

### Primary Usage (Production)
```bash
python run_niya.py              # Start bridge service
```

### Development/Testing
```bash
python run_niya.py --chat       # Direct chat interface
python run_niya.py --complete   # Both services
python run_niya.py --test       # Integration tests
python run_niya.py --monitor    # Activity monitoring
```

## Configuration Management

### Environment Variables
- `OPENAI_API_KEY` - Required for AI functionality
- `LETTA_TOKEN` - For Letta Cloud mode (recommended)
- `LETTA_BASE_URL` - For local Letta server
- `LETTA_MODE` - 'cloud' or 'local'

### Mode Switching
The system automatically detects configuration:
- Cloud mode: When `LETTA_TOKEN` is set
- Local mode: When `LETTA_BASE_URL` is set

## API Endpoints

### Bridge Service (Port 1511)
- `POST /message` - Main Niya backend integration
- `GET /health` - Service health check
- `POST /reset` - Reset AI agent

### Chat Interface (Port 8000)
- `GET /` - Web chat interface
- `WebSocket /ws` - Real-time chat
- `GET /api/agent-info` - Agent information

## Performance Characteristics

### Optimized Configuration
- **Model**: gpt-4o-mini (optimal speed/quality balance)
- **Tools**: None (for maximum speed)
- **Memory**: 6 focused memory blocks
- **Architecture**: Simple Flask bridge (no optimization layers)

### Measured Performance
- **Under 7s Rate**: 84% (21/25 messages)
- **Average Response**: 6.11 seconds
- **Success Rate**: 100%
- **Fastest Response**: 4.40 seconds

## Development Guidelines

### Adding Features
1. Maintain the simple architecture
2. Avoid adding optimization layers
3. Test performance impact
4. Update documentation

### File Organization
- Keep core functionality in `core/`
- Separate concerns clearly
- Maintain backward compatibility
- Document all changes

## Deployment

### Local Development
```bash
pip install -r requirements.txt
python run_niya.py
```

### Production (Cloud Mode)
```bash
export LETTA_TOKEN=your_token
export LETTA_MODE=cloud
python run_niya.py
```

### Docker Deployment
```bash
docker-compose up --build
```

## Testing Strategy

### Integration Testing
- Full frontend → backend → bridge flow
- Performance testing (25 message batches)
- Error handling and recovery

### Monitoring
- Real-time activity monitoring
- Performance metrics tracking
- Health check endpoints

This simplified structure provides optimal performance while maintaining clarity and maintainability. 