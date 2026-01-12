"""
Configuration settings for Start&Trade Backend
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # Application
    app_name: str = "Start&Trade Backend"
    app_version: str = "1.0.0"

    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "phi3.5"

    # MCP Server
    mcp_server_url: str = "http://localhost:8001"

    # n8n Webhook (for future integration)
    n8n_webhook_url: str = "http://localhost:5678/webhook"

    # API
    api_prefix: str = "/api/v1"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
