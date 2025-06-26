#!/usr/bin/env python3
"""
Priya Chat Application - Main Entry Point for Render.com
Flask-based AI girlfriend chat service optimized for production deployment
"""

import os
import sys
from pathlib import Path

# Add core directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent / 'core'))

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
from dotenv import load_dotenv

# Import the optimized bridge
from niya_bridge import NiyaBridge

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
           static_folder='deployment/static',
           template_folder='deployment/static')
CORS(app)

# Initialize the bridge service
bridge = NiyaBridge()

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint for Render.com"""
    return jsonify({
        'status': 'healthy',
        'service': 'Priya Chat Application',
        'version': '1.0.0'
    })

@app.route('/api/message', methods=['POST'])
def api_message():
    """API endpoint for chat messages"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400
            
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Empty message'
            }), 400
        
        # Get response from Priya AI
        response = bridge.get_priya_response(user_message)
        
        return jsonify({
            'success': True,
            'response': response,
            'agent_id': bridge.agent_id
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/reset', methods=['POST'])
def api_reset():
    """Reset the AI agent"""
    try:
        bridge.create_agent()
        return jsonify({
            'success': True,
            'message': 'Agent reset successfully',
            'agent_id': bridge.agent_id
        })
    except Exception as e:
        logger.error(f"Reset error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def initialize_app():
    """Initialize the application for production"""
    try:
        logger.info("🚀 Initializing Priya Chat Application...")
        
        # Initialize the bridge service
        success = bridge.initialize()
        if not success:
            logger.error("Failed to initialize bridge service")
            return False
            
        logger.info("✅ Priya Chat Application initialized successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize application: {e}")
        return False

if __name__ == '__main__':
    # Initialize the application
    if initialize_app():
        # Get port from environment (Render.com sets this)
        port = int(os.environ.get('PORT', 8000))
        
        logger.info(f"🌟 Starting Priya Chat Application on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        logger.error("❌ Failed to start application")
        sys.exit(1) 