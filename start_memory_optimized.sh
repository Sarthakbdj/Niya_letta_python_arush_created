#!/bin/bash

echo "🚀 Starting Memory-Optimized Niya Bridge System"
echo "=============================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Letta server is running
if ! curl -s http://localhost:8283/health > /dev/null 2>&1; then
    echo "🐳 Starting Letta server..."
    docker run -d --name letta-server \
        -p 8283:8283 \
        -e OPENAI_API_KEY=$OPENAI_API_KEY \
        --memory=1g \
        --cpus=2 \
        letta/letta:latest
    
    echo "⏳ Waiting for Letta server to be ready..."
    sleep 10
    
    # Check if server is ready
    for i in {1..30}; do
        if curl -s http://localhost:8283/health > /dev/null 2>&1; then
            echo "✅ Letta server is ready!"
            break
        fi
        echo "   Waiting... ($i/30)"
        sleep 2
    done
else
    echo "✅ Letta server is already running"
fi

# Start the memory-optimized bridge
echo "🧠 Starting Memory-Optimized Bridge..."
echo "Features enabled:"
echo "  ✓ Specialized memory blocks"
echo "  ✓ Intelligent consolidation"
echo "  ✓ Adaptive learning with confidence"
echo "  ✓ Smart context injection"
echo "  ✓ Memory health monitoring"
echo "  ✓ Predictive memory loading"
echo ""

cd core
python niya_bridge_memory_optimized.py
