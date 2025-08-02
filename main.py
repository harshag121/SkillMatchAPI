import os
import fitz  # PyMuPDF
import aiohttp
import google.generativeai as genai
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from dotenv import load_dotenv
import json
import asyncio
from datetime import datetime
from job_scraper import job_scraper

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise EnvironmentError('GEMINI_API_KEY not set')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI(
    title="SkillMatchAPI",
    description="A scalable FastAPI backend that uses Gemini API for skill extraction from PDFs and searches for job openings",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

# Add routes for serving static files and test interface
@app.get("/")
async def root():
    """Redirect to frontend"""
    return FileResponse("frontend/index.html")

@app.get("/test")
async def test_interface():
    """Serve the test interface HTML page"""
    return FileResponse("test_interface.html")

@app.get("/dummy_resume.pdf")
async def get_dummy_resume():
    """Serve the dummy resume PDF for testing"""
    return FileResponse("dummy_resume.pdf", media_type="application/pdf")

@app.get("/dummy_job_description.pdf") 
async def get_dummy_job_description():
    """Serve the dummy job description PDF for testing"""
    return FileResponse("dummy_job_description.pdf", media_type="application/pdf")

def extract_text_from_pdf(file: UploadFile) -> str:
    """Extract text content from uploaded PDF file"""
    doc = fitz.open(stream=file.file.read(), filetype='pdf')
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text

async def extract_skills(text: str) -> dict:
    """Use Gemini API to extract skills, roles, and summary from text"""
    prompt = f"""
    Given the following resume or job description:
    ---
    {text}
    ---
    Extract:
    - Key skills (as a list of strings)
    - Suggested job roles (as a list of strings)
    - Summary of capabilities (as a string)
    
    Return ONLY a valid JSON object with fields: skills, roles, summary.
    Do not include any markdown formatting or additional text.
    """
    
    try:
        response = model.generate_content(prompt)
        response_text = response.candidates[0].content.parts[0].text
        
        # Clean up the response to ensure it's valid JSON
        response_text = response_text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        return json.loads(response_text)
    except (json.JSONDecodeError, Exception) as e:
        # Fallback in case Gemini doesn't return valid JSON
        return {
            "skills": ["Unable to parse skills"],
            "roles": ["Unable to parse roles"],
            "summary": f"Error parsing content: {str(e)}"
        }

async def search_jobs(query: str, skills: List[str] = None, roles: List[str] = None, location: str = "United States") -> List[dict]:
    """Search for real job openings using web scraping"""
    try:
        # Use comprehensive job search
        if skills and roles:
            jobs = await job_scraper.search_jobs_comprehensive(skills, roles, location, max_results=15)
        else:
            # Fallback to basic search
            jobs = await job_scraper.scrape_indeed_jobs(query, location, max_results=10)
        
        # If no jobs found, provide fallback search URLs
        if not jobs and skills and roles:
            jobs = await job_scraper.get_fallback_jobs(skills, roles)
        
        return jobs
    except Exception as e:
        print(f"Job search error: {e}")
        # Return fallback URLs if scraping fails
        if skills and roles:
            return await job_scraper.get_fallback_jobs(skills, roles)
        else:
            return [{
                "title": "Job Search Results",
                "company": "Multiple Companies",
                "location": "Various",
                "salary": "Competitive",
                "link": f"https://www.indeed.com/jobs?q={query.replace(' ', '+')}",
                "source": "Indeed",
                "posted_date": "Live Results",
                "snippet": "Click to view current job openings",
                "match_keywords": []
            }]

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "SkillMatchAPI is running", "status": "healthy"}

@app.post("/match")
async def match(resume: UploadFile = File(...), job_desc: UploadFile = File(...)):
    """
    Match resume with job description using Gemini API for skill extraction
    and return job search links
    """
    try:
        # Validate file types
        if not resume.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Resume must be a PDF file")
        if not job_desc.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Job description must be a PDF file")
        
        # Extract text from PDFs
        resume_text = extract_text_from_pdf(resume)
        job_text = extract_text_from_pdf(job_desc)
        
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Resume PDF appears to be empty or unreadable")
        if not job_text.strip():
            raise HTTPException(status_code=400, detail="Job description PDF appears to be empty or unreadable")
        
        # Extract skills and roles using Gemini API
        resume_data, job_data = await asyncio.gather(
            extract_skills(resume_text),
            extract_skills(job_text)
        )
        
        # Calculate matching skills
        resume_skills = set([skill.lower().strip() for skill in resume_data.get('skills', [])])
        job_skills = set([skill.lower().strip() for skill in job_data.get('skills', [])])
        
        matched_skills = list(resume_skills & job_skills)
        total_job_skills = len(job_skills)
        score = (len(matched_skills) / total_job_skills * 100) if total_job_skills > 0 else 0
        
        # Generate job search query
        suggested_role = job_data.get('roles', [''])[0] if job_data.get('roles') else ''
        top_skills = list(job_skills)[:5]  # Use top 5 skills for search
        job_query = f"{suggested_role} {' '.join(top_skills)}" if suggested_role else ' '.join(top_skills)
        
        # Get real job openings with scraping
        job_openings = await search_jobs(
            job_query, 
            skills=list(job_skills), 
            roles=job_data.get('roles', []), 
            location="United States"
        )
        
        return JSONResponse({
            "resume_summary": resume_data.get('summary', ''),
            "job_summary": job_data.get('summary', ''),
            "resume_skills": resume_data.get('skills', []),
            "job_skills": job_data.get('skills', []),
            "matched_skills": matched_skills,
            "match_score": round(score, 2),
            "suggested_role": suggested_role,
            "job_search_query": job_query,
            "job_openings": job_openings,  # Real job listings with clickable links
            "total_jobs_found": len(job_openings),
            "resume_roles": resume_data.get('roles', []),
            "job_roles": job_data.get('roles', [])
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/extract-skills")
async def extract_skills_endpoint(file: UploadFile = File(...)):
    """
    Extract skills from a single PDF file (resume or job description)
    """
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        text = extract_text_from_pdf(file)
        if not text.strip():
            raise HTTPException(status_code=400, detail="PDF appears to be empty or unreadable")
        
        skills_data = await extract_skills(text)
        
        return JSONResponse({
            "filename": file.filename,
            "extracted_data": skills_data,
            "text_length": len(text)
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/search-jobs")
async def search_jobs_endpoint(
    skills: List[str], 
    roles: List[str] = None, 
    location: str = "United States", 
    max_results: int = 15
):
    """
    Search for job openings based on skills and roles
    """
    try:
        if not skills:
            raise HTTPException(status_code=400, detail="At least one skill is required")
        
        # Search for jobs
        job_openings = await search_jobs(
            query=" ".join(skills[:3]),
            skills=skills,
            roles=roles or [],
            location=location
        )
        
        return JSONResponse({
            "search_query": {
                "skills": skills,
                "roles": roles or [],
                "location": location,
                "max_results": max_results
            },
            "total_jobs_found": len(job_openings),
            "job_openings": job_openings[:max_results],
            "search_timestamp": datetime.now().isoformat()
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job search error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
