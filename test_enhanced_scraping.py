#!/usr/bin/env python3
"""
Enhanced test script for the job scraping functionality
"""
import requests
import json
import asyncio
from job_scraper import job_scraper

async def test_job_scraper_directly():
    """Test the job scraper directly"""
    print("🧪 Testing Job Scraper Directly...")
    
    skills = ["Python", "FastAPI", "Machine Learning"]
    roles = ["Software Developer", "Senior Python Developer"]
    
    try:
        # Test Indeed scraping
        print("🔍 Testing Indeed scraping...")
        indeed_jobs = await job_scraper.scrape_indeed_jobs("Python Software Developer", max_results=5)
        print(f"  📊 Indeed results: {len(indeed_jobs)}")
        
        if indeed_jobs:
            for job in indeed_jobs[:2]:
                print(f"  ✅ {job['title']} at {job['company']}")
                print(f"     Link: {job['link']}")
        
        # Test comprehensive search
        print("\n🔍 Testing comprehensive search...")
        all_jobs = await job_scraper.search_jobs_comprehensive(skills, roles, max_results=10)
        print(f"  📊 Total results: {len(all_jobs)}")
        
        if all_jobs:
            for job in all_jobs[:3]:
                print(f"  ✅ {job['title']} at {job['company']} ({job['source']})")
                print(f"     Match keywords: {job.get('match_keywords', [])}")
        
        # Test fallback
        print("\n🔍 Testing fallback URLs...")
        fallback_jobs = await job_scraper.get_fallback_jobs(skills, roles)
        print(f"  📊 Fallback results: {len(fallback_jobs)}")
        
        for job in fallback_jobs:
            print(f"  🔗 {job['title']} - {job['source']}")
            
    except Exception as e:
        print(f"❌ Error in direct testing: {e}")

def test_api_endpoints():
    """Test API endpoints with enhanced job search"""
    print("\n🚀 Testing Enhanced API Endpoints...")
    
    # Test direct job search
    print("🔍 Testing /search-jobs endpoint...")
    payload = {
        "skills": ["Python", "FastAPI", "Django"],
        "roles": ["Software Developer"],
        "location": "United States",
        "max_results": 10
    }
    
    try:
        response = requests.post("http://localhost:8001/search-jobs", 
                               json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Search successful!")
            print(f"  📊 Jobs found: {data.get('total_jobs_found', 0)}")
            
            jobs = data.get('job_openings', [])
            for job in jobs[:3]:
                print(f"  🎯 {job['title']} at {job['company']}")
                print(f"     Source: {job['source']} | Link: {job['link']}")
        else:
            print(f"  ❌ API Error: {response.status_code}")
            print(f"  Response: {response.text}")
            
    except Exception as e:
        print(f"❌ API test error: {e}")

if __name__ == "__main__":
    print("🧪 Enhanced Job Scraping Tests")
    print("=" * 50)
    
    # Run direct scraper tests
    asyncio.run(test_job_scraper_directly())
    
    # Run API tests
    test_api_endpoints()
    
    print("\n" + "=" * 50)
    print("🏁 Enhanced testing complete!")
    print("💡 If scraping is blocked, fallback URLs will be provided.")
