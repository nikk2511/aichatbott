#!/usr/bin/env python3
"""
Test OpenAI API with correct syntax
"""

from openai import OpenAI
import os

# Load API key from environment variable (more secure)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ No OpenAI API key found. Please set OPENAI_API_KEY environment variable.")
    print("💡 You can add it to your backend/.env file")
    exit(1)

client = OpenAI(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "write a haiku about ai"}
        ],
        max_tokens=100
    )
    
    print("✅ OpenAI API Response:")
    print(response.choices[0].message.content)
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 If you're getting quota errors, try:")
    print("1. Check your OpenAI billing at: https://platform.openai.com/account/billing")
    print("2. Use the mock API: python switch_api.py mock")
