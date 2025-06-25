#!/bin/bash
"""
Production Startup Script for Niya Bridge
Starts all services in production mode
"""

echo "�� Starting PRODUCTION Niya Bridge System..."
echo "========================================"

# Check Docker
if ! docker --version > /dev/null 2>&1; then
    echo "❌ Docker not installed"
    exit 1
fi

# Start optimized Letta server if not running
if ! docker ps | grep -q letta-server; then
    echo "🐳 Starting optimized Letta server..."
    source .env
    docker run -d --name letta-server \
        -p 8283:8283 \
        -e OPENAI_API_KEY="$OPENAI_API_KEY" \
        -e LETTA_LLM_ENDPOINT="https://api.openai.com/v1" \
        -e LETTA_LLM_MODEL="gpt-4o-mini" \
        --memory="1g" \
        --cpus="2" \
        letta/letta:latest
    echo "⏳ Waiting for Letta server startup..."
    sleep 20
fi

# Start Redis cache if not running
if ! docker ps | grep -q niya-redis-cache; then
    echo "🗄️ Starting Redis cache..."
    docker run -d --name niya-redis-cache \
        -p 6379:6379 \
        --memory="256m" \
        redis:7-alpine
fi

# Stop any existing bridge services
echo "🔄 Stopping existing bridge services..."
pkill -f gunicorn 2>/dev/null || true
pkill -f niya_bridge 2>/dev/null || true

# Start production bridge with Gunicorn
echo "⚡ Starting PRODUCTION Gunicorn bridge..."
cd core
gunicorn -c ../gunicorn_config.py production_app:application --daemon

# Wait and verify
sleep 5
if curl -s http://localhost:1511/health > /dev/null; then
    echo "✅ PRODUCTION system started successfully!"
    echo "🔗 Bridge running on: http://localhost:1511"
    echo "📊 Health check: curl http://localhost:1511/health"
    echo "🐳 Docker containers:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
else
    echo "❌ Bridge startup failed"
    exit 1
fi
