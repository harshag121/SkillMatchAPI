#!/usr/bin/env python3
"""
Create dummy PDF files for testing the SkillMatchAPI
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_dummy_resume():
    """Create a dummy resume PDF"""
    filename = "dummy_resume.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "John Doe - Software Developer")
    
    # Contact Info
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, "Email: john.doe@email.com | Phone: (555) 123-4567")
    c.drawString(50, height - 100, "LinkedIn: linkedin.com/in/johndoe")
    
    # Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 140, "Professional Summary")
    c.setFont("Helvetica", 11)
    summary_text = [
        "Experienced Software Developer with 5+ years in full-stack development.",
        "Proficient in Python, JavaScript, React, and Node.js.",
        "Strong background in API development, database design, and cloud technologies.",
        "Passionate about machine learning and artificial intelligence applications."
    ]
    y_pos = height - 160
    for line in summary_text:
        c.drawString(50, y_pos, line)
        y_pos -= 20
    
    # Skills
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_pos - 20, "Technical Skills")
    c.setFont("Helvetica", 11)
    skills_text = [
        "• Programming Languages: Python, JavaScript, Java, TypeScript, SQL",
        "• Frameworks: FastAPI, Django, React, Node.js, Express.js",
        "• Databases: PostgreSQL, MongoDB, Redis, MySQL",
        "• Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD, Git",
        "• Machine Learning: TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy",
        "• Tools: VS Code, IntelliJ, Postman, Jira, Slack"
    ]
    y_pos -= 40
    for skill in skills_text:
        c.drawString(50, y_pos, skill)
        y_pos -= 20
    
    # Experience
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_pos - 20, "Work Experience")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_pos - 40, "Senior Software Developer - Tech Solutions Inc. (2021-Present)")
    c.setFont("Helvetica", 11)
    exp_text = [
        "• Developed and maintained RESTful APIs using Python and FastAPI",
        "• Built responsive web applications using React and TypeScript",
        "• Implemented machine learning models for data analysis and predictions",
        "• Collaborated with cross-functional teams using Agile methodologies",
        "• Optimized database queries and improved application performance by 40%"
    ]
    y_pos -= 60
    for exp in exp_text:
        c.drawString(50, y_pos, exp)
        y_pos -= 18
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_pos - 20, "Full Stack Developer - StartupXYZ (2019-2021)")
    c.setFont("Helvetica", 11)
    exp2_text = [
        "• Built full-stack applications using Django and React",
        "• Designed and implemented PostgreSQL database schemas",
        "• Deployed applications on AWS using Docker containers",
        "• Participated in code reviews and maintained high code quality standards"
    ]
    y_pos -= 40
    for exp in exp2_text:
        c.drawString(50, y_pos, exp)
        y_pos -= 18
    
    # Education
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_pos - 30, "Education")
    c.setFont("Helvetica", 11)
    c.drawString(50, y_pos - 50, "Bachelor of Science in Computer Science - University of Technology (2019)")
    
    c.save()
    return filename

def create_dummy_job_description():
    """Create a dummy job description PDF"""
    filename = "dummy_job_description.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "Senior Python Developer")
    
    # Company Info
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 80, "AI Innovations Corp")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "Location: San Francisco, CA | Type: Full-time | Salary: $120k-150k")
    
    # Job Overview
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 140, "Job Overview")
    c.setFont("Helvetica", 11)
    overview_text = [
        "We are seeking a Senior Python Developer to join our AI team and help build",
        "cutting-edge machine learning applications. The ideal candidate will have strong",
        "experience in Python development, API design, and artificial intelligence technologies."
    ]
    y_pos = height - 160
    for line in overview_text:
        c.drawString(50, y_pos, line)
        y_pos -= 20
    
    # Required Skills
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_pos - 20, "Required Skills & Qualifications")
    c.setFont("Helvetica", 11)
    required_skills = [
        "• 5+ years of experience in Python development",
        "• Strong experience with FastAPI, Django, or Flask frameworks",
        "• Proficiency in machine learning libraries (TensorFlow, PyTorch, Scikit-learn)",
        "• Experience with RESTful API development and microservices architecture",
        "• Knowledge of SQL databases (PostgreSQL, MySQL) and NoSQL (MongoDB)",
        "• Familiarity with cloud platforms (AWS, GCP, Azure)",
        "• Experience with Docker containerization and CI/CD pipelines",
        "• Strong understanding of software engineering best practices",
        "• Bachelor's degree in Computer Science or related field"
    ]
    y_pos -= 40
    for skill in required_skills:
        c.drawString(50, y_pos, skill)
        y_pos -= 20
    
    # Preferred Skills
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_pos - 20, "Preferred Skills")
    c.setFont("Helvetica", 11)
    preferred_skills = [
        "• Experience with Kubernetes and container orchestration",
        "• Knowledge of natural language processing (NLP) techniques",
        "• Familiarity with MLOps and model deployment strategies",
        "• Experience with data visualization tools (Matplotlib, Plotly)",
        "• Knowledge of distributed computing frameworks (Apache Spark)",
        "• Contributions to open-source projects"
    ]
    y_pos -= 40
    for skill in preferred_skills:
        c.drawString(50, y_pos, skill)
        y_pos -= 18
    
    # Responsibilities
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_pos - 30, "Key Responsibilities")
    c.setFont("Helvetica", 11)
    responsibilities = [
        "• Design and develop scalable Python applications and APIs",
        "• Implement machine learning models and integrate them into production systems",
        "• Collaborate with data scientists to productionize ML algorithms",
        "• Write clean, maintainable, and well-documented code",
        "• Participate in code reviews and maintain high development standards",
        "• Optimize application performance and ensure system reliability",
        "• Mentor junior developers and contribute to technical decision-making"
    ]
    y_pos -= 50
    for resp in responsibilities:
        c.drawString(50, y_pos, resp)
        y_pos -= 18
    
    # Benefits
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_pos - 30, "Benefits")
    c.setFont("Helvetica", 11)
    benefits_text = [
        "• Competitive salary and equity package",
        "• Comprehensive health, dental, and vision insurance",
        "• Flexible work arrangements and remote work options",
        "• Professional development budget and learning opportunities",
        "• Stock options and 401(k) matching"
    ]
    y_pos -= 50
    for benefit in benefits_text:
        c.drawString(50, y_pos, benefit)
        y_pos -= 18
    
    c.save()
    return filename

if __name__ == "__main__":
    print("Creating dummy PDF files for testing...")
    
    resume_file = create_dummy_resume()
    job_file = create_dummy_job_description()
    
    print(f"✅ Created {resume_file}")
    print(f"✅ Created {job_file}")
    print("\nFiles are ready for testing the SkillMatchAPI!")
