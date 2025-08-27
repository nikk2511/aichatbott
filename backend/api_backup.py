import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import random

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body schema
class AskRequest(BaseModel):
    query: str

# Mock puja database
PUJA_DATABASE = {
    "ganesh chaturthi": {
        "summary": "Ganesh Chaturthi is a Hindu festival celebrating the birth of Lord Ganesha. It's a 10-day festival filled with devotion, prayers, and cultural celebrations.",
        "steps": [
            {"title": "Preparation", "instruction": "Clean the puja area and take a bath. Wear clean clothes."},
            {"title": "Idol Setup", "instruction": "Place the Ganesha idol on a clean platform. Decorate with flowers and rangoli."},
            {"title": "Kalash Sthapana", "instruction": "Fill a copper vessel with water and place mango leaves on top."},
            {"title": "Pran Pratishtha", "instruction": "Invoke life into the idol by chanting mantras and performing aarti."},
            {"title": "Puja Rituals", "instruction": "Offer modak, flowers, and perform 21 aartis with devotion."},
            {"title": "Visarjan", "instruction": "On the final day, immerse the idol in water with prayers."}
        ],
        "materials": [
            {"name": "Ganesha Idol", "product_match": "https://www.amazon.in"},
            {"name": "Modak (Sweet)", "product_match": "https://www.amazon.in"},
            {"name": "Flowers (Red and Yellow)", "product_match": "https://www.amazon.in"},
            {"name": "Incense Sticks", "product_match": "https://www.amazon.in"},
            {"name": "Camphor", "product_match": "https://www.amazon.in"},
            {"name": "Kumkum and Chandan", "product_match": "https://www.amazon.in"}
        ],
        "timings": ["Morning (6-8 AM)", "Evening (6-8 PM)", "Best during Shukla Paksha"],
        "mantras": [
            "ॐ गणपतये नमः",
            "वक्रतुण्ड महाकाय सूर्यकोटि समप्रभा",
            "निर्विघ्नं कुरु मे देव सर्वकार्येषु सर्वदा"
        ],
        "sources": [
            {"book": "Ganesh Puran", "page": 42, "snippet": "Ganesh Chaturthi should be celebrated with devotion and proper rituals."},
            {"book": "Shiv Puran", "page": 156, "snippet": "Lord Shiva declared Ganesha as the first deity to be worshipped."}
        ],
        "notes": "This is a mock response. For authentic information, please refer to traditional texts and consult with learned priests."
    },
    "diwali": {
        "summary": "Diwali, the Festival of Lights, celebrates the victory of light over darkness and good over evil. It's one of the most important Hindu festivals.",
        "steps": [
            {"title": "Cleaning", "instruction": "Clean the entire house thoroughly, especially the puja room."},
            {"title": "Decoration", "instruction": "Decorate with rangoli, diyas, and lights. Place diyas at the entrance."},
            {"title": "Lakshmi Puja", "instruction": "Perform Lakshmi Puja in the evening with proper mantras."},
            {"title": "Aarti", "instruction": "Perform aarti for Lakshmi and Ganesha together."},
            {"title": "Prasad Distribution", "instruction": "Distribute sweets and prasad to family and neighbors."}
        ],
        "materials": [
            {"name": "Diyas (Oil Lamps)", "product_match": "https://www.amazon.in"},
            {"name": "Rangoli Colors", "product_match": "https://www.amazon.in"},
            {"name": "Sweets (Laddoo, Barfi)", "product_match": "https://www.amazon.in"},
            {"name": "Flowers", "product_match": "https://www.amazon.in"},
            {"name": "Incense Sticks", "product_match": "https://www.amazon.in"}
        ],
        "timings": ["Evening (6-8 PM)", "During Amavasya", "Best during Kartik month"],
        "mantras": [
            "ॐ श्री महालक्ष्म्यै नमः",
            "ॐ गणपतये नमः",
            "सर्व मंगल मांगल्ये शिवे सर्वार्थ साधिके"
        ],
        "sources": [
            {"book": "Ramayan", "page": 78, "snippet": "Diwali marks the return of Lord Rama to Ayodhya after defeating Ravana."},
            {"book": "Lakshmi Puran", "page": 23, "snippet": "Goddess Lakshmi visits homes that are clean and well-lit on Diwali."}
        ],
        "notes": "This is a mock response. For authentic information, please refer to traditional texts and consult with learned priests."
    },
    "satyanarayan": {
        "summary": "Satyanarayan Puja is performed to seek blessings from Lord Vishnu and to fulfill wishes. It's a simple yet powerful puja.",
        "steps": [
            {"title": "Sankalp", "instruction": "Take a bath and wear clean clothes. Make a vow to perform the puja."},
            {"title": "Kalash Sthapana", "instruction": "Place a copper vessel with water and coconut on top."},
            {"title": "Pran Pratishtha", "instruction": "Invoke Lord Vishnu in the kalash with mantras."},
            {"title": "Puja Rituals", "instruction": "Offer flowers, fruits, and perform aarti with devotion."},
            {"title": "Katha", "instruction": "Read or listen to the Satyanarayan Katha."},
            {"title": "Prasad Distribution", "instruction": "Distribute prasad to all present."}
        ],
        "materials": [
            {"name": "Kalash (Copper Vessel)", "product_match": "https://www.amazon.in"},
            {"name": "Coconut", "product_match": "https://www.amazon.in"},
            {"name": "Banana", "product_match": "https://www.amazon.in"},
            {"name": "Flowers", "product_match": "https://www.amazon.in"},
            {"name": "Kumkum and Chandan", "product_match": "https://www.amazon.in"}
        ],
        "timings": ["Morning (6-8 AM)", "Evening (6-8 PM)", "On Purnima (Full Moon)"],
        "mantras": [
            "ॐ नमो भगवते वासुदेवाय",
            "ॐ श्री सत्यनारायणाय नमः",
            "कृष्णाय वासुदेवाय हरये परमात्मने"
        ],
        "sources": [
            {"book": "Skanda Puran", "page": 89, "snippet": "Satyanarayan Puja brings peace and prosperity to the family."},
            {"book": "Vishnu Puran", "page": 145, "snippet": "Lord Vishnu is pleased with simple devotion and pure heart."}
        ],
        "notes": "This is a mock response. For authentic information, please refer to traditional texts and consult with learned priests."
    },
    "durga puja": {
        "summary": "Durga Puja celebrates the victory of Goddess Durga over the demon Mahishasura. It's a 9-day festival of devotion and celebration.",
        "steps": [
            {"title": "Ghatasthapana", "instruction": "Place a pot with soil and sow barley seeds on the first day."},
            {"title": "Kalash Sthapana", "instruction": "Install the kalash and invoke Goddess Durga."},
            {"title": "Puja Rituals", "instruction": "Perform daily puja with flowers, incense, and aarti."},
            {"title": "Katha", "instruction": "Read Durga Saptashati or listen to the story."},
            {"title": "Aarti", "instruction": "Perform aarti with 108 diyas on the final day."},
            {"title": "Visarjan", "instruction": "Immerse the kalash in water with prayers."}
        ],
        "materials": [
            {"name": "Kalash", "product_match": "https://www.amazon.in"},
            {"name": "Barley Seeds", "product_match": "https://www.amazon.in"},
            {"name": "Red Cloth", "product_match": "https://www.amazon.in"},
            {"name": "Flowers (Red)", "product_match": "https://www.amazon.in"},
            {"name": "Incense Sticks", "product_match": "https://www.amazon.in"},
            {"name": "Kumkum and Chandan", "product_match": "https://www.amazon.in"}
        ],
        "timings": ["Morning (6-8 AM)", "Evening (6-8 PM)", "During Navratri"],
        "mantras": [
            "ॐ दुर्गायै नमः",
            "या देवी सर्वभूतेषु शक्तिरूपेण संस्थिता",
            "सर्वमंगलमांगल्ये शिवे सर्वार्थसाधिके"
        ],
        "sources": [
            {"book": "Devi Mahatmyam", "page": 67, "snippet": "Goddess Durga represents the supreme power that protects the universe."},
            {"book": "Markandeya Puran", "page": 234, "snippet": "Durga Puja during Navratri brings prosperity and removes obstacles."}
        ],
        "notes": "This is a mock response. For authentic information, please refer to traditional texts and consult with learned priests."
    }
}

