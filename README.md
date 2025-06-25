# Niya-Python Bridge - SPEED OPTIMIZED

**AI Girlfriend Integration for Niya Platform - Bridge Service Only**

## Overview

This repository provides the **SPEED-OPTIMIZED Python bridge service** that connects the Niya frontend/backend to Priya AI girlfriend using Letta Cloud. The system is now optimized for **95%+ of responses under 7 seconds**.

## Architecture

```
Frontend (React/Vue) → Niya Backend (NestJS:3002) → Python Bridge (Flask:1511) → Letta Cloud → Priya AI
```

## ⚡ Speed Optimizations

### **MAJOR PERFORMANCE IMPROVEMENTS**:
- ✅ **Request spacing**: Reduced from 2.0s to 0.5s (75% faster)
- ✅ **Memory blocks**: Reduced from 6 to 2 (faster processing)
- ✅ **No embedding processing**: Removed for speed
- ✅ **No multi-message overhead**: Single response only
- ✅ **Single attempt**: No retry delays
- ✅ **Minimal logging**: Reduced verbosity
- ✅ **No chat service dependencies**: Bridge only
- ✅ **Minimal requirements**: Only essential packages

### **Target Performance**: 95%+ responses under 7 seconds

## Quick Start

1. **Install Dependencies** (Minimal Set)
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Start Bridge Service** (Speed Optimized)
   ```bash
   python run_niya.py
   ```

## Configuration

### Cloud Mode (Recommended for Speed)
Set in `.env`:
```env
LETTA_TOKEN=your_letta_cloud_token
OPENAI_API_KEY=your_openai_key
```

### Local Mode (Development Only)
Set in `.env`:
```env
LETTA_BASE_URL=http://localhost:8283
OPENAI_API_KEY=your_openai_key
```

## Usage

| Command | Description |
|---------|-------------|
| `python run_niya.py` | Start bridge service (default, speed optimized) |
| `python run_niya.py --bridge` | Start bridge service only |
| `python run_niya.py --test` | Test integration flow |
| `python run_niya.py --monitor` | Monitor activity |
| `python run_niya.py --help` | Show help |

## Performance Benchmarks

### Before Optimization:
- **Under 7s Rate**: 84% (21/25 messages)
- **Average Response**: 6.11 seconds
- **Request Spacing**: 2.0 seconds
- **Memory Blocks**: 6 blocks
- **Retry Logic**: 2 attempts with delays

### After Speed Optimization:
- **Target Under 7s Rate**: 95%+ 
- **Expected Average**: <5.5 seconds
- **Request Spacing**: 0.5 seconds (75% faster)
- **Memory Blocks**: 2 blocks (minimal)
- **Retry Logic**: Single attempt (no delays)

## API Endpoints

### Bridge Service (Port 1511) - Speed Optimized

- `POST /message` - Main endpoint for Niya backend (single response)
- `GET /health` - Health check
- `POST /reset` - Reset AI agent

**Request Format**:
```json
{
  "message": "Hello Priya!"
}
```

**Response Format**:
```json
{
  "success": true,
  "response": "Hey jaan! How are you doing today? 💕",
  "error": null
}
```

## Core Components (Streamlined)

```
core/
├── niya_bridge.py           # Main bridge service (SPEED OPTIMIZED)
└── enhanced_personality.py  # Minimal AI personality configuration

testing/
├── test_frontend_flow.py    # Integration tests
└── monitor_messages.py      # Activity monitoring

deployment/
└── docker-compose.fast.yml  # Docker deployment (optional)
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | Yes |
| `LETTA_TOKEN` | Letta Cloud token (recommended) | For cloud mode |
| `LETTA_BASE_URL` | Local Letta server URL | For local mode |

## Development

### Testing (Speed Optimized)
```bash
# Test integration flow (fast)
python run_niya.py --test

# Monitor activity (real-time)
python run_niya.py --monitor
```

### Local Development
```bash
# Start local Letta server first (if using local mode)
letta server

# Then start bridge in local mode
LETTA_BASE_URL=http://localhost:8283 python run_niya.py
```

## Production Deployment

### Cloud Mode (Recommended for Speed)
```bash
# Install minimal dependencies
pip install -r requirements.txt

# Set production environment
export LETTA_TOKEN=your_production_token
export OPENAI_API_KEY=your_openai_key

# Start speed-optimized service
python run_niya.py
```

### Docker (Optional - for local Letta)
```bash
docker-compose -f deployment/docker-compose.fast.yml up --build
```

## Removed Components (For Speed)

### Removed Services:
- ❌ Chat interface (was on port 8000)
- ❌ Complete launcher 
- ❌ Multi-message processing
- ❌ Streaming endpoints

### Removed Dependencies:
- ❌ FastAPI, Uvicorn, WebSockets
- ❌ Data processing libraries (PyPDF2, python-docx)
- ❌ Vector database libraries (Pinecone)
- ❌ Gunicorn (using minimal waitress)

### Removed Features:
- ❌ Embedding processing
- ❌ Retry logic with delays
- ❌ Complex memory management
- ❌ Multi-message breaking
- ❌ Verbose logging

## Troubleshooting

### Performance Issues
1. **Still slow responses?**
   - Ensure using `LETTA_TOKEN` (cloud mode)
   - Check network connectivity
   - Verify minimal dependencies installed

2. **Connection errors?**
   - Verify API keys in `.env`
   - Check Letta Cloud service status
   - Ensure proper network access

### Monitoring
The bridge provides real-time performance logging:
- Request/response timing
- Optimization status
- Error diagnostics

## Architecture Benefits

### Speed Optimizations:
- **Minimal Dependencies**: Only essential packages
- **Streamlined Processing**: No unnecessary overhead
- **Direct API Calls**: No complex retry logic
- **Reduced Memory Usage**: Minimal personality blocks
- **Fast Startup**: No chat service initialization

### Maintained Features:
- ✅ Full Niya backend integration
- ✅ AI girlfriend personality (optimized)
- ✅ Error handling and health checks
- ✅ Development and testing tools
- ✅ Docker deployment support

## Support

For issues and questions about the speed-optimized bridge:
- Focus on bridge service only (no chat interface)
- Performance issues related to <7s response target
- Integration with Niya backend

**This speed-optimized version is designed specifically for production use with the Niya platform, prioritizing response speed over additional features.** 