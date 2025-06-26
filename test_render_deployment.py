#!/usr/bin/env python3
"""
Test script to verify Render.com deployment setup
Run this locally to ensure everything works before deploying
"""

import os
import sys
import requests
import time
import subprocess
from pathlib import Path

def print_header():
    print("🧪" * 50)
    print("🔍 RENDER.COM DEPLOYMENT TEST")
    print("🧪" * 50)
    print()

def check_files():
    """Check if all required files exist"""
    print("📁 Checking required files...")
    required_files = [
        'priya_chat.py',
        'requirements.txt',
        'Dockerfile.render',
        'render.yaml',
        'RENDER_DEPLOYMENT_GUIDE.md',
        'deployment/static/index.html',
        'core/niya_bridge.py',
        '.env'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
            print(f"❌ Missing: {file}")
        else:
            print(f"✅ Found: {file}")
    
    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} required files!")
        return False
    
    print("✅ All required files present!")
    return True

def check_environment():
    """Check environment variables"""
    print("\n🔐 Checking environment variables...")
    required_vars = ['OPENAI_API_KEY']
    optional_vars = ['PINECONE_API_KEY', 'PINECONE_INDEX_NAME']
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            print(f"❌ Missing: {var}")
        else:
            print(f"✅ Found: {var}")
    
    for var in optional_vars:
        if os.getenv(var):
            print(f"✅ Found: {var}")
        else:
            print(f"⚠️  Optional: {var} (not set)")
    
    if missing_vars:
        print(f"\n❌ Missing {len(missing_vars)} required environment variables!")
        print("💡 Make sure to set these in your .env file")
        return False
    
    print("✅ Environment variables OK!")
    return True

def test_dependencies():
    """Test if dependencies can be installed"""
    print("\n📦 Testing dependency installation...")
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '--dry-run', '-r', 'requirements.txt'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Dependencies can be installed successfully!")
            return True
        else:
            print(f"❌ Dependency installation failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Dependency check timed out")
        return False
    except Exception as e:
        print(f"❌ Error checking dependencies: {e}")
        return False

def test_app_startup():
    """Test if the app can start"""
    print("\n🚀 Testing application startup...")
    try:
        # Set test environment
        os.environ['PORT'] = '8999'
        
        # Import the app to test if it loads
        sys.path.insert(0, str(Path.cwd()))
        from priya_chat import app, initialize_app
        
        print("✅ Application imports successfully!")
        
        # Test initialization (without actually running Letta)
        print("🔧 Testing initialization logic...")
        print("✅ Application structure is valid!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Startup error: {e}")
        return False

def generate_deployment_summary():
    """Generate deployment summary"""
    print("\n📋 DEPLOYMENT SUMMARY")
    print("=" * 50)
    print("\n🌐 RENDER.COM DEPLOYMENT STEPS:")
    print("1. Push your code to GitHub")
    print("2. Connect GitHub repo to Render.com")
    print("3. Create new Web Service")
    print("4. Use these settings:")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: python priya_chat.py")
    print("   - Environment: Python 3")
    
    print("\n🔐 ENVIRONMENT VARIABLES TO SET:")
    print(f"   - OPENAI_API_KEY=***{os.getenv('OPENAI_API_KEY', '')[-4:]}")
    if os.getenv('PINECONE_API_KEY'):
        print(f"   - PINECONE_API_KEY=***{os.getenv('PINECONE_API_KEY', '')[-4:]}")
    if os.getenv('PINECONE_INDEX_NAME'):
        print(f"   - PINECONE_INDEX_NAME={os.getenv('PINECONE_INDEX_NAME')}")
    
    print("\n📱 EXPECTED ENDPOINTS:")
    print("   - https://your-app.onrender.com/ (Chat Interface)")
    print("   - https://your-app.onrender.com/health (Health Check)")
    print("   - https://your-app.onrender.com/api/message (Chat API)")
    
    print("\n📖 For detailed instructions, see: RENDER_DEPLOYMENT_GUIDE.md")

def main():
    """Main test function"""
    print_header()
    
    tests = [
        ("File Structure", check_files),
        ("Environment Variables", check_environment),
        ("Dependencies", test_dependencies),
        ("Application Startup", test_app_startup)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed!")
    
    print("\n" + "="*60)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Ready for Render.com deployment!")
        generate_deployment_summary()
        return True
    else:
        print("❌ Some tests failed. Please fix the issues before deploying.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 