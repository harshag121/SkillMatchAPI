#!/usr/bin/env python3
"""
Quick test script to verify SkillMatchAPI setup
"""
import os
import sys
import requests
import time
from pathlib import Path

def test_api_health():
    """Test if the API is running and responsive"""
    try:
        response = requests.get("http://localhost:8001/docs", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def test_frontend_access():
    """Test if frontend files are accessible"""
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        return response.status_code == 200 and "SkillMatch" in response.text
    except requests.exceptions.RequestException:
        return False

def test_file_upload():
    """Test file upload functionality"""
    try:
        # Check if dummy files exist
        if not Path("dummy_resume.pdf").exists():
            return False, "Dummy files not found"
        
        with open("dummy_resume.pdf", "rb") as f:
            files = {"file": f}
            response = requests.post("http://localhost:8001/extract-skills", 
                                   files=files, timeout=30)
        
        return response.status_code == 200, response.text
    except requests.exceptions.RequestException as e:
        return False, str(e)

def main():
    """Run all tests"""
    print("🧪 Testing SkillMatchAPI Setup")
    print("=" * 40)
    
    # Test 1: API Health
    print("1. Testing API Health...")
    if test_api_health():
        print("   ✅ API is running and accessible")
    else:
        print("   ❌ API is not accessible")
        print("   💡 Make sure the server is running: python3 run.py")
        return
    
    # Test 2: Frontend Access
    print("2. Testing Frontend Access...")
    if test_frontend_access():
        print("   ✅ Frontend is accessible")
    else:
        print("   ❌ Frontend is not accessible")
    
    # Test 3: File Upload
    print("3. Testing File Upload...")
    success, message = test_file_upload()
    if success:
        print("   ✅ File upload works")
    else:
        print(f"   ❌ File upload failed: {message}")
    
    print("\n🎉 Testing complete!")
    print("\nAccess your application at:")
    print("🌐 Frontend: http://localhost:8001/")
    print("📚 API Docs: http://localhost:8001/docs")
    print("🧪 Test Interface: http://localhost:8001/test")

if __name__ == "__main__":
    main()
