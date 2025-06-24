#!/usr/bin/env python3
"""
Setup script to help create the .env file for the Letta bot
"""

import os
import getpass

def print_colored(message, color_code):
    """Print a colored message"""
    print(f"\033[{color_code}m{message}\033[0m")

def print_success(message):
    print_colored(f"✓ {message}", "92")

def print_info(message):
    print_colored(f"ℹ {message}", "94")

def print_warning(message):
    print_colored(f"⚠ {message}", "93")

def create_env_file():
    """Create a .env file with user input"""
    print("🤖 Letta Bot Environment Setup")
    print("=" * 40)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print_warning(".env file already exists!")
        overwrite = input("Do you want to overwrite it? (y/N): ").lower().strip()
        if overwrite != 'y':
            print_info("Setup cancelled.")
            return
    
    print_info("Please provide your API keys:")
    print_info("You can get your Letta API key from: https://app.letta.com/")
    print_info("You can get your OpenAI API key from: https://platform.openai.com/api-keys")
    print_info("You can get your Pinecone API key from: https://www.pinecone.io/")
    print()
    
    # Get API keys
    letta_key = getpass.getpass("Enter your LETTA_API_KEY: ").strip()
    openai_key = getpass.getpass("Enter your OPENAI_API_KEY: ").strip()
    pinecone_key = getpass.getpass("Enter your PINECONE_API_KEY: ").strip()
    
    # Create .env content
    env_content = f"""# Letta API Key - Get from https://app.letta.com/
LETTA_API_KEY={letta_key}

# OpenAI API Key - Get from https://platform.openai.com/api-keys
OPENAI_API_KEY={openai_key}

# Pinecone API Key - Get from https://www.pinecone.io/
PINECONE_API_KEY={pinecone_key}

# Pinecone Index Name (will be created automatically)
PINECONE_INDEX_NAME=expert-agent-knowledge

# OpenAI Embedding Model
EMBEDDING_MODEL=text-embedding-ada-002
"""
    
    # Write to .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print_success(".env file created successfully!")
        print_info("You can now run: python lettabot.py")
    except Exception as e:
        print_colored(f"✗ Error creating .env file: {e}", "91")

if __name__ == "__main__":
    create_env_file() 