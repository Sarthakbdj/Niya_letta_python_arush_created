import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:1511"

def test_api():
    """Test the Letta Agent API"""
    print("🧪 Testing Letta Agent API...")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Get agent info
    print("\n2. Testing agent info...")
    try:
        response = requests.get(f"{BASE_URL}/agent/info")
        if response.status_code == 200:
            agent_info = response.json()
            print("✅ Agent info retrieved")
            print(f"   Agent ID: {agent_info['id']}")
            print(f"   Agent Name: {agent_info['name']}")
            print(f"   Model: {agent_info['model']}")
        else:
            print(f"❌ Agent info failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Agent info error: {e}")
        return False
    
    # Test 3: Send a message
    print("\n3. Testing message sending...")
    try:
        message_data = {
            "message": "Hello! Can you tell me a short joke?"
        }
        response = requests.post(
            f"{BASE_URL}/message",
            headers={"Content-Type": "application/json"},
            data=json.dumps(message_data)
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Message sent successfully")
                print(f"   Agent Response: {result['response'][:100]}...")
            else:
                print(f"❌ Message failed: {result['error']}")
                return False
        else:
            print(f"❌ Message request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Message error: {e}")
        return False
    
    # Test 4: List agents
    print("\n4. Testing list agents...")
    try:
        response = requests.get(f"{BASE_URL}/agents")
        if response.status_code == 200:
            agents = response.json()
            print(f"✅ Found {len(agents)} agents")
            for agent in agents:
                print(f"   - {agent['name']} ({agent['id']})")
        else:
            print(f"❌ List agents failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ List agents error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    return True

if __name__ == "__main__":
    print("Make sure the server is running on port 1511 before running this test.")
    print("You can start the server with: python server.py")
    print()
    
    input("Press Enter to start testing...")
    test_api() 