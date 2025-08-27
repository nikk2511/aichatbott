# 🕉 Puja AI Chatbot

A full-stack application that provides detailed information about Hindu pujas and rituals using AI.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API Key (optional - mock API available)

### Setup

1. **Clone and navigate to the project:**
   ```bash
   cd aichat
   ```

2. **Set up environment variables:**
   ```bash
   python setup_env.py
   ```
   Then edit `backend/.env` and add your OpenAI API key (optional).

3. **Install dependencies:**
   ```bash
   # Backend dependencies
   cd backend
   pip install -r requirements.txt
   
   # Frontend dependencies
   cd ../frontend
   npm install
   ```

4. **Choose your API mode:**
   ```bash
   # For testing without OpenAI (recommended for first run)
   python switch_api.py mock
   
   # For real OpenAI API (requires valid API key)
   python switch_api.py real
   ```

5. **Start the servers:**
   ```bash
   # Terminal 1 - Backend (from project root)
   cd backend
   python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 2 - Frontend (from project root)
   cd frontend
   npm run dev
   ```

6. **Access the application:**
   - Frontend: http://localhost:3000 (or 3001 if 3000 is busy)
   - Backend API: http://localhost:8000

## 🔧 Issues Fixed

### 1. Frontend-Backend Connection
- **Problem**: Frontend was using dummy responses instead of connecting to the backend
- **Solution**: Updated `PujaWidget.jsx` to make actual API calls to the backend

### 2. API Response Structure Mismatch
- **Problem**: Backend returned simple text, frontend expected structured data
- **Solution**: Enhanced backend API to return structured JSON responses with:
  - Summary
  - Step-by-step instructions
  - Required materials
  - Best timings
  - Relevant mantras
  - Sources
  - Notes

### 3. CORS Issues
- **Problem**: Frontend couldn't connect to backend due to CORS restrictions
- **Solution**: Added CORS middleware to the FastAPI backend

### 4. Environment Configuration
- **Problem**: Missing environment files and configuration
- **Solution**: Created setup script and environment files for both frontend and backend

### 5. Error Handling
- **Problem**: Poor error handling in both frontend and backend
- **Solution**: Added comprehensive error handling with user-friendly messages

### 6. OpenAI API Quota Issues
- **Problem**: OpenAI API quota exceeded or billing issues
- **Solution**: Created mock API with realistic puja data for testing

## 🤖 API Modes

### Mock API (Recommended for Testing)
- **No OpenAI API key required**
- **Pre-loaded with realistic puja data**
- **Includes: Ganesh Chaturthi, Diwali, Satyanarayan Puja, Durga Puja**
- **Switch to mock**: `python switch_api.py mock`

### Real OpenAI API
- **Requires valid OpenAI API key with credits**
- **Dynamic AI-generated responses**
- **More comprehensive and detailed answers**
- **Switch to real**: `python switch_api.py real`

## 📁 Project Structure

```
aichat/
├── backend/
│   ├── api.py              # Main FastAPI application
│   ├── mock_api.py         # Mock API (no OpenAI required)
│   ├── api_backup.py       # Backup of original API
│   ├── ingestion.py        # PDF processing and vector storage
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Backend environment variables
│   ├── pdfs/              # PDF files for puja information
│   └── data/              # Vector database storage
├── frontend/
│   ├── app/
│   │   ├── page.js        # Main page component
│   │   ├── components/    # React components
│   │   └── globals.css    # Global styles
│   ├── utils/
│   │   └── api.js         # API utility functions
│   ├── package.json       # Node.js dependencies
│   └── .env.local         # Frontend environment variables
├── setup_env.py           # Environment setup script
├── switch_api.py          # API switching utility
└── README.md              # This file
```

## 🎯 Features

- **AI-Powered Responses**: Uses OpenAI GPT models for detailed puja information
- **Mock API**: Pre-loaded realistic responses for testing without API costs
- **Structured Data**: Returns organized information including steps, materials, and timings
- **Preset Queries**: Quick access to common pujas (Ganesh Chaturthi, Diwali, etc.)
- **Responsive Design**: Modern UI with Tailwind CSS
- **Real-time Chat**: Interactive chat interface for puja queries

## 🔌 API Endpoints

- `GET /` - Health check
- `POST /api/ask` - Ask about a puja
  - Request: `{"query": "How to perform Ganesh Chaturthi puja?"}`
  - Response: Structured JSON with puja details

## 🛠️ Development

### Backend Development
```bash
cd backend
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Adding New Features
1. Update the backend API in `backend/api.py`
2. Modify frontend components in `frontend/app/components/`
3. Test the integration between frontend and backend

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Quota Exceeded (Error 429)**
   - **Solution**: Use mock API - `python switch_api.py mock`
   - **Alternative**: Add credits to your OpenAI account

2. **Backend not starting**: Check if port 8000 is available
3. **Frontend not connecting**: Verify CORS settings and API URL
4. **Port conflicts**: Frontend will automatically use port 3001 if 3000 is busy

### Debug Mode
- Backend logs will show in the terminal where uvicorn is running
- Frontend logs are available in browser developer tools
- Check network tab for API call details

### API Switching
```bash
# Check current API mode
python switch_api.py status

# Switch to mock API (no OpenAI required)
python switch_api.py mock

# Switch to real OpenAI API
python switch_api.py real
```

## 📝 Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBED_MODEL=text-embedding-3-small
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 💡 Tips

1. **Start with Mock API**: Use `python switch_api.py mock` for initial testing
2. **Test Preset Buttons**: Try the preset puja buttons for quick testing
3. **Check API Status**: Use `python switch_api.py status` to see current mode
4. **Real API**: Only switch to real API when you have valid OpenAI credits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
