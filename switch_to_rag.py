#!/usr/bin/env python3
"""
Switch to RAG API Script
This script switches to the RAG API that uses your uploaded PDF books.
"""

import os
import shutil
import sys

def switch_to_rag():
    """Switch to RAG API (uses uploaded PDF books)."""
    try:
        # Backup current API if it exists
        if os.path.exists("backend/api.py"):
            shutil.copy("backend/api.py", "backend/api_backup.py")
            print("✅ Backed up current API to api_backup.py")
        
        # Copy RAG API to main API
        shutil.copy("backend/rag_api.py", "backend/api.py")
        print("✅ Switched to RAG API (Uses your uploaded PDF books)")
        print("📚 Available books:")
        print("   - sai_divya_pooja.pdf")
        print("   - siva_puranam.pdf")
        print("   - Book-2-Lakshmi-Puja.pdf")
        print("   - chandi_r_sans-.pdf")
        print("   - Book-3-Durga-Puja.pdf")
        print("\n🚀 Start the server with: cd backend && python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000")
        
    except Exception as e:
        print(f"❌ Error switching to RAG API: {e}")

def main():
    print("🕉 Puja AI Chatbot - Switch to RAG API\n")
    print("This will switch to an API that searches through your uploaded PDF books!")
    print("The RAG API will provide authentic, sourced responses from your books.\n")
    
    choice = input("🤔 Switch to RAG API now? (y/n): ").lower()
    if choice == 'y':
        switch_to_rag()
    else:
        print("❌ Cancelled. Keeping current API.")

if __name__ == "__main__":
    main()
