# SkillMatchAPI - AI-Powered Resume & Job Matching Platform

A comprehensive full-stack application that uses Google Gemini AI for intelligent skill extraction from resumes and job descriptions, with automated job search and matching capabilities.

## 🌟 Features

### Backend API
- 📄 **PDF Processing**: Extract text from PDF resumes and job descriptions using PyMuPDF
- 🤖 **AI-Powered Analysis**: Google Gemini API for intelligent skill extraction and role suggestions
- 🔍 **Job Matching**: Compare resume skills with job requirements and calculate match scores
- 🌐 **Real-time Job Search**: Automated web scraping across multiple job boards
- ⚡ **Fast & Scalable**: Built with FastAPI for high performance
- 🔒 **Secure**: Environment-based configuration and CORS protection

### Frontend Application
- 🎨 **Modern UI**: Responsive design with TailwindCSS
- 📤 **Drag & Drop Upload**: Intuitive file upload with progress tracking
- 📊 **Results Visualization**: Beautiful display of match results and skill analysis
- � **Job Search Interface**: Browse and search job opportunities
- 📱 **Mobile Responsive**: Works seamlessly on all devices
- ⚡ **Real-time Updates**: Live API integration and status updates

## 🚀 Quick Start

### One-Command Setup
```bash
git clone <repository-url>
cd SkillMatchAPI
./start.sh
```

This will automatically:
- Set up Python virtual environment
- Install all dependencies
- Create configuration files
- Start the development server

### Access Your Application
- **Main Application**: http://localhost:8001/
- **API Documentation**: http://localhost:8001/docs
- **Test Interface**: http://localhost:8001/test

## 📋 Prerequisites

- Python 3.10+ (tested with Python 3.12.1)
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))
- Virtual environment (recommended)

## 🛠️ Manual Installation

### 1. Clone and Setup
```bash
git clone <repository-url>
cd SkillMatchAPI
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 4. Run the Application
```bash
python3 run.py
```

## 🎯 Getting Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
3. Click "Create API Key"
4. Copy the generated API key and add it to your `.env` file

## Usage

### Starting the Server

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### 1. Health Check
```http
GET /
```
Returns server status.

#### 2. Match Resume with Job Description
```http
POST /match
```
**Parameters**:
- `resume`: PDF file (multipart/form-data)
- `job_desc`: PDF file (multipart/form-data)

**Response**:
```json
{
  "resume_summary": "Summary of candidate's background",
  "job_summary": "Summary of job requirements",
  "resume_skills": ["Python", "FastAPI", "Machine Learning"],
  "job_skills": ["Python", "API Development", "AI/ML"],
  "matched_skills": ["Python"],
  "match_score": 75.5,
  "suggested_role": "Senior Python Developer",
  "job_search_query": "Senior Python Developer API Development AI/ML",
  "job_links": [
    "https://www.indeed.com/jobs?q=Senior+Python+Developer+API+Development",
    "https://www.linkedin.com/jobs/search/?keywords=Senior%20Python%20Developer",
    "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=Senior%20Python%20Developer"
  ],
  "resume_roles": ["Python Developer", "Software Engineer"],
  "job_roles": ["Senior Python Developer", "Backend Developer"]
}
```

#### 3. Extract Skills from Single PDF
```http
POST /extract-skills
```
**Parameters**:
- `file`: PDF file (multipart/form-data)

**Response**:
```json
{
  "filename": "resume.pdf",
  "extracted_data": {
    "skills": ["Python", "FastAPI", "Docker"],
    "roles": ["Backend Developer", "Software Engineer"],
    "summary": "Experienced developer with 5+ years in Python development"
  },
  "text_length": 1250
}
```

## Testing with cURL

### Test Health Check
```bash
curl http://localhost:8000/
```

### Test Skill Extraction
```bash
curl -X POST "http://localhost:8000/extract-skills" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/your/resume.pdf"
```

### Test Resume-Job Matching
```bash
curl -X POST "http://localhost:8000/match" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "resume=@path/to/resume.pdf" \
     -F "job_desc=@path/to/job_description.pdf"
```

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   PDF Upload    │───▶│  FastAPI Server  │───▶│  Gemini API     │
│   (Resume/Job)  │    │                  │    │  (Skill Extract)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │  Skill Matching  │───▶│  Job Search     │
                       │  & Scoring       │    │  Links          │
                       └──────────────────┘    └─────────────────┘
```

## Components

- **PDF Parser**: PyMuPDF for reliable text extraction
- **AI Integration**: Google Gemini API for intelligent content analysis
- **Matching Engine**: Semantic skill comparison and scoring
- **Web Search**: Direct links to major job boards
- **API Framework**: FastAPI for high-performance REST API

## Error Handling

The API includes comprehensive error handling for:
- Invalid file formats (non-PDF files)
- Empty or unreadable PDFs
- Gemini API failures
- JSON parsing errors
- Network connectivity issues

## Development

### Running in Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Project Structure
```
SkillMatchAPI/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .env                # Your environment variables (not in git)
├── .gitignore          # Git ignore rules
├── .venv/              # Virtual environment
└── README.md           # This file
```

## Deployment

The application is designed to be stateless and easily deployable on:
- **Docker containers**
- **AWS Lambda** (with appropriate adaptations)
- **Google Cloud Run**
- **Heroku**
- **Traditional VPS/servers**

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
2. Review [Gemini API documentation](https://ai.google.dev/docs)
3. Open an issue in this repository