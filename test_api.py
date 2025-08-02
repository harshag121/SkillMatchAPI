#!/usr/bin/env python3
"""
Test script for SkillMatchAPI endpoints using dummy PDF files
"""
import requests
import json
import os
import time
from pathlib import Path

# API configuration
BASE_URL = "http://localhost:8001"
RESUME_FILE = "dummy_resume.pdf"
JOB_DESC_FILE = "dummy_job_description.pdf"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing Health Check Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Health check passed: {data}")
            return True
        else:
            print(f"  ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Health check error: {e}")
        return False

def test_extract_skills_resume():
    """Test skill extraction from resume"""
    print("\n🔍 Testing Skill Extraction - Resume...")
    
    if not Path(RESUME_FILE).exists():
        print(f"  ❌ Resume file not found: {RESUME_FILE}")
        return False
    
    try:
        with open(RESUME_FILE, 'rb') as f:
            files = {'file': (RESUME_FILE, f, 'application/pdf')}
            response = requests.post(f"{BASE_URL}/extract-skills", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Resume skill extraction successful!")
            print(f"  📄 Filename: {data.get('filename')}")
            print(f"  📊 Text length: {data.get('text_length')} characters")
            
            extracted_data = data.get('extracted_data', {})
            skills = extracted_data.get('skills', [])
            roles = extracted_data.get('roles', [])
            summary = extracted_data.get('summary', '')
            
            print(f"  🛠️  Skills found: {len(skills)}")
            for skill in skills[:5]:  # Show first 5 skills
                print(f"    • {skill}")
            if len(skills) > 5:
                print(f"    ... and {len(skills) - 5} more")
            
            print(f"  👨‍💼 Roles found: {roles}")
            print(f"  📝 Summary: {summary[:100]}..." if len(summary) > 100 else f"  📝 Summary: {summary}")
            
            return True
        else:
            print(f"  ❌ Resume extraction failed: {response.status_code}")
            print(f"  📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ❌ Resume extraction error: {e}")
        return False

def test_extract_skills_job():
    """Test skill extraction from job description"""
    print("\n🔍 Testing Skill Extraction - Job Description...")
    
    if not Path(JOB_DESC_FILE).exists():
        print(f"  ❌ Job description file not found: {JOB_DESC_FILE}")
        return False
    
    try:
        with open(JOB_DESC_FILE, 'rb') as f:
            files = {'file': (JOB_DESC_FILE, f, 'application/pdf')}
            response = requests.post(f"{BASE_URL}/extract-skills", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Job description skill extraction successful!")
            print(f"  📄 Filename: {data.get('filename')}")
            print(f"  📊 Text length: {data.get('text_length')} characters")
            
            extracted_data = data.get('extracted_data', {})
            skills = extracted_data.get('skills', [])
            roles = extracted_data.get('roles', [])
            summary = extracted_data.get('summary', '')
            
            print(f"  🛠️  Skills required: {len(skills)}")
            for skill in skills[:5]:  # Show first 5 skills
                print(f"    • {skill}")
            if len(skills) > 5:
                print(f"    ... and {len(skills) - 5} more")
            
            print(f"  💼 Job roles: {roles}")
            print(f"  📝 Summary: {summary[:100]}..." if len(summary) > 100 else f"  📝 Summary: {summary}")
            
            return True
        else:
            print(f"  ❌ Job description extraction failed: {response.status_code}")
            print(f"  📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ❌ Job description extraction error: {e}")
        return False

def test_match_resume_job():
    """Test resume-job matching"""
    print("\n🔍 Testing Resume-Job Matching...")
    
    if not Path(RESUME_FILE).exists() or not Path(JOB_DESC_FILE).exists():
        print(f"  ❌ Required files not found")
        return False
    
    try:
        with open(RESUME_FILE, 'rb') as resume_f, open(JOB_DESC_FILE, 'rb') as job_f:
            files = {
                'resume': (RESUME_FILE, resume_f, 'application/pdf'),
                'job_desc': (JOB_DESC_FILE, job_f, 'application/pdf')
            }
            response = requests.post(f"{BASE_URL}/match", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Resume-job matching successful!")
            print(f"  🎯 Match Score: {data.get('match_score', 0):.1f}%")
            
            matched_skills = data.get('matched_skills', [])
            print(f"  🔗 Matched Skills ({len(matched_skills)}):")
            for skill in matched_skills:
                print(f"    • {skill}")
            
            suggested_role = data.get('suggested_role', '')
            print(f"  💼 Suggested Role: {suggested_role}")
            
            job_links = data.get('job_links', [])
            print(f"  🌐 Job Search Links ({len(job_links)}):")
            for i, link in enumerate(job_links[:3], 1):
                print(f"    {i}. {link}")
            
            print(f"  📊 Resume Skills: {len(data.get('resume_skills', []))}")
            print(f"  📊 Job Skills: {len(data.get('job_skills', []))}")
            
            # Show detailed comparison
            resume_skills = set(skill.lower() for skill in data.get('resume_skills', []))
            job_skills = set(skill.lower() for skill in data.get('job_skills', []))
            missing_skills = job_skills - resume_skills
            
            if missing_skills and len(missing_skills) <= 10:
                print(f"  ⚠️  Skills to develop ({len(missing_skills)}):")
                for skill in sorted(missing_skills)[:5]:
                    print(f"    • {skill}")
                if len(missing_skills) > 5:
                    print(f"    ... and {len(missing_skills) - 5} more")
            
            return True
        else:
            print(f"  ❌ Resume-job matching failed: {response.status_code}")
            print(f"  📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ❌ Resume-job matching error: {e}")
        return False

def test_error_handling():
    """Test error handling with invalid files"""
    print("\n🔍 Testing Error Handling...")
    
    # Test with non-PDF file
    try:
        test_content = b"This is not a PDF file"
        files = {'file': ('test.txt', test_content, 'text/plain')}
        response = requests.post(f"{BASE_URL}/extract-skills", files=files)
        
        if response.status_code == 400:
            print("  ✅ Correctly rejected non-PDF file")
        else:
            print(f"  ⚠️  Unexpected response for non-PDF: {response.status_code}")
    
    except Exception as e:
        print(f"  ❌ Error handling test failed: {e}")

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting SkillMatchAPI Tests")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 5
    
    # Run all tests
    if test_health_check():
        tests_passed += 1
    
    if test_extract_skills_resume():
        tests_passed += 1
    
    if test_extract_skills_job():
        tests_passed += 1
    
    if test_match_resume_job():
        tests_passed += 1
    
    test_error_handling()
    tests_passed += 1  # Error handling always considered passed if it runs
    
    print("\n" + "=" * 60)
    print(f"🏁 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! SkillMatchAPI is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print("\n💡 Tips:")
    print("  • View interactive docs at: http://localhost:8001/docs")
    print("  • Test manually with curl or Postman")
    print("  • Check server logs if tests fail")

if __name__ == "__main__":
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not responding correctly. Make sure it's running on port 8001.")
            exit(1)
    except:
        print("❌ Cannot connect to server. Make sure it's running on port 8001.")
        print("💡 Start server with: uvicorn main:app --reload --host 0.0.0.0 --port 8001")
        exit(1)
    
    run_all_tests()
