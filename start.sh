#!/bin/bash

# SkillMatchAPI Start Script
# This script sets up and runs the SkillMatchAPI server

set -e  # Exit on any error

echo "🚀 SkillMatchAPI Startup Script"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if Python is installed
print_step "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.10+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_status "Python version: $PYTHON_VERSION"

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    print_error "main.py not found. Please run this script from the SkillMatchAPI directory."
    exit 1
fi

# Create virtual environment if it doesn't exist
print_step "Setting up virtual environment..."
if [ ! -d ".venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
print_step "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_step "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_status "Dependencies installed successfully"
else
    print_error "requirements.txt not found"
    exit 1
fi

# Check for .env file
print_step "Checking environment configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        print_warning ".env file not found. Creating from .env.example..."
        cp .env.example .env
        print_warning "Please edit .env file and add your GEMINI_API_KEY before running the server"
        echo ""
        echo "To get your Gemini API key:"
        echo "1. Go to https://aistudio.google.com/app/apikey"
        echo "2. Sign in with your Google account"
        echo "3. Create a new API key"
        echo "4. Copy the key and paste it in the .env file"
        echo ""
        read -p "Press Enter after you've updated the .env file with your API key..."
    else
        print_error ".env.example file not found. Please create a .env file with GEMINI_API_KEY"
        exit 1
    fi
fi

# Verify GEMINI_API_KEY is set
if ! grep -q "^GEMINI_API_KEY=.*[^[:space:]]" .env; then
    print_error "GEMINI_API_KEY is not properly set in .env file"
    print_warning "Please edit .env file and add your Gemini API key"
    exit 1
fi

print_status "Environment configuration OK"

# Create dummy PDFs if they don't exist
print_step "Checking test files..."
if [ ! -f "dummy_resume.pdf" ] || [ ! -f "dummy_job_description.pdf" ]; then
    print_status "Creating dummy PDF files for testing..."
    python3 create_dummy_pdfs.py
fi

# Start the server
print_step "Starting SkillMatchAPI server..."
echo ""
print_status "Server starting with the following URLs:"
echo "  🌐 Main API: http://localhost:8001"
echo "  📚 API Docs: http://localhost:8001/docs"
echo "  🧪 Test Interface: http://localhost:8001/test"
echo "  📱 Frontend: http://localhost:8001/frontend/"
echo ""
print_status "Press Ctrl+C to stop the server"
echo ""

# Run the server
python3 run.py
