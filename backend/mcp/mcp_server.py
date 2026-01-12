"""
MCP Server - Model Context Protocol Server for Start&Trade
Manages tool registration and execution
"""
import logging
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .tools import market_data_tool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app for MCP server
mcp_app = FastAPI(
    title="Start&Trade MCP Server",
    version="1.0.0",
    description="Model Context Protocol server for financial tools",
)


class ToolCallRequest(BaseModel):
    """Request model for tool execution"""

    tool_name: str
    parameters: Dict


class ToolCallResponse(BaseModel):
    """Response model for tool execution"""

    success: bool
    result: Dict
    tool_name: str


@mcp_app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Start&Trade MCP Server",
        "version": "1.0.0",
        "available_tools": [tool["function"]["name"] for tool in get_available_tools()],
    }


@mcp_app.get("/tools", tags=["Tools"])
async def list_tools() -> List[Dict]:
    """
    List all available tools with their definitions.

    Returns:
        List of tool definitions in MCP format
    """
    logger.info("Listing available tools")
    return get_available_tools()


@mcp_app.post("/tools/execute", response_model=ToolCallResponse, tags=["Tools"])
async def execute_tool(request: ToolCallRequest):
    """
    Execute a specific tool with provided parameters.

    Args:
        request: ToolCallRequest with tool name and parameters

    Returns:
        ToolCallResponse with execution result
    """
    logger.info(f"Executing tool: {request.tool_name} with params: {request.parameters}")

    # Route to appropriate tool
    if request.tool_name == "get_market_data":
        ticker = request.parameters.get("ticker")

        if not ticker:
            raise HTTPException(
                status_code=400, detail="Missing required parameter: ticker"
            )

        result = market_data_tool.get_market_data(ticker)

        return ToolCallResponse(
            success=result.get("success", False),
            result=result,
            tool_name=request.tool_name,
        )

    else:
        logger.error(f"Unknown tool requested: {request.tool_name}")
        raise HTTPException(status_code=404, detail=f"Tool not found: {request.tool_name}")


@mcp_app.get("/health", tags=["Health"])
async def health_check():
    """Health check for MCP server"""
    return {
        "status": "healthy",
        "server": "Start&Trade MCP Server",
        "tools_count": len(get_available_tools()),
    }


def get_available_tools() -> List[Dict]:
    """
    Get all available tools.

    Returns:
        List of tool definitions
    """
    return [market_data_tool.get_tool_definition()]


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting MCP Server on port 8001...")
    uvicorn.run(
        "mcp.mcp_server:mcp_app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info",
    )
