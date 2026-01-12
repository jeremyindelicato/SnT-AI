# Start&Trade Backend

Backend orchestrator for the Start&Trade intelligent financial assistant using FastAPI, Ollama (Phi 3.5), and MCP.

## Architecture

```
backend/
├── app/                    # Main FastAPI application
│   ├── main.py            # FastAPI app & endpoints
│   ├── agent.py           # FinancialAgent class (Ollama integration)
│   ├── config.py          # Configuration settings
│   ├── models.py          # Pydantic models
│   └── prompts.py         # System prompts
├── mcp/                    # Model Context Protocol server
│   ├── mcp_server.py      # MCP server implementation
│   └── tools.py           # Tool definitions (get_market_data)
├── scripts/                # Utility scripts
└── requirements.txt        # Python dependencies
```

## Prerequisites

1. **Python 3.10+**
2. **Ollama** installed and running
3. **Phi 3.5 model** pulled in Ollama:
   ```bash
   ollama pull phi3.5
   ```

## Installation

1. Create and activate a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env if needed
   ```

## Running the Application

### Option 1: Run Backend Only (Port 8000)

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Run MCP Server Only (Port 8001)

```bash
cd backend
python -m mcp.mcp_server
```

### Option 3: Run Both Servers (Recommended for Development)

Terminal 1 - Backend:
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 - MCP Server:
```bash
cd backend
python -m mcp.mcp_server
```

## Testing the API

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "app_name": "Start&Trade Backend",
  "version": "1.0.0",
  "ollama_connected": true
}
```

### 2. Test Chat Endpoint

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Bonjour ! Peux-tu m'\''expliquer ce qu'\''est une action ?"
  }'
```

Expected response structure:
```json
{
  "success": true,
  "response": "Bonjour ! Je suis ravi de t'accompagner...",
  "model": "phi3.5",
  "conversation_length": 3,
  "error": null
}
```

### 3. Test MCP Tool

```bash
curl -X POST http://localhost:8001/tools/execute \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "get_market_data",
    "parameters": {"ticker": "AAPL"}
  }'
```

Expected response:
```json
{
  "success": true,
  "result": {
    "success": true,
    "ticker": "AAPL",
    "message": "Tool call logged. Ready to integrate with n8n for real data scraping of AAPL.",
    "webhook_ready": false,
    "timestamp": "2026-01-12T...",
    "note": "This is a skeleton response..."
  },
  "tool_name": "get_market_data"
}
```

### 4. List Available Tools

```bash
curl http://localhost:8001/tools
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Backend API**: http://localhost:8000/docs
- **MCP Server API**: http://localhost:8001/docs

## Next Steps

1. **Frontend Integration**: Connect a JavaScript/TypeScript frontend to the `/chat` endpoint
2. **n8n Webhook Setup**: Configure n8n for real Yahoo Finance scraping
3. **Tool Integration**: Connect the MCP tools to the FinancialAgent for real-time data retrieval
4. **Session Management**: Implement persistent conversation sessions

## Troubleshooting

### "Ollama connection failed"

Ensure Ollama is running:
```bash
ollama serve
```

Verify the model is available:
```bash
ollama list
```

If phi3.5 is not listed:
```bash
ollama pull phi3.5
```

### Import errors

Make sure you're in the backend directory and the virtual environment is activated:
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Project Status

✅ Backend orchestrator with FastAPI
✅ FinancialAgent with Ollama (Phi 3.5) integration
✅ System prompt for Start&Trade personality
✅ MCP server with get_market_data tool skeleton
⏳ n8n webhook integration (next sprint)
⏳ Frontend web application (next sprint)
⏳ Real-time tool calling integration (next sprint)
