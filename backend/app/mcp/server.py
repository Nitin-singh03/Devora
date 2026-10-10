import logging
import sys

# Ensure logging goes to stderr so stdout is reserved for MCP stdio protocol
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

try:
    from mcp.server.fastmcp import FastMCP
except (ImportError, ModuleNotFoundError):
    from mcp.server.mcpserver import MCPServer as FastMCP


mcp = FastMCP("Devora")

from app.mcp import tools  # noqa: F401, E402


if __name__ == "__main__":
    from app.mcp.server import mcp as server_mcp
    server_mcp.run()

