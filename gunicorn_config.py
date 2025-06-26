"""
Gunicorn Configuration for ULTRA-FAST Production Niya Bridge
Optimized for maximum performance and reliability
"""

# Server socket - Use PORT from Render.com environment
import os
port = os.environ.get('PORT', '8000')
bind = f"0.0.0.0:{port}"
backlog = 2048

# Worker processes
workers = 2  # 2x CPU cores for optimal performance
worker_class = "sync"  # Best for CPU-bound tasks like AI inference
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100

# Timeout settings - Optimized for AI responses
timeout = 30  # Allow up to 30s for AI responses
keepalive = 2
graceful_timeout = 10

# Performance tuning
preload_app = True  # Faster startup
sendfile = True  # Faster file serving

# Logging - Minimal for speed
loglevel = "error"  # Only errors, no debug/info
errorlog = "-"  # STDERR
accesslog = None  # Disable access logs for speed

# Process naming
proc_name = "niya_bridge_production"

# Security and reliability
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Memory management
max_requests = 1000  # Restart workers after 1000 requests to prevent memory leaks
max_requests_jitter = 50

# Development vs Production
reload = False  # Disable auto-reload for production
