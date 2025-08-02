#!/usr/bin/env python3
"""
Test script to verify the SkillMatchAPI setup
"""
import sys
import os
import requests
import time
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all required packages are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'google.generativeai', 
        'fitz', 'aiohttp', 'dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'fitz':
                import fitz
            elif package == 'google.generativeai':
                import google.generativeai
            elif package == 'dotenv':
                from dotenv import load_dotenv
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def check_env_file():
    """Check if .env file exists and has GEMINI_API_KEY"""
    print("\n🔍 Checking environment configuration...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("  ❌ .env file not found")
        print("  📝 Create .env file with: cp .env.example .env")
        print("  📝 Then add your GEMINI_API_KEY to .env")
        return False
    
    # Check if GEMINI_API_KEY is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("  ❌ GEMINI_API_KEY not set or using placeholder value")
        print("  📝 Add your actual Gemini API key to .env file")
        print("  📝 Get API key from: https://aistudio.google.com/app/apikey")
        return False
    
    print("  ✅ .env file exists")
    print("  ✅ GEMINI_API_KEY is set")
    return True

def test_server_start():
    """Test if the server can start"""
    print("\n🔍 Testing server startup...")
    
    try:
        # Import to check for basic syntax errors
        from main import app
        print("  ✅ main.py imports successfully")
        print("  ✅ FastAPI app created successfully")
        return True
    except Exception as e:
        print(f"  ❌ Error importing main.py: {e}")
        return False

def run_health_check():
    """Run a health check against the server"""
    print("\n🔍 Testing server health check...")
    
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Server responded: {data}")
            return True
        else:
            print(f"  ❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("  ❌ Could not connect to server at http://localhost:8000")
        print("  📝 Make sure server is running: uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"  ❌ Error testing server: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 SkillMatchAPI Setup Test")
    print("=" * 50)
    
    all_good = True
    
    # Test 1: Dependencies
    if not check_dependencies():
        all_good = False
    
    # Test 2: Environment
    if not check_env_file():
        all_good = False
    
    # Test 3: Server startup
    if not test_server_start():
        all_good = False
    
    # Test 4: Health check (only if server is running)
    server_running = run_health_check()
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 Setup looks good!")
        if not server_running:
            print("\n📝 To start the server, run:")
            print("   source .venv/bin/activate")
            print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        else:
            print("🌐 Server is running at: http://localhost:8000")
            print("📚 API docs at: http://localhost:8000/docs")
    else:
        print("❌ Setup issues found. Please fix the issues above.")
    
    print("\n📖 For more information, see README.md")

if __name__ == "__main__":
    main()
