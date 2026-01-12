"""
Start&Trade Backend - FastAPI Application
Main orchestrator for the financial assistant chatbot
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import ollama

from .config import settings
from .models import ChatRequest, ChatResponse, HealthResponse
from .agent import FinancialAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Global agent instance
financial_agent: FinancialAgent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    global financial_agent

    # Startup
    logger.info("Starting Start&Trade Backend...")
    financial_agent = FinancialAgent()

    # Verify Ollama connection
    try:
        ollama.list()
        logger.info("✓ Ollama connection successful")
    except Exception as e:
        logger.warning(f"⚠ Ollama connection failed: {e}")
        logger.warning("The application will start but chat functionality may not work")

    logger.info(f"✓ {settings.app_name} v{settings.app_version} started successfully")

    yield

    # Shutdown
    logger.info("Shutting down Start&Trade Backend...")


# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend orchestrator for Start&Trade intelligent financial assistant",
    lifespan=lifespan,
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Start&Trade Backend API",
        "version": settings.app_version,
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint to verify system status"""
    ollama_connected = False

    try:
        ollama.list()
        ollama_connected = True
    except Exception:
        pass

    return HealthResponse(
        status="healthy" if ollama_connected else "degraded",
        app_name=settings.app_name,
        version=settings.app_version,
        ollama_connected=ollama_connected,
    )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint for interacting with the Start&Trade financial assistant.

    Args:
        request: ChatRequest containing user message

    Returns:
        ChatResponse with assistant's reply
    """
    if not financial_agent:
        raise HTTPException(
            status_code=503, detail="Financial agent not initialized"
        )

    logger.info(f"Received chat request: {request.message[:100]}...")

    try:
        result = await financial_agent.chat(request.message)

        return ChatResponse(
            success=result["success"],
            response=result["response"],
            model=result.get("model"),
            conversation_length=result.get("conversation_length"),
            error=result.get("error"),
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/reset", tags=["Chat"])
async def reset_conversation():
    """Reset the conversation history"""
    if not financial_agent:
        raise HTTPException(
            status_code=503, detail="Financial agent not initialized"
        )

    financial_agent.reset_conversation()
    return {"message": "Conversation history reset successfully"}


@app.get("/chat/history", tags=["Chat"])
async def get_history():
    """Get current conversation history"""
    if not financial_agent:
        raise HTTPException(
            status_code=503, detail="Financial agent not initialized"
        )

    return {"history": financial_agent.get_conversation_history()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
