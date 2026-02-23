from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("MyServer")

# Define a tool
@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b

if __name__ == "__main__":
    mcp.run()