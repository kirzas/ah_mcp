## Appie MCP

MCP server that exposes appie CLI commands as tools. It runs appie via `uv run appie` from the appie project directory (configurable with `APPIE_PROJECT_DIR`, default `D:\git\ah_app`).

### Tools

- **receipt_list** — List the last n receipts (`appie receipt -n N`).
- **receipt_show** — Show details for a single receipt by ID (`appie receipt show <id>`).
- **search** — Search with appie (`appie search -n N query`).
- **order_list** — List orders (`appie order`).
- **order_show** — Show details for a single order by ID (`appie order show <order-id>`).
- **order_add** — Add a product to an order (`appie order add -n N <order-id> <product>`).

### Installation

Create and activate a virtual environment (optional), then install dependencies:

```bash
pip install -r requirements.txt
```

Or with uv:

```bash
uv sync
```

### Running the server

From the project directory:

```bash
python appie.py
```

The server listens for MCP connections on STDIN/STDOUT.

### Using with Cursor (or another MCP client)

Configure your MCP client to launch the Appie server, for example:

```json
{
  "mcpServers": {
    "user-appie": {
      "command": "python",
      "args": ["appie.py"],
      "env": {}
    }
  }
}
```

Set `APPIE_PROJECT_DIR` in `env` if your appie project is not at `D:\git\ah_app`.

After configuration, the client will discover the receipt, search, and order tools automatically.
