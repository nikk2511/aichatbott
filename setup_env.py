#!/usr/bin/env python3
"""
Environment Setup Script for Puja AI Chatbot
This script helps set up the necessary environment variables.
"""

import os
import sys

def create_env_file(filepath, content):
    """Create an environment file if it doesn't exist."""
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✅ Created {filepath}")
    else:
        print(f"⚠️  {filepath} already exists")

def main():
    print("🕉 Setting up Puja AI Chatbot Environment...\n")
    
    # Backend .env file
    backend_env_content = """# Backend Environment Variables
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBED_MODEL=text-embedding-3-small
"""
    
    # Frontend .env.local file
    frontend_env_content = """# Frontend Environment Variables
NEXT_PUBLIC_API_URL=http://localhost:8000
"""
    
    # Create backend .env
    create_env_file("backend/.env", backend_env_content)
    
    # Create frontend .env.local
    create_env_file("frontend/.env.local", frontend_env_content)
    
    print("\n📋 Setup Instructions:")
    print("1. Edit 'backend/.env' and add your OpenAI API key")
    print("2. Make sure both backend and frontend servers are running")
    print("3. Backend should be on http://localhost:8000")
    print("4. Frontend should be on http://localhost:3000 or http://localhost:3001")
    print("\n🚀 To start the servers:")
    print("   Backend: cd backend && python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000")
    print("   Frontend: cd frontend && npm run dev")

if __name__ == "__main__":
    main()
