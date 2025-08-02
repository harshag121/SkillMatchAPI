# Deployment Guide for SkillMatchAPI

## 🚀 Quick Start (Development)

### Prerequisites
- Python 3.10+
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### One-Command Setup
```bash
./start.sh
```

This script will:
- Set up virtual environment
- Install dependencies
- Create .env file from template
- Start the development server

### Manual Setup
```bash
# 1. Setup development environment
./setup-dev.sh

# 2. Edit .env file with your API key
nano .env

# 3. Start the server
python3 run.py
```

## 🌐 Access Points

Once running, access these URLs:
- **Frontend Application**: http://localhost:8001/
- **API Documentation**: http://localhost:8001/docs
- **Test Interface**: http://localhost:8001/test
- **Individual Pages**:
  - Upload Resume: http://localhost:8001/frontend/upload.html
  - Search Jobs: http://localhost:8001/frontend/jobs.html
  - View Results: http://localhost:8001/frontend/results.html
  - About: http://localhost:8001/frontend/about.html
  - Contact: http://localhost:8001/frontend/contact.html

## 🐳 Docker Deployment

### Development with Docker
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t skillmatch-api .
docker run -p 8001:8001 --env-file .env skillmatch-api
```

### Production with Docker Compose + Nginx
```bash
# Run with production profile (includes nginx reverse proxy)
docker-compose --profile production up --build

# Access via:
# - Frontend: http://localhost
# - API: http://localhost/api/
```

## ☁️ Cloud Deployment Options

### 1. Heroku
```bash
# Install Heroku CLI and login
heroku create your-app-name
heroku config:set GEMINI_API_KEY=your_api_key_here
git push heroku main
```

### 2. Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/your-project/skillmatch-api
gcloud run deploy --image gcr.io/your-project/skillmatch-api --platform managed
```

### 3. AWS ECS/Fargate
```bash
# Build and push to ECR
aws ecr create-repository --repository-name skillmatch-api
docker build -t skillmatch-api .
docker tag skillmatch-api:latest your-account.dkr.ecr.region.amazonaws.com/skillmatch-api:latest
docker push your-account.dkr.ecr.region.amazonaws.com/skillmatch-api:latest
```

### 4. DigitalOcean App Platform
- Create app from GitHub repository
- Set environment variable: `GEMINI_API_KEY`
- Deploy automatically on git push

## 🔧 Environment Variables

Required:
- `GEMINI_API_KEY`: Your Google Gemini API key

Optional:
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8001)
- `DEBUG`: Enable debug mode (default: false)
- `WORKERS`: Number of worker processes (default: 1)

## 📁 Project Structure

```
SkillMatchAPI/
├── main.py              # FastAPI application
├── run.py               # Server runner with configuration
├── job_scraper.py       # Job scraping functionality
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── start.sh            # Quick start script
├── setup-dev.sh        # Development setup
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── nginx.conf          # Nginx reverse proxy config
├── frontend/           # Frontend application
│   ├── index.html     # Landing page
│   ├── upload.html    # File upload page
│   ├── jobs.html      # Job search page
│   ├── results.html   # Results display
│   ├── about.html     # About page
│   ├── contact.html   # Contact page
│   └── skills.html    # Skill extraction page
└── __pycache__/       # Python cache (auto-generated)
```

## 🧪 Testing

### Manual Testing
1. Visit http://localhost:8001/test for the test interface
2. Upload dummy files provided (dummy_resume.pdf, dummy_job_description.pdf)
3. Test API endpoints via http://localhost:8001/docs

### API Testing with curl
```bash
# Health check
curl http://localhost:8001/docs

# Upload resume for skill extraction
curl -X POST "http://localhost:8001/extract-skills" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@dummy_resume.pdf"

# Search jobs
curl -X POST "http://localhost:8001/search-jobs" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{"query": "python developer", "location": "San Francisco"}'
```

## 🔒 Security Considerations

### Development
- API key stored in .env file (not committed to git)
- CORS enabled for all origins (restrictive in production)

### Production
- Use environment variables for secrets
- Restrict CORS origins to your domain
- Enable HTTPS
- Use reverse proxy (nginx) for additional security
- Implement rate limiting
- Use container security scanning

## 🛠️ Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY not set" error**
   - Solution: Edit .env file and add your API key

2. **"Port already in use" error**
   - Solution: Change PORT in .env or kill process using port 8001

3. **Frontend not loading**
   - Solution: Ensure frontend/ directory exists with HTML files

4. **PDF upload fails**
   - Solution: Check file size (<10MB) and format (PDF/DOC/DOCX)

### Debug Mode
```bash
# Enable debug mode for detailed logs
echo "DEBUG=true" >> .env
python3 run.py
```

### View Logs
```bash
# Docker logs
docker-compose logs -f

# Local development
# Logs appear in terminal where server is running
```

## 📈 Performance Optimization

### Production Settings
- Set `DEBUG=false`
- Increase `WORKERS` based on CPU cores
- Use nginx reverse proxy
- Enable gzip compression
- Implement caching for job search results
- Use CDN for static assets

### Monitoring
- Enable access logs
- Monitor API response times
- Track Gemini API usage
- Set up health checks

## 🔄 Updates and Maintenance

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Database Migrations
Currently using file-based storage. For production, consider:
- PostgreSQL for job data
- Redis for caching
- S3 for file storage

### Backup Strategy
- Environment configuration (.env)
- Uploaded files (if stored locally)
- Job search cache (if implemented)
