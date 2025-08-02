#!/usr/bin/env python3
"""
Main entry point for running the SkillMatchAPI server
"""
import os
import sys
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Run the FastAPI server with uvicorn"""
    
    # Get configuration from environment variables with defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", os.getenv("WEBSITES_PORT", "8001")))  # Azure compatibility
    debug = os.getenv("DEBUG", "False").lower() == "true"
    workers = int(os.getenv("WORKERS", "1"))
    
    # Verify required environment variables
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable is required!")
        print("Please set your Gemini API key in the .env file or environment")
        sys.exit(1)
    
    print(f"🚀 Starting SkillMatchAPI server...")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🐛 Debug mode: {debug}")
    print(f"👥 Workers: {workers}")
    print(f"🌐 Access URL: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🧪 Test Interface: http://{host}:{port}/test")
    
    # Configuration for uvicorn
    config = {
        "app": "main:app",
        "host": host,
        "port": port,
        "reload": debug,
        "workers": 1 if debug else workers,  # Single worker in debug mode for reload
        "access_log": True,
        "log_level": "debug" if debug else "info"
    }
    
    try:
        uvicorn.run(**config)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
