"""Entry point to run the Aviationstack MCP server over HTTP/SSE on cloud platforms."""

# pylint: disable=wrong-import-position,invalid-name

import os
import sys
from pathlib import Path

# Add src/ to sys.path so aviationstack_mcp is found regardless of installation mode
SRC_PATH = str(Path(__file__).parent / "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

import uvicorn
from starlette.responses import JSONResponse
from starlette.routing import Route
from aviationstack_mcp.server import mcp

# Disable DNS rebinding check so external host headers (e.g., *.onrender.com) are accepted
mcp.settings.transport_security = None

# Build the Starlette ASGI application using SSE transport
app = mcp.sse_app()

# Add root and health endpoints for platform health checks
app.routes.append(
    Route("/", lambda req: JSONResponse({"status": "ok", "service": "Aviationstack MCP"}))
)
app.routes.append(
    Route("/health", lambda req: JSONResponse({"status": "ok"}))
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
