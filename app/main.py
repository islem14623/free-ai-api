"""
Free AI Assistant API - Day 1
Using Google Gemini (100% FREE!)
Author: Islem Chenafi
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file!")

genai.configure(api_key=GEMINI_API_KEY)

# Create FastAPI app
app = FastAPI(
    title="Free AI Assistant API",
    description="AI-powered text processing with Google Gemini (FREE!)",
    version="1.0.0"
)


# ENDPOINT 1: Home
@app.get("/")
def home():
    """Welcome endpoint"""
    return {
        "message": "🎉 Welcome to Free AI Assistant API!",
        "status": "running",
        "ai_provider": "Google Gemini",
        "cost": "$0.00 (FREE!)"
    }


# ENDPOINT 2: Health Check
@app.get("/health")
def health_check():
    """Check if API is healthy"""
    return {
        "status": "healthy",
        "gemini_configured": GEMINI_API_KEY is not None
    }


# ENDPOINT 3: Test AI
@app.get("/test")
def test_ai():
    """Test if Gemini API is working"""
    try:
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        response = model.generate_content("Say 'Hello from Algeria!' in a friendly way")
        
        return {
            "status": "success",
            "ai_response": response.text,
            "message": "✅ Gemini API is working!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ENDPOINT 4: Summarize Text
class TextInput(BaseModel):
    text: str
    max_words: int = 100

@app.post("/summarize")
def summarize_text(input: TextInput):
    """Summarize long text"""
    try:
        # Validate
        if len(input.text) < 50:
            raise HTTPException(status_code=400, detail="Text too short")
        
        # Create AI model
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Ask AI to summarize
        prompt = f"Summarize this in {input.max_words} words:\n\n{input.text}"
        response = model.generate_content(prompt)
        
        # Return result
        return {
            "status": "success",
            "summary": response.text,
            "original_length": len(input.text.split()),
            "summary_length": len(response.text.split())
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
