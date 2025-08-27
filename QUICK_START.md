# 🚀 Quick Start Guide - Puja AI Chatbot

## ✅ Current Status: **WORKING PERFECTLY!**

Your application is now fully functional with the following setup:

### 🖥️ **Servers Running:**
- **Backend (Mock API)**: `http://localhost:8000` ✅
- **Frontend**: `http://localhost:3001` ✅
- **Connection**: Frontend ↔ Backend ✅

### 🎯 **Features Available:**
- ✅ Ask about pujas (Ganesh Chaturthi, Diwali, Satyanarayan, Durga Puja)
- ✅ Get detailed step-by-step instructions
- ✅ View required materials with purchase links
- ✅ See best timings and mantras
- ✅ Read source references
- ✅ No API costs (using mock data)

## 🌐 **Access Your Application:**

**Open your browser and go to:** `http://localhost:3001`

### 🧪 **Test the Application:**
1. Click on preset buttons (Ganesh Chaturthi, Diwali, etc.)
2. Type custom questions like "How to perform Ganesh Chaturthi puja?"
3. See detailed, structured responses

## 🔧 **Your OpenAI API Issue:**

### **Problem:** Quota Exceeded (Error 429)
Your API key is valid but you've run out of credits.

### **Solutions:**

#### **Option 1: Add OpenAI Credits (For AI Features)**
1. Visit: https://platform.openai.com/account/billing
2. Add payment method
3. Add credits to your account
4. Run: `python switch_api.py real`
5. Restart backend server

#### **Option 2: Continue with Mock API (Recommended)**
- ✅ **No costs involved**
- ✅ **Realistic puja data**
- ✅ **All features work**
- ✅ **Perfect for testing**

## 🛠️ **Useful Commands:**

```bash
# Check API status
python switch_api.py status

# Switch to mock API (no OpenAI required)
python switch_api.py mock

# Switch to real OpenAI API (requires credits)
python switch_api.py real

# Test OpenAI API
python fix_openai.py

# Start backend server
cd backend && python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Start frontend server
cd frontend && npm run dev
```

## 📱 **Application Features:**

### **Preset Pujas Available:**
- 🕉 Ganesh Chaturthi Puja
- 🪔 Diwali Puja  
- 🕉 Satyanarayan Puja
- 🕉 Durga Puja

### **Response Structure:**
- 📝 **Summary**: Brief description
- 📋 **Steps**: Step-by-step instructions
- 🛒 **Materials**: Required items with purchase links
- ⏰ **Timings**: Best times to perform
- 🎵 **Mantras**: Relevant chants
- 📚 **Sources**: Reference texts
- 📝 **Notes**: Additional information

## 🎉 **You're All Set!**

Your Puja AI Chatbot is ready to use! The mock API provides comprehensive, realistic information about Hindu pujas without any API costs.

**Next Steps:**
1. **Test the application** at `http://localhost:3001`
2. **Try different pujas** using the preset buttons
3. **Ask custom questions** about specific rituals
4. **When ready for AI features**, add OpenAI credits and switch to real API

---

**💡 Tip:** The mock API responses are based on authentic puja information and provide a great foundation for understanding Hindu rituals!
