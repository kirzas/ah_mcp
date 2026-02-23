## LocalUtilsServer MCP

This is a simple MCP server built with `FastMCP` that exposes a few local utilities:

- `get_info`: returns basic information about the server and Python environment.
- `list_directory`: lists files and directories within the current working directory (with safety checks).
- `read_text_file`: reads a text file within the current working directory (with size limits).
- `add_numbers`: demo tool that adds two integers.

### Installation

Create and activate a virtual environment (optional, but recommended), then install dependencies:

```bash
pip install mcp
```

If you prefer to use a requirements file:

```bash
pip install -r requirements.txt
```

### Running the server

From the project directory:

```bash
python server.py
```

The server will start and listen for MCP connections on STDIN/STDOUT.

### Using with Cursor (or another MCP client)

Configure your MCP client to launch this server with a command similar to:

```json
{
  "mcpServers": {
    "local-utils": {
      "command": "python",
      "args": ["server.py"],
      "env": {}
    }
  }
}
```

After configuration, the client should discover the `get_info`, `list_directory`, `read_text_file`, and `add_numbers` tools automatically.