def find_best_match(query):
    """Find the best matching puja from the database."""
    query_lower = query.lower()
    
    for puja_name, puja_data in PUJA_DATABASE.items():
        if puja_name in query_lower:
            return puja_data
    
    # If no exact match, return a generic response
    return {
        "summary": f"Information about {query}. This is a Hindu ritual that requires proper guidance from learned priests.",
        "steps": [
            {"title": "Preparation", "instruction": "Clean the puja area and take a bath. Wear clean clothes."},
            {"title": "Setup", "instruction": "Arrange all required materials as per tradition."},
            {"title": "Puja", "instruction": "Perform the puja with devotion and proper mantras."},
            {"title": "Aarti", "instruction": "Perform aarti and offer prasad."}
        ],
        "materials": [
            {"name": "Flowers", "product_match": "https://www.amazon.in"},
            {"name": "Incense Sticks", "product_match": "https://www.amazon.in"},
            {"name": "Kumkum and Chandan", "product_match": "https://www.amazon.in"}
        ],
        "timings": ["Morning (6-8 AM)", "Evening (6-8 PM)"],
        "mantras": ["ॐ नमः शिवाय", "ॐ गणपतये नमः"],
        "sources": [
            {"book": "Traditional Texts", "page": 1, "snippet": "Please consult with learned priests for authentic information."}
        ],
        "notes": "This is a mock response. For authentic and detailed information, please consult with learned priests and refer to traditional texts."
    }

# Test route
@app.get("/")
def root():
    return {"message": "Mock Puja AI API is running! (No OpenAI required)"}

# Chat endpoint
@app.post("/api/ask")
def ask_question(request: AskRequest):
    try:
        # Get response from mock database
        response = find_best_match(request.query)
        
        # Add a small delay to simulate API processing
        import time
        time.sleep(0.5)
        
        return response

    except Exception as e:
        return {
            "summary": "Error occurred while processing your request",
            "steps": [],
            "materials": [],
            "timings": [],
            "mantras": [],
            "sources": [],
            "notes": f"Error: {str(e)}. Please try again."
        }
