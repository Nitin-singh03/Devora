try:
    from mcp.server.fastmcp import FastMCP
except (ImportError, ModuleNotFoundError):
    from mcp.server.mcpserver import MCPServer as FastMCP


mcp = FastMCP("Devora")

from app.mcp import tools  # noqa: F401, E402


if __name__ == "__main__":
    mcp.run()
