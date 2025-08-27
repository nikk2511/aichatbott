#!/usr/bin/env python3
"""
API Switching Script for Puja AI Chatbot
This script helps you switch between real OpenAI API and mock API.
"""

import os
import shutil
import sys

def switch_to_mock():
    """Switch to mock API (no OpenAI required)."""
    try:
        # Backup original API if it exists
        if os.path.exists("backend/api.py"):
            shutil.copy("backend/api.py", "backend/api_backup.py")
            print("✅ Backed up original API to api_backup.py")
        
        # Copy mock API to main API
        shutil.copy("backend/mock_api.py", "backend/api.py")
        print("✅ Switched to Mock API (No OpenAI required)")
        print("🚀 Start the server with: cd backend && python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000")
        
    except Exception as e:
        print(f"❌ Error switching to mock API: {e}")

def switch_to_real():
    """Switch to real OpenAI API."""
    try:
        # Restore original API if backup exists
        if os.path.exists("backend/api_backup.py"):
            shutil.copy("backend/api_backup.py", "backend/api.py")
            print("✅ Switched to Real OpenAI API")
            print("⚠️  Make sure you have a valid OpenAI API key in backend/.env")
            print("🚀 Start the server with: cd backend && python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000")
        else:
            print("❌ No backup found. Please restore the original api.py manually.")
            
    except Exception as e:
        print(f"❌ Error switching to real API: {e}")

def show_status():
    """Show current API status."""
    if os.path.exists("backend/api.py"):
        with open("backend/api.py", "r") as f:
            content = f.read()
            if "mock" in content.lower():
                print("🔄 Current: Mock API (No OpenAI required)")
            else:
                print("🤖 Current: Real OpenAI API")
    else:
        print("❌ No API file found")

def main():
    print("🕉 Puja AI Chatbot - API Switcher\n")
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python switch_api.py mock    - Switch to Mock API (no OpenAI)")
        print("  python switch_api.py real    - Switch to Real OpenAI API")
        print("  python switch_api.py status  - Show current API status")
        return
    
    command = sys.argv[1].lower()
    
    if command == "mock":
        switch_to_mock()
    elif command == "real":
        switch_to_real()
    elif command == "status":
        show_status()
    else:
        print("❌ Invalid command. Use 'mock', 'real', or 'status'")

if __name__ == "__main__":
    main()
