from letta_client import Letta
import os
from dotenv import load_dotenv
import json

load_dotenv()

def print_success(message):
    """Print a success message with green color"""
    print(f"\033[92m✓ {message}\033[0m")

def print_info(message):
    """Print an info message with blue color"""
    print(f"\033[94mℹ {message}\033[0m")

def print_error(message):
    """Print an error message with red color"""
    print(f"\033[91m✗ {message}\033[0m")

def print_separator():
    """Print a separator line"""
    print("\n" + "="*50 + "\n")

def create_agent():
    """Create a new Letta agent with custom configuration"""
    print_info("Creating new Letta agent...")
    
    try:
        agent = client.agents.create(
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
        
        print_success(f"Agent created successfully!")
        print_info(f"Agent ID: {agent.id}")
        print_info(f"Agent Name: {agent.name}")
        return agent
        
    except Exception as e:
        print_error(f"Failed to create agent: {e}")
        return None

def send_message_to_agent(agent_id, message_content):
    """Send a message to a specific agent"""
    print_info(f"Sending message: '{message_content}'")
    
    try:
        response = client.agents.messages.create(
            agent_id=agent_id,
            messages=[{"role": "user", "content": message_content}],
        )
        
        print_success("Message sent successfully!")
        return response
        
    except Exception as e:
        print_error(f"Failed to send message: {e}")
        return None

def main():
    """Main function to run the Letta bot"""
    print_separator()
    print("🤖 Letta Bot - AI Agent Manager")
    print_separator()
    
    # Check if API key is available
    api_key = os.getenv("LETTA_API_KEY")
    if not api_key:
        print_error("LETTA_API_KEY not found in environment variables")
        print_info("Please create a .env file with your LETTA_API_KEY")
        return
    
    print_info("API key found, initializing Letta client...")
    
    # Initialize client
    global client
    client = Letta(token=api_key)
    
    # Create agent
    agent = create_agent()
    if not agent:
        return
    
    print_separator()
    
    # Send a test message
    print(send_message_to_agent(agent.id, "Hello! How are you today?").messages[-1].content)
    
    print_separator()
    print_success("Letta bot operations completed!")

if __name__ == "__main__":
    main()


# response = client.templates.agents.create(
#     project="default-project",
#     template_version="sorry-yellow-blackbird:latest",
# )

# # message agent
# client.agents.messages.create(
#     agent_id=response.agents[0].id,
#     messages=[{"role": "user", "content": "hello"}],
# )








