#!/bin/bash

# Development setup script for SkillMatchAPI
echo "🔧 Setting up development environment..."

# Create .env from example if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your GEMINI_API_KEY"
fi

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create dummy files if they don't exist
if [ ! -f "dummy_resume.pdf" ]; then
    echo "📄 Creating dummy test files..."
    python3 create_dummy_pdfs.py
fi

echo "✅ Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your GEMINI_API_KEY"
echo "2. Run: source .venv/bin/activate"
echo "3. Run: python3 run.py"
echo ""
echo "Or simply run: ./start.sh"
