from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Medicine Quality Chatbot API",
    description="AI Chatbot for medicine quality and monitoring",
    version="1.0.0"
)

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "medicine-quality-chatbot"}
    )

# API Root
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Medicine Quality Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "chat": "/api/v1/chat"
        }
    }

# Medicine Authentication Endpoint
@app.post("/api/v1/chat")
async def chat(message: dict):
    """
    Chat endpoint for medicine quality queries
    
    Request body:
    {
        "message": "Is this medicine genuine?",
        "medicine_name": "Aspirin",
        "batch_number": "ABC123"
    }
    """
    try:
        user_message = message.get("message", "")
        medicine_name = message.get("medicine_name", "")
        batch_number = message.get("batch_number", "")
        
        logger.info(f"Chat request: {user_message}")
        
        # Placeholder for AI model response
        response = {
            "status": "success",
            "message": "Processing your query...",
            "medicine_name": medicine_name,
            "batch_number": batch_number,
            "authenticity": "genuine",
            "confidence": 0.95,
            "details": {
                "manufacturer": "XYZ Pharma",
                "expiry_date": "2025-12-31",
                "quality_status": "verified"
            }
        }
        
        return JSONResponse(status_code=200, content=response)
    
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "details": str(e)}
        )

# Medicine Database Query Endpoint
@app.get("/api/v1/medicine/{medicine_name}")
async def get_medicine_info(medicine_name: str):
    """Get medicine information"""
    try:
        # Placeholder for database query
        medicine_data = {
            "name": medicine_name,
            "type": "Analgesic",
            "manufacturer": "XYZ Pharma",
            "active_ingredient": "Acetylsalicylic Acid",
            "dosage": "500mg",
            "side_effects": ["Nausea", "Dizziness"],
            "interactions": ["Warfarin", "Ibuprofen"],
            "contraindications": ["Pregnancy", "Bleeding disorders"]
        }
        return JSONResponse(status_code=200, content=medicine_data)
    
    except Exception as e:
        logger.error(f"Error fetching medicine info: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to fetch medicine information"}
        )

# Batch Verification Endpoint
@app.post("/api/v1/verify-batch")
async def verify_batch(batch_data: dict):
    """Verify medicine batch authenticity"""
    try:
        batch_number = batch_data.get("batch_number")
        qr_code = batch_data.get("qr_code")
        
        # Placeholder for verification logic
        verification_result = {
            "batch_number": batch_number,
            "status": "verified",
            "authenticity": "genuine",
            "manufacturing_date": "2023-01-15",
            "expiry_date": "2025-12-31",
            "quality_score": 98.5
        }
        
        return JSONResponse(status_code=200, content=verification_result)
    
    except Exception as e:
        logger.error(f"Error verifying batch: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Batch verification failed"}
        )

# Error handler
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
