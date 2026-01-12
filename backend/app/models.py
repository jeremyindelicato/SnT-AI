"""
Pydantic models for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""

    message: str = Field(..., min_length=1, description="User message to the assistant")
    session_id: Optional[str] = Field(
        None, description="Optional session ID to maintain conversation context"
    )


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""

    success: bool = Field(..., description="Whether the request was successful")
    response: str = Field(..., description="Assistant's response message")
    model: Optional[str] = Field(None, description="Model used for generation")
    conversation_length: Optional[int] = Field(
        None, description="Number of messages in conversation history"
    )
    error: Optional[str] = Field(None, description="Error message if request failed")


class HealthResponse(BaseModel):
    """Response model for health check endpoint"""

    status: str
    app_name: str
    version: str
    ollama_connected: bool
